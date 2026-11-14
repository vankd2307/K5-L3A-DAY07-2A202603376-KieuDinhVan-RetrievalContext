"""Regression tests for failure paths and preservation of explicit human reviews."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from src.common import digest
from src.agent import run_agent
from src.run import summaries
from src.reviews import aggregate_reviews
from scripts.write_reviews import validate_split

CID = 'a' * 24
CONFIG = {'name': 'baseline', 'method': 'tfidf', 'top_k': 3, 'candidates': 12, 'budget_chars': 1000, 'max_searches': 1}
CHUNK = {'id': CID, 'source_id': 'doc', 'source': 'doc.pdf', 'page': 1, 'text': 'Evidence.', 'metadata': {}}


def put(root, relative, value):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding='utf-8')
    return path


class Model:
    model = 'offline-test'
    def __init__(self, finish):
        self.calls = iter([{'name': 'search', 'args': {'query': 'evidence'}}, {'name': 'finish', 'args': finish}])
    def generate(self, body):
        return {'candidates': [{'content': {'role': 'model', 'parts': [{'functionCall': next(self.calls)}]}}]}, True


class Retriever:
    def search(self, *args):
        return [CHUNK]


def review_fixture(root):
    put(root, 'benchmark/dev.json', [{'id': 'q1', 'answerable': True, 'gold': [{'source_id': 'doc', 'page': 1, 'evidence': 'Evidence.'}]}])
    put(root, 'configs/experiments.json', {'configs': [{'name': 'baseline'}]})
    path = put(root, 'results/dev/baseline/agent/q1.json', {'status': 'answered', 'answer': 'Partial answer', 'citations': [CID]})
    labels = [{'config': 'baseline', 'query_id': 'q1', 'reviewer': 'Student reviewer', 'reason': 'Corrected after reading source.',
               'student_verified': True, 'trace_sha256': digest(path), 'citation_support': [False],
               'answer_grade': 1, 'context_grade': 1, 'abstention_correct': None, 'reviewed_at': 'original timestamp'}]
    label_path = put(root, 'results/review_labels.json', labels)
    return path, label_path


class RobustnessTests(unittest.TestCase):
    def test_invalid_citation_is_error_and_retains_raw_response(self):
        args = {'answer': 'Unsupported [fake]', 'citations': ['fake'], 'abstain': False}
        result = run_agent('Q', Model(args), Retriever(), CONFIG)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['reason'], 'invalid_citations')
        self.assertEqual(result['raw_answer'], args['answer'])
        self.assertEqual(result['raw_citations'], ['fake'])

    def test_actual_abstention_remains_distinct_from_output_failure(self):
        args = {'answer': 'Not enough evidence.', 'citations': [], 'abstain': True}
        result = run_agent('Q', Model(args), Retriever(), CONFIG)
        self.assertEqual(result['status'], 'abstain')
        self.assertNotIn('error', result)

    def test_empty_finish_answer_is_not_success(self):
        result = run_agent('Q', Model({'answer': ' ', 'citations': [CID], 'abstain': False}), Retriever(), CONFIG)
        self.assertEqual(result['status'], 'error')

    def test_external_value_error_is_redacted_and_failed_search_logged(self):
        class FailingRetriever:
            def search(self, *args):
                raise ValueError('postgresql://name:private-password@server/db')
        result = run_agent('Q', Model({}), FailingRetriever(), CONFIG)
        self.assertEqual(result['status'], 'error')
        self.assertNotIn('private-password', str(result))
        self.assertEqual(result['events'][0]['event'], 'search_error')
        self.assertEqual(result['search_count'], 1)

    def test_bom_env_and_environment_override(self):
        from src.common import settings
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            day6 = root / 'day6'
            (day6 / 'starter').mkdir(parents=True)
            (day6 / 'starter/.env').write_text('GEMINI_API_KEY=dummy-local-key\n', encoding='utf-8-sig')
            (root / '.env').write_text('DAY6_ROOT=' + str(day6) + '\nGEMINI_MODEL=local-model\n', encoding='utf-8-sig')
            with patch('src.common.ROOT', root), patch.dict('os.environ', {'GEMINI_MODEL': 'environment-model'}, clear=True):
                cfg = settings()
            self.assertEqual(cfg['DAY6_ROOT'], str(day6))
            self.assertEqual(cfg['GEMINI_API_KEY'], 'dummy-local-key')
            self.assertEqual(cfg['GEMINI_MODEL'], 'environment-model')

    def test_no_answerable_questions_returns_not_applicable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            put(root, 'benchmark/dev.json', [{'id': 'u1', 'answerable': False}])
            with patch('src.run.ROOT', root):
                row = summaries('dev', [{'name': 'baseline'}])[0]
            self.assertIsNone(row['hit1'])
            self.assertIsNone(row['agent_context_rate'])

    def test_review_validation_preserves_all_manual_fields_and_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, labels = review_fixture(root)
            before = labels.read_bytes()
            with patch('scripts.write_reviews.ROOT', root), patch('builtins.print'):
                validate_split('dev')
            self.assertEqual(before, labels.read_bytes())

    def test_aggregation_uses_actual_reviewer_and_confirmation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review_fixture(root)
            with patch('src.reviews.ROOT', root):
                row = aggregate_reviews('dev')[0]
            self.assertEqual(row['reviewers'], ['Student reviewer'])
            self.assertTrue(row['student_review_complete'])
            self.assertEqual(row['grounded_mean_out_of_2'], 1)
            self.assertEqual(row['citation_n'], 0)

    def test_aggregation_rejects_stale_labels_before_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace, _ = review_fixture(root)
            t = json.loads(trace.read_text(encoding='utf-8'))
            t['answer'] = 'Changed answer with same citation'
            trace.write_text(json.dumps(t), encoding='utf-8')
            with patch('src.reviews.ROOT', root), self.assertRaises(ValueError):
                aggregate_reviews('dev')
            self.assertFalse((root / 'results/audit_dev.json').exists())

    def test_missing_trace_reports_failed_check_instead_of_crashing(self):
        import scripts.verify as verify
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace, _ = review_fixture(root)
            trace.unlink()
            put(root, 'benchmark/test.json', [{'id': 't1', 'answerable': True, 'gold': [{'source_id': 'doc', 'page': 1, 'evidence': 'Evidence.'}]}])
            put(root, 'results/selection_lock.json', {'baseline': 'baseline', 'selected': 'baseline'})
            (root / '.gitignore').write_text('.env\n', encoding='utf-8')
            provenance = {'current_pipeline_matches_lock': True, 'archived_pipeline_matches_lock': False}
            with patch.object(verify, 'ROOT', root), patch('src.reviews.ROOT', root), \
                 patch.object(verify, 'inputs', return_value=([CHUNK], {'configs': [CONFIG], 'agent_model': 'offline-test'})), \
                 patch.object(verify, 'historical_state', return_value=provenance), \
                 patch.object(verify, 'settings', return_value={}), patch('builtins.print'), self.assertRaises(SystemExit) as stopped:
                verify.main()
            self.assertEqual(stopped.exception.code, 1)
            report = json.loads((root / 'results/delivery_checks.json').read_text(encoding='utf-8'))
            self.assertFalse(report['passed'])
            self.assertIn('dev/review_aggregation', report['failed'])


    def test_failed_agent_execution_still_updates_partial_summaries(self):
        import src.run as runner
        from src.provider import ProviderError
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            experiment = {'agent_model': 'offline-test', 'configs': [CONFIG]}
            cfg = {'GEMINI_MODEL': 'offline-test', 'DATABASE_URL': 'unused'}
            with patch.object(runner, 'ROOT', root), patch('sys.argv', ['run', 'agent']), \
                 patch.object(runner, 'inputs', return_value=([], experiment)), \
                 patch.object(runner, 'settings', return_value=cfg), patch.object(runner, 'Gemini'), \
                 patch.object(runner, 'Retrievers'), \
                 patch.object(runner, 'execute', side_effect=ProviderError('simulated quota failure')), \
                 patch.object(runner, 'summaries', return_value=[]) as summary, \
                 patch.object(runner, 'review_packet') as packet:
                with self.assertRaises(ProviderError):
                    runner.main()
                summary.assert_called_once_with('dev', [CONFIG])
                packet.assert_called_once_with('dev', [CONFIG])


if __name__ == '__main__':
    unittest.main()
