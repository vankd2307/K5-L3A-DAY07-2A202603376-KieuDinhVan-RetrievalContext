"""Validate existing dev reviews without changing scores, authors or confirmations."""
from copy import deepcopy
from src.common import ROOT, read, digest


def reviewed_support(existing, name, qid, path, citations):
    return list(reviewed_label(existing, name, qid, path, citations)['citation_support'])


def reviewed_label(existing, name, qid, path, citations):
    old = existing.get((name, qid))
    if old is None:
        raise ValueError('No source review recorded: ' + name + '/' + qid)
    if not path.exists() or old.get('trace_sha256') != digest(path):
        raise ValueError('Trace missing or changed since review: ' + name + '/' + qid)
    support = old.get('citation_support')
    if not isinstance(support, list) or len(support) != len(citations) or any(type(v) is not bool for v in support):
        raise ValueError('Explicit citation judgments required: ' + name + '/' + qid)
    return deepcopy(old)


def validate_split(split):
    existing = read(ROOT / 'results/review_labels.json')
    by_key = {(r['config'], r['query_id']): r for r in existing}
    if len(by_key) != len(existing):
        raise ValueError('Duplicate review labels.')
    if split == 'dev':
        names = [c['name'] for c in read(ROOT / 'configs/experiments.json')['configs']]
    else:
        lock = read(ROOT / 'results/selection_lock.json')
        names = list(dict.fromkeys([lock['baseline'], lock['selected']]))
    for name in names:
        for q in read(ROOT / 'benchmark' / (split + '.json')):
            path = ROOT / 'results' / split / name / 'agent' / (q['id'] + '.json')
            t = read(path)
            reviewed_label(by_key, name, q['id'], path, t['citations'])
    print('Validated existing ' + split + ' reviews; no labels were regenerated or overwritten.')
    return existing


def main():
    return validate_split('dev')


if __name__ == '__main__':
    main()
