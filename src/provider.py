"""Real Gemini REST requests, content cache and explicit free-tier gate."""
import hashlib
import json
import math
import time
import urllib.error
import urllib.request
from .common import ROOT, now, read, write


class ProviderError(RuntimeError):
    pass


def cacheable(body, data):
    """Cache only usable responses, so a retry of a failed trace sends a fresh request.

    Tool requests need exactly one functionCall in the first candidate; plain requests need text.
    Empty candidates, safety blocks and malformed function calls are never replayed from cache.
    """
    candidates = data.get('candidates') or []
    if not candidates:
        return False
    parts = (candidates[0].get('content') or {}).get('parts') or []
    if body.get('tools'):
        return sum('functionCall' in p for p in parts) == 1
    return any(p.get('text') for p in parts)


class Gemini:
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = cfg['GEMINI_MODEL']
        self.cache_path = ROOT / '.cache/gemini_responses.json'
        self.cache = read(self.cache_path) if self.cache_path.exists() else {}
        self.embedding_path = ROOT / '.cache/query_embeddings.json'
        self.embeddings = read(self.embedding_path) if self.embedding_path.exists() else {}
        day6_path = __import__('pathlib').Path(cfg['DAY6_ROOT']) / '.cache/embeddings.json'
        self.day6_cache = read(day6_path) if day6_path.exists() else {}
        self.ledger_path = ROOT / 'results/api_usage.json'
        self.ledger = read(self.ledger_path) if self.ledger_path.exists() else []
        self.last_request = 0.0
        self.cache_hits = 0

    def request(self, endpoint, body):
        if self.cfg.get('FREE_TIER_CONFIRMED', '').lower() != 'true':
            raise ProviderError('Free tier not confirmed: set FREE_TIER_CONFIRMED=true only for a project without billing.')
        key = self.cfg.get('GEMINI_API_KEY', '').strip()
        if not key:
            raise ProviderError('GEMINI_API_KEY missing; configure local .env.')
        if len(self.ledger) >= int(self.cfg.get('GEMINI_MAX_REQUESTS', '180')):
            raise ProviderError('Request cap reached; no request sent.')
        interval = float(self.cfg.get('GEMINI_INTERVAL_SECONDS', '7'))
        time.sleep(max(0, self.last_request + interval - time.monotonic()))
        row = {'at': now(), 'endpoint': endpoint, 'status': 'pending',
               'free_tier_confirmed_by_user': True, 'billing_cost_usd': None}
        self.ledger.append(row)
        write(self.ledger_path, self.ledger)
        req = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/' + endpoint,
              json.dumps(body).encode(), {'Content-Type': 'application/json', 'x-goog-api-key': key})
        self.last_request = time.monotonic()
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                data = json.load(response)
            row.update(status='ok', usage=data.get('usageMetadata', {}))
            write(self.ledger_path, self.ledger)
            return data
        except urllib.error.HTTPError as exc:
            row['status'] = 'HTTP_' + str(exc.code)
            # Never print provider bodies, authorization headers or secrets.
            write(self.ledger_path, self.ledger)
            raise ProviderError('Gemini HTTP ' + str(exc.code) + '; stopped without paid fallback or automatic retry.') from None
        except Exception as exc:
            row['status'] = type(exc).__name__
            write(self.ledger_path, self.ledger)
            raise ProviderError('Gemini transport error: ' + type(exc).__name__) from None

    def generate(self, body):
        identity = hashlib.sha256(json.dumps([self.model, body], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        if identity in self.cache:
            self.cache_hits += 1
            return self.cache[identity], True
        result = self.request('models/' + self.model + ':generateContent', body)
        if cacheable(body, result):
            self.cache[identity] = result
            write(self.cache_path, self.cache)
        return result, False

    def embed(self, text):
        identity = hashlib.sha256(('gemini-embedding-001|768|RETRIEVAL_QUERY|' + text).encode()).hexdigest()
        value = self.embeddings.get(identity) or self.day6_cache.get(identity)
        if value is None:
            data = self.request('models/gemini-embedding-001:embedContent', {
                'model': 'models/gemini-embedding-001', 'content': {'parts': [{'text': text}]},
                'taskType': 'RETRIEVAL_QUERY', 'outputDimensionality': 768})
            value = data['embedding']['values']
            norm = math.sqrt(sum(float(x) ** 2 for x in value))
            if len(value) != 768 or not math.isfinite(norm) or norm == 0:
                raise ProviderError('Invalid embedding response.')
            value = [float(x) / norm for x in value]
            self.embeddings[identity] = value
            write(self.embedding_path, self.embeddings)
        else:
            self.cache_hits += 1
        if len(value) != 768 or not all(math.isfinite(float(x)) for x in value) or not any(value):
            raise ProviderError('Invalid cached embedding.')
        return value
