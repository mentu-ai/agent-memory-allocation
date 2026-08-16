"""L4 — the external implementation control (registration §2).

SQLite FTS5, `porter unicode61` tokenizer, BM25 ranking, behind the same
k=8 contract shape the navigator arms return. Deliberately NOT given a
Spanish stemmer: its control value is isolating *our per-language
analyzers and fusion* from *BM25 the idea*. Staked by no prediction;
reported descriptively.

The index is built in memory per process from the sandbox corpus copy and
never written anywhere (S9; read-only proof applies to this arm too).
"""
import os
import re
import sqlite3

_MD = re.compile(r"\.md$", re.IGNORECASE)
_TOKEN = re.compile(r"[\w./:-]{2,}", re.UNICODE)

_cache = {}


def _build(corpus_dir):
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE VIRTUAL TABLE docs USING fts5(path UNINDEXED, body, tokenize='porter unicode61')")
    for dirpath, dirnames, filenames in os.walk(corpus_dir):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
        for name in sorted(filenames):
            if not _MD.search(name):
                continue
            abspath = os.path.join(dirpath, name)
            rel = os.path.relpath(abspath, corpus_dir).replace(os.sep, "/")
            with open(abspath, encoding="utf-8", errors="replace") as f:
                conn.execute("INSERT INTO docs (path, body) VALUES (?, ?)", (rel, f.read()))
    conn.commit()
    return conn


def _fts_query(query):
    """FTS5 match syntax is an injection surface; queries become quoted
    OR-terms, mirroring the navigator's term extraction bound (12 terms)."""
    terms = _TOKEN.findall(query)[:12]
    quoted = ['"{}"'.format(t.replace('"', '""')) for t in terms]
    return " OR ".join(quoted) if quoted else '""'


def locate_fts5(corpus_dir, query, k=8):
    conn = _cache.get(corpus_dir)
    if conn is None:
        conn = _cache[corpus_dir] = _build(corpus_dir)
    try:
        rows = conn.execute(
            "SELECT path, bm25(docs) AS score FROM docs WHERE docs MATCH ? "
            "ORDER BY score ASC, path ASC LIMIT ?", (_fts_query(query), k)).fetchall()
    except sqlite3.OperationalError:
        rows = []
    # bm25() returns lower-is-better; negate so the envelope shape matches.
    return {
        "capability": "locate",
        "strategy": "sqlite-fts5-porter-unicode61",
        "request": {"query": query, "k": k, "retriever": "L4-external"},
        "hits": [
            {"path": path, "line": 1, "score": round(-score, 4), "retriever": "fts5"}
            for path, score in rows
        ],
    }
