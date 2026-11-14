"""Meaningful offline checks for isolation, fusion, citation checks and error traces."""
import unittest
from src.retrieval import fuse, context_pack, Retrievers
from src.agent import run_agent
from src.provider import ProviderError

CID = 'a' * 24
CHUNK = {'id': CID, 'source_id': 'book', 'source': 'book.pdf', 'page': 3,
         'text': 'A PMF maps values to probabilities.', 'metadata': {}, 'score': 1.0}
CONFIG = {'name': 'unit', 'method': 'tfidf', 'top_k': 3, 'candidates': 12,
          'budget_chars': 1000, 'max_searches': 1}


class MockGemini:
    model = 'offline-test-only'
    def __init__(self, calls):
        self.calls = iter(calls)
        self.bodies = []
    def generate(self, body):
        self.bodies.append(body)
        return {'candidates': [{'content': {'role': 'model', 'parts': [{'functionCall': next(self.calls)}]}}]}, False


class MockRetriever:
    def search(self, *args):
        return [CHUNK]


class LabTests(unittest.TestCase):
    def test_rrf_uses_rank_and_deduplicates_within_component(self):
        other = {**CHUNK, 'id': 'b' * 24, 'score': 100000}
        rows = fuse([[CHUNK, CHUNK, other], [other, CHUNK]], 2)
        self.assertEqual(len(rows), 2)
        first = next(r for r in rows if r['id'] == CID)
        self.assertAlmostEqual(first['score'], 1 / 61 + 1 / 62)

    def test_context_preserves_source_and_counts_delimiters(self):
        context, ids = context_pack([CHUNK, CHUNK], 1000)
        self.assertEqual(ids, [CID])
        self.assertIn('book.pdf | PDF page 3', context)
        self.assertEqual(context_pack([CHUNK], len(context) - 1), ('', []))

    def test_native_tool_search_then_citation_and_no_gold_in_request(self):
        model = MockGemini([{'name': 'search', 'args': {'query': 'PMF'}},
                            {'name': 'finish', 'args': {'answer': 'X [' + CID + ']', 'citations': [CID], 'abstain': False}}])
        result = run_agent('Question?', model, MockRetriever(), CONFIG)
        self.assertEqual(result['status'], 'answered')
        self.assertEqual(result['search_count'], 1)
        self.assertNotIn('gold', str(model.bodies))
        self.assertEqual(model.bodies[1]['toolConfig']['functionCallingConfig']['allowedFunctionNames'], ['finish'])

    def test_fabricated_citation_is_rejected(self):
        model = MockGemini([{'name': 'search', 'args': {'query': 'PMF'}},
                            {'name': 'finish', 'args': {'answer': 'X [fake]', 'citations': ['fake'], 'abstain': False}}])
        self.assertEqual(run_agent('Q', model, MockRetriever(), CONFIG)['status'], 'abstain')

    def test_error_remains_error_and_preserves_previous_events(self):
        class FailingGemini(MockGemini):
            def generate(self, body):
                if self.bodies:
                    raise ProviderError('Gemini HTTP 429')
                return super().generate(body)
        model = FailingGemini([{'name': 'search', 'args': {'query': 'PMF'}}])
        result = run_agent('Q', model, MockRetriever(), CONFIG)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(len(result['events']), 1)

    def test_lexical_retrieval_never_calls_api(self):
        rows = Retrievers([CHUNK], None, None).search('tfidf', 'PMF')
        self.assertEqual(rows[0]['id'], CID)


class AdditionalAgentTests(unittest.TestCase):
    def test_grouped_citations_normalize_but_unknown_ids_are_rejected(self):
        cid2 = 'b' * 24
        class TwoRetriever:
            def search(self, *args):
                return [CHUNK, {**CHUNK, 'id': cid2}]
        for second, expected in [(cid2, 'answered'), ('c' * 24, 'abstain')]:
            model = MockGemini([{'name': 'search', 'args': {'query': 'PMF'}},
                {'name': 'finish', 'args': {'answer': 'Evidence [' + CID + ', ' + second + ']',
                                          'citations': [CID, second], 'abstain': False}}])
            result = run_agent('Q', model, TwoRetriever(), CONFIG)
            self.assertEqual(result['status'], expected)
            if expected == 'answered':
                self.assertIn('[' + cid2 + ']', result['answer'])

    def test_model_cannot_finish_without_search(self):
        model = MockGemini([{'name': 'finish', 'args': {'answer': 'No search', 'citations': [], 'abstain': True}}])
        self.assertEqual(run_agent('Q', model, MockRetriever(), CONFIG)['status'], 'error')

    def test_database_error_string_is_redacted(self):
        class BrokenRetriever:
            def search(self, *args):
                raise RuntimeError('postgresql://name:secret@server/db')
        model = MockGemini([{'name': 'search', 'args': {'query': 'PMF'}}])
        result = run_agent('Q', model, BrokenRetriever(), CONFIG)
        self.assertEqual(result['status'], 'error')
        self.assertNotIn('secret', str(result))

    def test_free_tier_not_confirmed_means_no_network(self):
        from unittest.mock import patch
        from src.provider import Gemini
        model = Gemini({'DAY6_ROOT': str(__import__('pathlib').Path.cwd() / 'nonexistent'),
                        'GEMINI_MODEL': 'offline-test-only', 'GEMINI_API_KEY': 'dummy'})
        with patch('urllib.request.urlopen') as request:
            with self.assertRaises(ProviderError):
                model.request('models/x:generateContent', {})
            request.assert_not_called()


if __name__ == '__main__':
    unittest.main()
