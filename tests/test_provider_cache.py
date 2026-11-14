"""Offline checks that failed Gemini responses are never replayed from the cache."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from src.provider import Gemini, cacheable

TOOLS_BODY = {'contents': [], 'tools': [{'functionDeclarations': []}]}
CALL = {'candidates': [{'content': {'parts': [{'functionCall': {'name': 'search', 'args': {'query': 'x'}}}]}}]}
MALFORMED = {'candidates': [{'finishReason': 'MALFORMED_FUNCTION_CALL', 'content': {}}]}
BLOCKED = {'candidates': [], 'promptFeedback': {'blockReason': 'SAFETY'}}


class ProviderCacheTests(unittest.TestCase):
    def test_cacheable_rules(self):
        self.assertTrue(cacheable(TOOLS_BODY, CALL))
        self.assertFalse(cacheable(TOOLS_BODY, MALFORMED))
        self.assertFalse(cacheable(TOOLS_BODY, BLOCKED))
        two = {'candidates': [{'content': {'parts': CALL['candidates'][0]['content']['parts'] * 2}}]}
        self.assertFalse(cacheable(TOOLS_BODY, two))
        self.assertTrue(cacheable({'contents': []}, {'candidates': [{'content': {'parts': [{'text': 'OK'}]}}]}))
        self.assertFalse(cacheable({'contents': []}, {'candidates': [{'content': {'parts': []}}]}))

    def test_failed_response_is_requested_again_instead_of_replayed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch('src.provider.ROOT', Path(tmp)):
                model = Gemini({'GEMINI_MODEL': 'offline-test-only', 'DAY6_ROOT': tmp})
            with patch.object(model, 'request', side_effect=[MALFORMED, CALL]) as request:
                first, cached_first = model.generate(TOOLS_BODY)
                second, cached_second = model.generate(TOOLS_BODY)
                third, cached_third = model.generate(TOOLS_BODY)
            self.assertEqual(request.call_count, 2)
            self.assertEqual((first, cached_first), (MALFORMED, False))
            self.assertEqual((second, cached_second), (CALL, False))
            self.assertEqual((third, cached_third), (CALL, True))


if __name__ == '__main__':
    unittest.main()
