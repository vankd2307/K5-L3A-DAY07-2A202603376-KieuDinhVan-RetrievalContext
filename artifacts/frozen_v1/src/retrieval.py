"""TF-IDF, read-only Day 6 pgvector and reciprocal-rank fusion."""
import math
import re
from collections import Counter
import psycopg


def terms(text):
    return re.findall(r'\w+', text.casefold())


class Retrievers:
    def __init__(self, chunks, gemini, database_url):
        self.chunks, self.gemini, self.url = chunks, gemini, database_url
        counts = [Counter(terms(c['text'])) for c in chunks]
        df = Counter(t for row in counts for t in row)
        self.idf = {t: math.log((1 + len(chunks)) / (1 + n)) + 1 for t, n in df.items()}
        self.vectors = [self.vector(row) for row in counts]

    def vector(self, counts):
        row = {t: n * self.idf[t] for t, n in counts.items() if t in self.idf}
        norm = math.sqrt(sum(v * v for v in row.values())) or 1
        return {t: v / norm for t, v in row.items()}

    def lexical(self, query, top_k):
        q = self.vector(Counter(terms(query)))
        hits = [{**c, 'score': sum(v * vec.get(t, 0) for t, v in q.items()), 'method': 'tfidf'}
                for c, vec in zip(self.chunks, self.vectors)]
        return sorted((c for c in hits if c['score'] > 0), key=lambda c: (-c['score'], c['id']))[:top_k]

    def dense(self, query, top_k):
        vector = '[' + ','.join(map(str, self.gemini.embed(query))) + ']'
        with psycopg.connect(self.url, connect_timeout=5, options='-c default_transaction_read_only=on') as conn:
            rows = conn.execute('''SELECT chunk_id,document_id,source,page,text,metadata,
                 1-(embedding <=> %s::vector) FROM day6_chunks WHERE strategy=%s
                 ORDER BY embedding <=> %s::vector,chunk_id LIMIT %s''', (vector, 'B', vector, top_k)).fetchall()
        return [dict(zip(('id', 'source_id', 'source', 'page', 'text', 'metadata', 'score'), r), method='dense') for r in rows]

    def search(self, method, query, top_k=3, candidates=12):
        if method not in ('tfidf', 'dense', 'hybrid') or not query.strip() or not 1 <= top_k <= 100:
            raise ValueError('Invalid retrieval parameters.')
        if method == 'tfidf':
            return self.lexical(query, top_k)
        if method == 'dense':
            return self.dense(query, top_k)
        rankings = [self.dense(query, max(top_k, candidates)), self.lexical(query, max(top_k, candidates))]
        return fuse(rankings, top_k)


def fuse(rankings, top_k):
    scores, rows, provenance = {}, {}, {}
    for list_id, ranking in enumerate(rankings):
        seen = set()
        for rank, row in enumerate(ranking, 1):
            cid = row['id']
            if cid in seen:
                continue
            seen.add(cid)
            rows[cid] = row
            scores[cid] = scores.get(cid, 0) + 1 / (60 + rank)
            provenance.setdefault(cid, {})[str(list_id)] = rank
    return [{**rows[cid], 'score': scores[cid], 'method': 'hybrid', 'component_ranks': provenance[cid]}
            for cid in sorted(scores, key=lambda c: (-scores[c], c))[:top_k]]


def context_pack(rows, budget):
    blocks, ids, seen = [], [], set()
    for row in rows:
        if row['id'] in seen:
            continue
        seen.add(row['id'])
        block = '[{} | {} | PDF page {}]\n{}'.format(row['id'], row['source'], row['page'], row['text'])
        if len('\n\n'.join(blocks + [block])) <= budget:
            blocks.append(block)
            ids.append(row['id'])
    return '\n\n'.join(blocks), ids
