"""CLI: check, retrieval, agent, freeze, test, summarize. All Day 6 access is read-only."""
import argparse
import hashlib
import json
import statistics
import time
from pathlib import Path
import psycopg
from .common import ROOT, read, write, settings, digest, supports, now
from .provider import Gemini, ProviderError
from .retrieval import Retrievers, context_pack
from .agent import run_agent


def inputs():
    frozen = read(ROOT / 'benchmark/frozen.json')
    paths = {'dev': 'benchmark/dev.json', 'test': 'benchmark/test.json', 'chunks': 'data/chunks.json', 'configs': 'configs/experiments.json'}
    for name, path in paths.items():
        if digest(ROOT / path) != frozen[name]:
            raise ValueError('Frozen input changed: ' + path)
    return read(ROOT / paths['chunks']), read(ROOT / paths['configs'])


def fingerprint():
    paths = ['benchmark/dev.json', 'benchmark/test.json', 'benchmark/PROTOCOL.md', 'data/chunks.json', 'data/manifest.json', 'configs/experiments.json']
    paths += sorted(str(p.relative_to(ROOT)).replace('\\', '/') for p in (ROOT / 'src').glob('*.py'))
    return {p: digest(ROOT / p) for p in paths}


def check(cfg, chunks):
    with psycopg.connect(cfg['DATABASE_URL'], connect_timeout=5, options='-c default_transaction_read_only=on') as conn:
        versions = conn.execute("SELECT version(),extversion FROM pg_extension WHERE extname='vector'").fetchone()
        rows = conn.execute("SELECT chunk_id,document_id,page,text FROM day6_chunks WHERE strategy='B' ORDER BY chunk_id").fetchall()
    expected = sorted((c['id'], c['source_id'], c['page'], c['text']) for c in chunks)
    if rows != expected:
        raise ValueError('Day 6 B index differs from the exported corpus.')
    report = {'at': now(), 'chunk_count': len(rows), 'read_only': True, 'index_matches': True,
              'versions': versions, 'embedding_model': 'gemini-embedding-001', 'dimensions': 768,
              'free_tier_confirmed_by_user': cfg.get('FREE_TIER_CONFIRMED') == 'true',
              'credential_configured': bool(cfg.get('GEMINI_API_KEY')), 'agent_model': cfg['GEMINI_MODEL']}
    write(ROOT / 'results/setup_check.json', report)
    print(json.dumps(report, ensure_ascii=False), flush=True)


def trace_path(split, name, qid, kind):
    return ROOT / 'results' / split / name / kind / (qid + '.json')


def retrieval_case(q, config, retrievers):
    started = time.perf_counter()
    rows = retrievers.search(config['method'], q['question'], max(3, config['top_k']), config['candidates'])
    context, ids = context_pack(rows[:config['top_k']], config['budget_chars'])
    gold = q['gold']
    return {'query_id': q['id'], 'split': q['split'], 'config': config['name'], 'status': 'ok',
            'query': q['question'], 'filter': {}, 'results': rows, 'context': context, 'context_ids': ids,
            'hit1': bool(rows and supports(rows[0], gold)), 'hit3': any(supports(c, gold) for c in rows[:3]),
            'context_hit': any(c['id'] in ids and supports(c, gold) for c in rows),
            'elapsed_ms': (time.perf_counter() - started) * 1000}


def execute(split, specs, retrievers, gemini, kind):
    questions = read(ROOT / 'benchmark' / (split + '.json'))
    execution_hash = hashlib.sha256(json.dumps(fingerprint(), sort_keys=True).encode()).hexdigest()
    for config in specs:
        for q in questions:
            if kind == 'retrieval' and not q['answerable']:
                continue
            path = trace_path(split, config['name'], q['id'], kind)
            if path.exists():
                previous = read(path)
                if previous.get('status') not in ('error', 'pending') and previous.get('execution_hash') == execution_hash:
                    continue
            if kind == 'retrieval':
                try:
                    result = retrieval_case(q, config, retrievers)
                    result['execution_hash'] = execution_hash
                except Exception as exc:
                    write(path, {'query_id': q['id'], 'config': config['name'], 'status': 'error', 'error_type': type(exc).__name__})
                    raise
            else:
                result = run_agent(q['question'], gemini, retrievers, config)
                result.update(query_id=q['id'], split=split, execution_hash=execution_hash)
                result['context_hit'] = any(
                    supports(c, q['gold']) and c['id'] in result['context_ids']
                    for e in result['events'] if e['event'] == 'search' for c in e['results']) if q['answerable'] else None
            if path.exists():
                previous = read(path)
                if kind == 'agent' and result['requests'] and all(x['cached'] for x in result['requests']) and previous.get('status') != 'error':
                    result['reference_elapsed_ms'] = previous.get('reference_elapsed_ms', previous['elapsed_ms'])
                    result['reference_elapsed_note'] = 'Timing from earlier real/cached mixed execution; current elapsed_ms measures cache replay.'
                result['previous_attempts'] = previous.get('previous_attempts', []) + [{k: v for k, v in previous.items() if k != 'previous_attempts'}]
            write(path, result)
            print(f"{split}/{config['name']}/{q['id']}/{kind}: {result['status']}", flush=True)
            if result['status'] == 'error':
                raise ProviderError('Stopped after a recorded agent error: ' + result.get('error', 'runtime failure'))


def summaries(split, specs):
    questions = read(ROOT / 'benchmark' / (split + '.json'))
    answerable = [q for q in questions if q['answerable']]
    table = []
    for config in specs:
        retrieval, agents = [], []
        for q in questions:
            for kind, target in [('retrieval', retrieval), ('agent', agents)]:
                path = trace_path(split, config['name'], q['id'], kind)
                if path.exists():
                    target.append(read(path))
        good = [r for r in retrieval if r['status'] == 'ok']
        answer_agents = [r for r in agents if any(q['id'] == r['query_id'] for q in answerable)]
        successful = [r for r in agents if r['status'] in ('answered', 'abstain')]
        calls = [r.get('search_count', 0) for r in successful]
        row = {'config': config['name'], 'split': split, 'expected_answerable': len(answerable), 'expected_total': len(questions),
               'retrieval_completed': len(good), 'agent_completed': len(successful),
               'agent_errors': sum(r['status'] == 'error' for r in agents),
               'hit1_n': sum(r['hit1'] for r in good), 'hit3_n': sum(r['hit3'] for r in good),
               'retrieval_context_n': sum(r['context_hit'] for r in good),
               'agent_context_n': sum(bool(r.get('context_hit')) for r in answer_agents),
               'tool_use_n': sum(n > 0 for n in calls), 'tool_use_N': len(calls),
               'search_count_distribution': {str(n): calls.count(n) for n in sorted(set(calls))},
               'agent_median_ms': statistics.median([r.get('reference_elapsed_ms', r['elapsed_ms']) for r in successful]) if successful else None,
               'agent_current_median_ms': statistics.median([r['elapsed_ms'] for r in successful]) if successful else None,
               'retrieval_median_ms': statistics.median([r['elapsed_ms'] for r in good]) if good else None,
               'successful_generation_requests': sum(len(r.get('requests', [])) for r in successful),
               'cached_generation_requests': sum(x.get('cached', False) for r in successful for x in r.get('requests', [])),
               'billing_cost_usd': None}
        for source, target in [('hit1_n', 'hit1'), ('hit3_n', 'hit3'), ('retrieval_context_n', 'retrieval_context_rate'), ('agent_context_n', 'agent_context_rate')]:
            row[target] = row[source] / len(answerable) if answerable else None
        table.append(row)
    write(ROOT / 'results' / ('summary_' + split + '.json'), table)
    return table


def freeze(specs, experiment):
    existing_lock = ROOT / 'results/selection_lock.json'
    if existing_lock.exists() and read(existing_lock)['fingerprint'] != fingerprint():
        raise ValueError('Historical lock belongs to frozen_v1; do not relock corrected code against the old test.')
    rows = summaries('dev', specs)
    for row in rows:
        if row['expected_answerable'] < 15 or row['expected_total'] - row['expected_answerable'] < 2:
            raise ValueError('Dev requires at least 15 answerable and 2 unanswerable cases.')
        if row['retrieval_completed'] != row['expected_answerable'] or row['agent_completed'] != row['expected_total'] or row['agent_errors']:
            raise ValueError('Need complete successful dev runs for every registered config before freezing.')
    by_name = {s['name']: s for s in specs}
    chosen = min(rows, key=lambda r: (-r['agent_context_rate'], -r['hit3'], -r['hit1'],
                 by_name[r['config']]['budget_chars'], by_name[r['config']]['max_searches'], r['config']))['config']
    lock_path = ROOT / 'results/selection_lock.json'
    lock = {'at': now(), 'selected': chosen, 'baseline': 'baseline', 'selection_rule': experiment['selection_rule'],
            'fingerprint': fingerprint(), 'dev_metrics': rows}
    if lock_path.exists():
        previous = read(lock_path)
        if previous['selected'] != chosen or previous['fingerprint'] != lock['fingerprint']:
            raise ValueError('Cannot replace an existing selection lock.')
    else:
        write(lock_path, lock)
    print('Frozen configuration: ' + chosen)


def review_packet(split, specs):
    cases = read(ROOT / 'benchmark' / (split + '.json'))
    packet = []
    for config in specs:
        for q in cases:
            path = trace_path(split, config['name'], q['id'], 'agent')
            if not path.exists():
                continue
            t = read(path)
            packet.append({'config': config['name'], 'query_id': q['id'], 'answerable': q['answerable'],
                           'status': t['status'], 'expected_answer': q.get('expected_answer'),
                           'gold': q['gold'], 'answer': t.get('answer'), 'context': t.get('context'),
                           'citations': t['citations'], 'reviewer': None, 'context_grade': None,
                           'answer_grade': None, 'citation_support': [None] * len(t['citations']),
                           'abstention_correct': None, 'reason': None, 'student_verified': False})
    write(ROOT / 'results' / ('review_packet_' + split + '.json'), packet)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['check', 'probe', 'retrieval', 'agent', 'freeze', 'test', 'summarize'])
    parser.add_argument('--split', default='dev', choices=['dev', 'test'])
    parser.add_argument('--configs', help='Comma-separated dev configs; test always uses frozen baseline and winner.')
    args = parser.parse_args()
    chunks, experiment = inputs()
    cfg = settings()
    if cfg['GEMINI_MODEL'] != experiment['agent_model']:
        raise ValueError('Agent model differs from registered experiment.')
    gemini = Gemini(cfg)
    retrievers = Retrievers(chunks, gemini, cfg['DATABASE_URL'])
    specs = experiment['configs']
    if args.phase == 'check':
        return check(cfg, chunks)
    if args.phase == 'probe':
        response, cached = gemini.generate({'contents': [{'role': 'user', 'parts': [{'text': 'Reply exactly OK.'}]}],
                                            'generationConfig': {'temperature': 0, 'maxOutputTokens': 16}})
        write(ROOT / 'results/model_probe.json', {'at': now(), 'model': gemini.model, 'response': response, 'cached': cached})
        print('Model probe saved (real API response).')
        return
    if args.phase == 'freeze':
        return freeze(specs, experiment)
    if args.configs:
        names = set(args.configs.split(','))
        if not names.issubset({s['name'] for s in specs}):
            raise ValueError('Unknown config.')
        specs = [s for s in specs if s['name'] in names]
    split = 'test' if args.phase == 'test' else args.split
    if split == 'test':
        lock = read(ROOT / 'results/selection_lock.json')
        if lock['fingerprint'] != fingerprint():
            raise ValueError('Current code differs from frozen_v1. Existing results belong to artifacts/frozen_v1; a new held-out benchmark is required for new evaluation.')
        specs = [s for s in experiment['configs'] if s['name'] in {lock['baseline'], lock['selected']}]
    elif (ROOT / 'results/selection_lock.json').exists() and args.phase in ('retrieval', 'agent'):
        raise ValueError('Dev already frozen; refuse further tuning.')
    try:
        if args.phase in ('retrieval', 'test'):
            execute(split, specs, retrievers, gemini, 'retrieval')
        if args.phase in ('agent', 'test'):
            execute(split, specs, retrievers, gemini, 'agent')
    finally:
        # Preserve partial progress/error counts even when a provider or retriever fails.
        table = summaries(split, specs)
        review_packet(split, specs)
    print(json.dumps(table, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    try:
        main()
    except (ProviderError, ValueError) as exc:
        raise SystemExit(str(exc))
