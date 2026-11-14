"""Validate explicit review labels and aggregate them; never infer semantic scores."""
from collections import Counter
from .common import ROOT, read, write, digest


def aggregate_reviews(split):
    path = ROOT / 'results/review_labels.json'
    labels = read(path) if path.exists() else []
    cases = {q['id']: q for q in read(ROOT / 'benchmark' / (split + '.json'))}
    groups = {}
    seen = set()
    for r in labels:
        if r['query_id'] not in cases:
            continue
        key = r['config'], r['query_id']
        if key in seen:
            raise ValueError('Duplicate review label.')
        seen.add(key)
        trace = ROOT / 'results' / split / r['config'] / 'agent' / (r['query_id'] + '.json')
        if not trace.exists() or r.get('trace_sha256') != digest(trace):
            raise ValueError('Review trace missing or changed: ' + r['config'] + '/' + r['query_id'])
        t = read(trace)
        if t.get('status') == 'error':
            continue
        q = cases[r['query_id']]
        if not r.get('reviewer') or not r.get('reason'):
            raise ValueError('Each review needs a named reviewer and evidence-based reason.')
        supports = r['citation_support']
        if len(supports) != len(t['citations']) or any(type(x) is not bool for x in supports):
            raise ValueError('One semantic support label required for each citation.')
        if q['answerable']:
            if type(r.get('answer_grade')) is not int or r['answer_grade'] not in (0, 1, 2):
                raise ValueError('Answer grade must be 0/1/2.')
            if type(r.get('context_grade')) is not int or r['context_grade'] not in (0, 1, 2):
                raise ValueError('Context grade must be 0/1/2.')
            if t['status'] == 'abstain' and r['answer_grade'] != 0:
                raise ValueError('False abstention must receive zero.')
        elif type(r.get('abstention_correct')) is not bool:
            raise ValueError('Unanswerable case needs an abstention judgment.')
        if r.get('abstention_correct') and t['status'] != 'abstain':
            raise ValueError('Correct abstention label conflicts with trace.')
        group = groups.setdefault(r['config'], [])
        group.append((q, t, r))
    output = []
    for name, rows in groups.items():
        ans = [(q, t, r) for q, t, r in rows if q['answerable']]
        unans = [(q, t, r) for q, t, r in rows if not q['answerable']]
        answered = [(q, t, r) for q, t, r in rows if t['status'] == 'answered']
        output.append({'config': name, 'split': split, 'reviewed': len(rows),
            'reviewers': sorted({r['reviewer'] for q, t, r in rows}),
            'reviewer': '; '.join(sorted({r['reviewer'] for q, t, r in rows})),
            'student_review_complete': all(r.get('student_verified') is True for q, t, r in rows),
            'answer_citation_scope': 'Successfully answered outputs only; citation gate makes this conditional coverage, not grounding accuracy.',
            'answer_distribution': {str(n): sum(r['answer_grade'] == n for q, t, r in ans) for n in (0, 1, 2)},
            'context_distribution': {str(n): sum(r['context_grade'] == n for q, t, r in ans) for n in (0, 1, 2)},
            'grounded_mean_out_of_2': sum(r['answer_grade'] for q, t, r in ans) / len(ans) if ans else None,
            'citation_n': sum(sum(r['citation_support']) for q, t, r in rows),
            'citation_N': sum(len(r['citation_support']) for q, t, r in rows),
            'answer_citation_n': sum(bool(t['citations']) for q, t, r in answered), 'answer_citation_N': len(answered),
            'abstention_n': sum(r['abstention_correct'] for q, t, r in unans), 'abstention_N': len(unans),
            'false_abstention_n': sum(t['status'] == 'abstain' for q, t, r in ans), 'false_abstention_N': len(ans),
            'student_verified_n': sum(r.get('student_verified') is True for q, t, r in rows)})
    write(ROOT / 'results' / ('audit_' + split + '.json'), output)
    return output
