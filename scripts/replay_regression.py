"""Regression replay of recorded tool decisions; never a new held-out evaluation."""
from copy import deepcopy
from src.common import ROOT, read, write, now
from src.agent import run_agent


class RecordedModel:
    def __init__(self, trace):
        self.model = trace['model']
        self.actions = iter([{'name': 'search', 'args': {'query': e['query']}} if e['event'] == 'search'
                             else {'name': 'finish', 'args': e['arguments']}
                             for e in trace['events'] if e['event'] in ('search', 'finish')])
    def generate(self, body):
        return {'candidates': [{'content': {'role': 'model', 'parts': [{'functionCall': deepcopy(next(self.actions))}]}}]}, True


class RecordedRetriever:
    def __init__(self, trace):
        self.events = iter(e for e in trace['events'] if e['event'] == 'search')
    def search(self, method, query, top_k, candidates):
        event = next(self.events)
        if query != event['query'] or method != event['tool']:
            raise ValueError('Replay diverged from recorded search.')
        return deepcopy(event['results'])


def main():
    archived = ROOT / 'artifacts/frozen_v1'
    configs = {c['name']: c for c in read(archived / 'configs/experiments.json')['configs']}
    checks = []
    for split in ('dev', 'test'):
        for path in sorted((archived / 'results' / split).glob('*/agent/*.json')):
            old = read(path)
            result = run_agent(old['question'], RecordedModel(old), RecordedRetriever(old), configs[old['config']])
            fields = ('status', 'answer', 'citations', 'context', 'context_ids', 'search_count')
            differences = [k for k in fields if result.get(k) != old.get(k)]
            checks.append({'split': split, 'config': old['config'], 'query_id': old['query_id'], 'differences': differences})
    output = {'at': now(), 'kind': 'offline regression using recorded decisions and retrieval results',
              'independent_test': False, 'api_requests': 0, 'cases': len(checks),
              'passed': not any(c['differences'] for c in checks), 'checks': checks}
    write(ROOT / 'results/maintenance/regression_v2.json', output)
    print('Recorded-decision replay:', len(checks), 'cases; passed:', output['passed'], '; API requests: 0')
    if not output['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
