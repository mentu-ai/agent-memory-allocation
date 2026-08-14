#!/usr/bin/env python3
"""C34 — rule R: the frozen public-corpus eligibility rule, self-contained.

Registered in `corpus/conjectures/c34-public-curation-vs-search-replication.md`
§1, narrowed by correction v2 C-2 (README.md named exemption = deviation D-8;
snapshot source pinned to the git TREE of cb73654) and correction v3 G5 (the
>170 ceiling branch and the <135 floor branch are DEAD — the enumeration at
cb73654 is fixed, so a single precondition assertion replaces both).

Rule R — a file is an eligible corpus member at the snapshot commit S iff:
  1. it is git-tracked in `epistemics` at S;
  2. its path ends in `.md`;
  3. its path is at the repository root, or under one of applications/,
     corpus/, docs/, essays/, instruments/, lineage/, observatory/, results/;
  4. its size is >= 2,000 bytes;
  5. it passes the client-content audit with ZERO flags;
  6. its path contains neither `c29` nor `c34`, and it is not under
     analyses/c34-public-curation-vs-search-replication/;
  and it is not a named exemption (D-8: README.md).

Clauses 1-3 define the CANDIDATE set. Clauses 4-6 and the named exemption are
the rejecting clauses, and the rejection ledger buckets by FIRST match in the
frozen order size -> audit -> selfref (-> exemption), per correction v2 C-9;
C-9 additionally requires ALL matching clauses per rejected file, so the ledger
is order-annotated rather than order-dependent. `exemption` is ordered last so
the registered 3/5/4 arithmetic is unchanged by D-8's addition.

The audit token set and the Spanish-density regex are copied VERBATIM from
`paper/agent-memory-allocation/sensitivity_audit.py` so the rule is
self-contained in the public bundle and needs no withheld file to re-run.

Reads the cb73654 TREE via git plumbing, never the working tree: nothing any
session or observatory beat wrote after the registration commit can enter the
corpus (correction v2 C-2.3).

Usage:
  python3 corpus_rule.py              # enumerate and print; WRITES NOTHING
  python3 corpus_rule.py --log        # also write the rule-R evaluation log
  python3 corpus_rule.py --snapshot   # M3: log + corpus-snapshot/ +
                                      #     corpus-manifest.json

A bare invocation is read-only by design: verification passes must be able to
re-enumerate the corpus without leaving an artifact in the study directory.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# --- frozen constants -------------------------------------------------------
SNAPSHOT_COMMIT = "cb736542a2bfc96a230e8bb9b605d11ff0b87d86"   # cb73654
ALLOWED_DIRS = ("applications/", "corpus/", "docs/", "essays/", "instruments/",
                "lineage/", "observatory/", "results/")
MIN_BYTES = 2000
NAMED_EXEMPTIONS = ("README.md",)            # deviation D-8 (correction v2 C-2.1)
STUDY_DIR = "analyses/c34-public-curation-vs-search-replication/"
CLAUSE_ORDER = ("size", "audit", "selfref", "exemption")

# Verified precondition, NOT a live branch (correction v3 G5). The <135 floor
# and >170 ceiling paths are unreachable once the snapshot source is pinned to
# the cb73654 tree, so they are not implemented; this assertion replaces both
# and fails closed on any mismatch.
EXPECTED_ACCEPTED_FILES = 141
EXPECTED_ACCEPTED_BYTES = 1_162_998

# --- client-content audit: VERBATIM from sensitivity_audit.py ---------------
# Third-party identifiers (engagement + org + personnel + product), from the
# operator's own AGENTS.md. Used ONLY to locate content for a redaction map.
CLIENT_TOKENS = []  # see redaction note below
# --- REDACTED FOR PUBLIC RELEASE (registration correction v5, 2026-08-14) ---
# The canonical CLIENT_TOKENS list is a curated enumeration of third-party
# identifiers, three of which are personal names. It is withheld from the
# public bundle; the repository copy is unchanged.
#
# Prove-same-rule: the canonical list's digest is
#   sha256(json.dumps(tokens, separators=(",", ":")).encode())
#   = 7db653bf09e813a28d0e5613fcdc2a197c39940c3c78c877cea3387c329d7c3b
# Anyone holding the canonical list can recompute that in one line and confirm
# the bundle ships the same rule.
#
# Consequence, stated plainly: with an empty token set the token half of the
# client-content audit cannot fire, so the smuggled-file dead run in
# tests/test_corpus_rule.py SKIPS in the bundle rather than passing vacuously.
# The Spanish-density half is a generic stopword list, identifies no third
# party, is NOT redacted, and still runs. Rule R's enumeration is not runnable
# from the bundle in any case: it reads the git tree at cb73654, and no git
# history ships. See registration/correction-v5.md.
CLIENT_TOKENS_SHA256 = "7db653bf09e813a28d0e5613fcdc2a197c39940c3c78c877cea3387c329d7c3b"
ES = re.compile(r"\b(que|para|con|los|las|una|está|según|equipo|"
                r"corrida|resultado|pregunta|semana|reunión)\b", re.I)

SNAPSHOT_DIR = os.path.join(HERE, "corpus-snapshot")
MANIFEST = os.path.join(HERE, "corpus-manifest.json")
EVAL_LOG = os.path.join(HERE, "rule-R-evaluation-log.json")


def audit(raw):
    """Client-content audit over raw bytes. Counts and flags only; never
    returns matched client content (sensitivity_audit.py's discipline)."""
    text = raw.decode("utf-8", errors="replace")
    low = text.lower()
    token_hits = len([t for t in CLIENT_TOKENS if t in low])
    es_hits = len(ES.findall(text))
    es_dense = es_hits >= 20     # operational-Spanish density, not a stray word
    return {"client_token_hits": token_hits, "es_hits": es_hits,
            "es_dense": es_dense, "flag": bool(token_hits) or es_dense}


# --- the clauses ------------------------------------------------------------
def is_candidate(rp):
    """Clauses 2 and 3 (clause 1 holds by construction: we read a git tree)."""
    if not rp.endswith(".md"):
        return False
    if "/" not in rp:
        return True                              # repository root
    return rp.startswith(ALLOWED_DIRS)


def clause_size(size):
    return size < MIN_BYTES


def clause_selfref(rp):
    low = rp.lower()
    return ("c29" in low) or ("c34" in low) or low.startswith(STUDY_DIR)


def evaluate(rp, size, raw):
    """Ledger entry for one candidate. `rejected_by` is the first matching
    clause in the frozen order; `matching_clauses` is all of them (C-9)."""
    a = audit(raw)
    matched = []
    if clause_size(size):
        matched.append("size")
    if a["flag"]:
        matched.append("audit")
    if clause_selfref(rp):
        matched.append("selfref")
    if rp in NAMED_EXEMPTIONS:
        matched.append("exemption")
    primary = next((c for c in CLAUSE_ORDER if c in matched), None)
    return {"path": rp, "size": size, "accepted": primary is None,
            "rejected_by": primary, "matching_clauses": matched,
            "client_token_hits": a["client_token_hits"],
            "es_hits": a["es_hits"],
            "sha256": hashlib.sha256(raw).hexdigest()}


# --- git plumbing over the pinned tree --------------------------------------
def tree_entries(commit=SNAPSHOT_COMMIT, repo=REPO):
    """[(path, blob_sha, size)] for every blob in the commit's tree."""
    out = subprocess.run(
        ["git", "-C", repo, "ls-tree", "-r", "-l", "-z", commit],
        capture_output=True, text=True, check=True).stdout
    entries = []
    for rec in out.split("\0"):
        if not rec:
            continue
        meta, path = rec.split("\t", 1)
        _mode, otype, sha, size = meta.split()
        if otype != "blob":
            continue
        entries.append((path, sha, int(size)))
    return entries


def read_blobs(shas, repo=REPO):
    """{sha: bytes} via one `git cat-file --batch` process."""
    if not shas:
        return {}
    proc = subprocess.run(["git", "-C", repo, "cat-file", "--batch"],
                          input="\n".join(shas).encode(),
                          stdout=subprocess.PIPE, check=True)
    buf, pos, blobs = proc.stdout, 0, {}
    for _ in shas:
        nl = buf.index(b"\n", pos)
        sha, _otype, size = buf[pos:nl].split()
        size = int(size)
        start = nl + 1
        blobs[sha.decode()] = buf[start:start + size]
        pos = start + size + 1               # trailing newline after the blob
    return blobs


def enumerate_corpus(commit=SNAPSHOT_COMMIT, repo=REPO):
    """Run rule R over the commit's tree. Returns (accepted, ledger, summary).

    `accepted` is [{path, size, sha256, bytes}] in ascending path order.
    """
    entries = tree_entries(commit, repo)
    candidates = [(p, s, n) for (p, s, n) in entries if is_candidate(p)]
    blobs = read_blobs(sorted({s for (_p, s, _n) in candidates}), repo)
    ledger, accepted = [], []
    for path, sha, size in sorted(candidates):
        raw = blobs[sha]
        e = evaluate(path, size, raw)
        ledger.append(e)
        if e["accepted"]:
            accepted.append({"path": path, "size": size,
                             "sha256": e["sha256"], "bytes": raw})
    buckets = {c: sum(1 for e in ledger if e["rejected_by"] == c)
               for c in CLAUSE_ORDER}
    summary = {
        "snapshot_commit": commit,
        "tree_blobs": len(entries),
        "candidates": len(candidates),
        "non_candidates_clause_2_or_3": len(entries) - len(candidates),
        "accepted_files": len(accepted),
        "accepted_bytes": sum(a["size"] for a in accepted),
        "rejected_by_clause": buckets,
    }
    return accepted, ledger, summary


def assert_precondition(summary):
    """Verified precondition in place of the dead <135 / >170 branches
    (correction v3 G5). Fails closed."""
    got = (summary["accepted_files"], summary["accepted_bytes"])
    want = (EXPECTED_ACCEPTED_FILES, EXPECTED_ACCEPTED_BYTES)
    if got != want:
        raise SystemExit(
            "CORPUS PRECONDITION FAILED: rule R at "
            f"{summary['snapshot_commit'][:7]} yields {got[0]} files / "
            f"{got[1]} bytes; registered precondition is {want[0]} files / "
            f"{want[1]} bytes (correction v3 G5). The corpus is pinned to a "
            "fixed tree, so any mismatch is an instrument fault, not a "
            "corpus change. Stopping before any provider call.")


def write_snapshot(accepted):
    """M3: copy the full bytes of every eligible file, preserving relative
    paths, and write corpus-manifest.json."""
    import shutil
    if os.path.isdir(SNAPSHOT_DIR):
        shutil.rmtree(SNAPSHOT_DIR)
    manifest = []
    for a in accepted:
        dest = os.path.join(SNAPSHOT_DIR, a["path"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(a["bytes"])
        manifest.append({"path": a["path"], "size": a["size"],
                         "sha256": a["sha256"]})
    with open(MANIFEST, "w") as fh:
        json.dump({"snapshot_commit": SNAPSHOT_COMMIT,
                   "files": len(manifest),
                   "bytes": sum(m["size"] for m in manifest),
                   "entries": manifest}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", action="store_true",
                    help="write the rule-R evaluation log")
    ap.add_argument("--snapshot", action="store_true",
                    help="M3: write corpus-snapshot/ and corpus-manifest.json "
                         "(implies --log)")
    args = ap.parse_args()

    accepted, ledger, summary = enumerate_corpus()
    assert_precondition(summary)
    print(json.dumps(summary, indent=1, sort_keys=True))
    if args.log or args.snapshot:
        with open(EVAL_LOG, "w") as fh:
            json.dump({"rule": "R", "summary": summary,
                       "clause_order": list(CLAUSE_ORDER),
                       "named_exemptions": list(NAMED_EXEMPTIONS),
                       "candidates": ledger}, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print(f"evaluation log -> {EVAL_LOG}")
    if args.snapshot:
        m = write_snapshot(accepted)
        print(f"snapshot: {len(m)} files -> {SNAPSHOT_DIR}")


if __name__ == "__main__":
    sys.exit(main())
