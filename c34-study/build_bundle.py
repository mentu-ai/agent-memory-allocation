#!/usr/bin/env python3
"""C34 — assemble the public bundle (M8, registration §Release binding).

Copies every artifact the registration commits to shipping into one tree a
reader can hold in full, writes BUNDLE-MANIFEST.json (path + size + sha256 for
every file), and runs the client-content audit over the ASSEMBLED bundle as
the last gate before release.

Design note, stated because it is a judgment call: the bundle is BUILT rather
than committed. Every byte in it is already committed in this repository, and
copying 141 snapshot files plus 390 run records into a second tracked tree
would create a duplicate source of truth that could drift from the first. What
is committed instead is this script, the manifest with its hashes, the bundle
README, and the audit report — which together make the bundle reproducible and
verifiable without storing it twice. `--out` defaults outside the repository
for the same reason.

Usage:
  python3 build_bundle.py                    # assemble + audit + manifest
  python3 build_bundle.py --out DIR
  python3 build_bundle.py --verify DIR       # re-verify an assembled bundle
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys

import corpus_rule as R

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DEFAULT_OUT = os.path.join("/private/tmp/claude-501", "c34-public-bundle")

# What ships, per registration §Release binding. (source, bundle destination)
STUDY_FILES = (
    "corpus_rule.py", "harness_lib.py", "generate_questions.py",
    "build_index.py", "run_policies.py", "adjudicate.py", "audit_smoke.py",
    "run_tests.py", "build_bundle.py", "expected-artifacts.json",
    "CONVENTIONS.md", "BUNDLE-README.md",
    "NOTE-M2-2026-08-13.md", "NOTE-M3-2026-08-13.md",
    "corpus-manifest.json", "rule-R-evaluation-log.json",
    "questions-2026-08-13.json", "selection-2026-08-13.json",
    "index-2026-08-13.json", "reality-probe.json",
    "call-ledger.jsonl", "call-ledger.jsonl.head.json",
    "smoke-audit-2026-08-13.json", "effect-table-2026-08-14.json",
)
STUDY_DIRS = ("corpus-snapshot", "runs", "gen-cache", "tests")
REPO_FILES = (
    ("corpus/conjectures/c34-public-curation-vs-search-replication.md",
     "registration/conjecture-c34.md"),
    ("instruments/2026-08-12-c34-public-corpus-replication-instrument.md",
     "registration/instrument-note-2026-08-12.md"),
    ("docs/BUILD-c34-public-curation-vs-search-replication-v1.md",
     "registration/BUILD-v1.md"),
    ("instruments/2026-08-13-c34-registration-correction-v2.md",
     "registration/correction-v2.md"),
    ("instruments/2026-08-13-c34-registration-correction-v3.md",
     "registration/correction-v3.md"),
    ("instruments/2026-08-13-c34-registration-correction-v4.md",
     "registration/correction-v4.md"),
    ("instruments/2026-08-13-c34-correction-v4-erratum-1.md",
     "registration/correction-v4-erratum-1.md"),
    ("instruments/2026-08-14-c34-registration-correction-v5.md",
     "registration/correction-v5.md"),
    ("results/2026-08-14-c34-public-curation-vs-search-replication.md",
     "RESULTS.md"),
)


# --- redaction, registered by correction v5 (2026-08-14) -------------------
# The bundle's copies of three files differ from the repository's, and only
# these three. Each carries a client-identifier literal that makes the file
# fail the very audit it defines. The repository's copies are untouched.
CANONICAL_TOKENS_SHA256 = hashlib.sha256(
    json.dumps(R.CLIENT_TOKENS, separators=(",", ":")).encode()).hexdigest()

REDACTION_NOTE = f'''
# --- REDACTED FOR PUBLIC RELEASE (registration correction v5, 2026-08-14) ---
# The canonical CLIENT_TOKENS list is a curated enumeration of third-party
# identifiers, three of which are personal names. It is withheld from the
# public bundle; the repository copy is unchanged.
#
# Prove-same-rule: the canonical list's digest is
#   sha256(json.dumps(tokens, separators=(",", ":")).encode())
#   = {CANONICAL_TOKENS_SHA256}
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
CLIENT_TOKENS_SHA256 = "{CANONICAL_TOKENS_SHA256}"
'''


def redact_corpus_rule(text):
    """Replace the token list with an empty one plus the verifying digest."""
    start = text.index("CLIENT_TOKENS = [")
    end = text.index("]", start) + 1
    return (text[:start] + "CLIENT_TOKENS = []  # see redaction note below"
            + REDACTION_NOTE + text[end + 1:])


MARKER = "REDACTED-CLIENT-IDENTIFIER"


def redact_all_tokens(text, require=True):
    """Redact every canonical client token appearing in the text, matched
    case-insensitively.

    The tokens are read from the canonical list rather than written here: a
    redactor that spells out what it redacts fails the same audit as the file
    it is redacting. That is not hypothetical — the first version of this
    module hardcoded two of them and was itself flagged by the release gate.
    """
    hits = 0
    for token in R.CLIENT_TOKENS:
        text, n = re.subn(re.escape(token), MARKER, text, flags=re.I)
        hits += n
    if require and hits == 0:
        raise SystemExit("REDACTION FAILED: no client token found to redact")
    return text


REDACTIONS = {
    "corpus_rule.py": lambda t: redact_all_tokens(redact_corpus_rule(t),
                                                  require=False),
    "tests/test_corpus_rule.py": redact_all_tokens,
    "tests/test_harness_lib.py": redact_all_tokens,
}


def apply_redaction(rel, dst):
    fn = REDACTIONS.get(rel)
    if fn is None:
        return False
    with open(dst, encoding="utf-8") as fh:
        text = fh.read()
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(fn(text))
    return True


def copy_tree(src, dst):
    n = 0
    for root, _dirs, files in os.walk(src):
        for name in sorted(files):
            if name.endswith(".pyc") or "__pycache__" in root:
                continue
            s = os.path.join(root, name)
            d = os.path.join(dst, os.path.relpath(s, src))
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            n += 1
    return n


def assemble(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    n = 0
    for name in STUDY_FILES:
        src = os.path.join(HERE, name)
        if not os.path.exists(src):
            raise SystemExit(f"BUNDLE INCOMPLETE: missing {name}")
        shutil.copy2(src, os.path.join(out, name))
        n += 1
    for name in STUDY_DIRS:
        src = os.path.join(HERE, name)
        if not os.path.isdir(src):
            raise SystemExit(f"BUNDLE INCOMPLETE: missing {name}/")
        n += copy_tree(src, os.path.join(out, name))
    for src_rel, dst_rel in REPO_FILES:
        src = os.path.join(REPO, src_rel)
        if not os.path.exists(src):
            raise SystemExit(f"BUNDLE INCOMPLETE: missing {src_rel}")
        d = os.path.join(out, dst_rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(src, d)
        n += 1
    applied = [rel for rel in sorted(REDACTIONS)
               if apply_redaction(rel, os.path.join(out, rel))]
    if applied != sorted(REDACTIONS):
        raise SystemExit(f"REDACTION INCOMPLETE: applied {applied}")
    print(f"redacted (correction v5): {applied}")
    return n


def manifest(out):
    entries = []
    for root, _dirs, files in os.walk(out):
        for name in sorted(files):
            if name == "BUNDLE-MANIFEST.json":
                continue
            p = os.path.join(root, name)
            with open(p, "rb") as fh:
                raw = fh.read()
            entries.append({"path": os.path.relpath(p, out),
                            "size": len(raw),
                            "sha256": hashlib.sha256(raw).hexdigest()})
    entries.sort(key=lambda e: e["path"])
    return {"files": len(entries),
            "bytes": sum(e["size"] for e in entries),
            "entries": entries}


def audit_bundle(out):
    """The last gate before release: the client-content audit over the
    ASSEMBLED bundle, not over the source tree (BUILD M8)."""
    flagged = []
    for e in manifest(out)["entries"]:
        with open(os.path.join(out, e["path"]), "rb") as fh:
            raw = fh.read()
        a = R.audit(raw)
        if a["flag"]:
            flagged.append({"path": e["path"],
                            "client_token_hits": a["client_token_hits"],
                            "es_hits": a["es_hits"]})
    return flagged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--verify", metavar="DIR",
                    help="re-verify an already-assembled bundle")
    args = ap.parse_args()
    out = args.verify or args.out
    if not args.verify:
        n = assemble(out)
        print(f"assembled {n} files -> {out}")
    man = manifest(out)
    with open(os.path.join(out, "BUNDLE-MANIFEST.json"), "w") as fh:
        json.dump(man, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"manifest: {man['files']} files, {man['bytes']:,} bytes")
    flagged = audit_bundle(out)
    if flagged:
        print(f"CONFIDENTIALITY AUDIT FAILED: {len(flagged)} flagged file(s)")
        for f in flagged[:20]:
            print(f"  {f['path']}  tokens={f['client_token_hits']} "
                  f"es={f['es_hits']}")
        return 1
    print(f"confidentiality audit: SILENT — 0 of {man['files']} files flagged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
