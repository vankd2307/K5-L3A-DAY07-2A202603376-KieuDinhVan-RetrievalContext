"""Offline delivery checks; does not call Gemini, DB, or modify Day 6."""
import json
import sys
from pathlib import Path
from src.common import ROOT, read, write, settings, digest, supports, now
from src.run import inputs, fingerprint, trace_path
from src.reviews import aggregate_reviews
from scripts.archive_status import historical_state


def main():
    chunks, experiment = inputs()
    lock = read(ROOT / 'results/selection_lock.json')
    provenance = historical_state()
    checks = {'historical_pipeline_available': provenance['current_pipeline_matches_lock'] or provenance['archived_pipeline_matches_lock'],
              'historical_lock_preserved': provenance['current_pipeline_matches_lock'] or provenance['historical_lock_preserved'],
              'historical_traces_unchanged': provenance['current_pipeline_matches_lock'] or provenance['historical_traces_unchanged'],
              'chunk_ids_unique': len({c['id'] for c in chunks}) == len(chunks),
              'minimum_30_pages': len({(c['source_id'], c['page']) for c in chunks}) >= 30}
    cases = {}
    reviews = read(ROOT / 'results/review_labels.json')
    reviews_by_key = {(r['config'], r['query_id']): r for r in reviews}
    for split in ('dev', 'test'):
        questions = read(ROOT / 'benchmark' / (split + '.json'))
        cases[split] = questions
        min_answerable, min_unanswerable = (15, 2) if split == 'dev' else (5, 2)
        checks[split + '_benchmark_counts'] = (sum(q['answerable'] for q in questions) >= min_answerable and
                                               sum(not q['answerable'] for q in questions) >= min_unanswerable)
        specs = experiment['configs'] if split == 'dev' else [s for s in experiment['configs'] if s['name'] in {lock['baseline'], lock['selected']}]
        for spec in specs:
            for q in questions:
                path = trace_path(split, spec['name'], q['id'], 'agent')
                prefix = split + '/' + spec['name'] + '/' + q['id']
                t = read(path) if path.exists() else {}
                checks[prefix + '/real_trace'] = t.get('model') == experiment['agent_model'] and t.get('status') in ('answered', 'abstain') and bool(t.get('requests'))
                checks[prefix + '/tool_used'] = t.get('search_count', 0) > 0
                checks[prefix + '/budget'] = len(t.get('context', '')) <= spec['budget_chars']
                checks[prefix + '/citations_in_context'] = all(cid in t.get('context_ids', []) for cid in t.get('citations', []))
                review = reviews_by_key.get((spec['name'], q['id']))
                checks[prefix + '/reviewed_current_trace'] = bool(review and path.exists() and review.get('trace_sha256') == digest(path))
                if q['answerable']:
                    checks[prefix + '/gold_exists'] = any(supports(c, q['gold']) for c in chunks)
        try:
            aggregate_reviews(split)
            checks[split + '/review_aggregation'] = True
        except (OSError, ValueError, KeyError, TypeError):
            checks[split + '/review_aggregation'] = False
    checks['dev_test_ids_disjoint'] = not ({q['id'] for q in cases['dev']} & {q['id'] for q in cases['test']})
    # Compare the local credential with deliverable text without ever displaying it.
    key = settings().get('GEMINI_API_KEY', '')
    candidates = []
    for folder in ('src', 'scripts', 'configs', 'benchmark', 'results', 'report', 'docs', 'data', 'artifacts'):
        candidates.extend(p for p in (ROOT / folder).rglob('*') if p.suffix in ('.py', '.md', '.json', '.txt'))
    candidates.extend(p for p in ROOT.iterdir() if p.is_file() and not p.name.startswith('.env'))
    leaks = []
    if key:
        for p in candidates:
            if key in p.read_text(encoding='utf-8-sig', errors='ignore'):
                leaks.append(str(p.relative_to(ROOT)))
    checks['no_credential_in_deliverables'] = not leaks
    checks['env_ignored'] = '.env' in (ROOT / '.gitignore').read_text(encoding='utf-8-sig').splitlines()
    failures = [name for name, ok in checks.items() if not ok]
    report = {'at': now(), 'passed': not failures, 'count': len(checks), 'failed': failures,
              'checks': checks, 'benchmark_provenance': provenance, 'student_review_pending': any(not r.get('student_verified') for r in reviews),
              'note': 'AI-assisted source-based labels are present; this does not certify student review or a rubric score.'}
    write(ROOT / 'results/delivery_checks.json', report)
    print(json.dumps({'passed': not failures, 'checks': len(checks), 'failed': failures,
                      'student_review_pending': report['student_review_pending'], 'benchmark_provenance': provenance}, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
