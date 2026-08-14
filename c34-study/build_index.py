#!/usr/bin/env python3
"""C34 — policy C's materialized index (M4; a SEPARATE committed pass from
question generation, per the registration's exposure rule 2).

Per corpus file: relative path + one-line digest. The digest is the file's own
frontmatter `summary`/`description`/`title` where mechanically extractable
(free), else a generator-authored one-liner (charged to policy C's authoring
ledger). Authoring cost is reported both amortized and unamortized, carried
from C29 D5 and registration §3.

The generator sees frontmatter-stripped bodies here too, and never sees a
question. Digest authoring and question generation are separate passes so no
call can carry both.

Usage: python3 build_index.py
"""
import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import harness_lib as H
from generate_questions import S_PROMPT, cached, cached_keys

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-08-13"
I_OUT = os.path.join(HERE, f"index-{DATE}.json")
DIGEST_INPUT_CHARS = 6000        # carried verbatim from C29 generate_questions


def author_one(rp, ledger):
    _fm, body = H.strip_frontmatter(H.read_snapshot(rp))
    sent = body.strip()[:DIGEST_INPUT_CHARS]
    rec = H.run_claude(S_PROMPT.format(rp=rp, body=sent), H.GENERATOR,
                       ledger=ledger, bucket="digest", key=f"digest:{rp}")
    lines = (rec.get("result_text") or "").strip().splitlines()
    return {"digest": (lines[0][:200] if lines else ""),
            "tokens": rec.get("tokens_total", 0),
            "cost_usd": rec.get("cost_usd") or 0.0,
            "input_sha256": hashlib.sha256(sent.encode("utf-8")).hexdigest()}


def index_text(index):
    """The exact block interpolated into C_PROMPT — one line per file, in
    ascending path order (C29's `sorted(index.items())`)."""
    return "\n".join(f"{rp} — {v['digest']}" for rp, v in sorted(index.items()))


def main():
    man = H.load_manifest()
    paths = sorted(e["path"] for e in man["entries"])
    if len(paths) != H.EXPECTED_CORPUS_FILES:
        raise SystemExit(
            f"CORPUS PRECONDITION FAILED: {len(paths)} snapshot files, "
            f"expected {H.EXPECTED_CORPUS_FILES} (correction v3 G5).")

    ledger = H.CallLedger()
    ledger.discover(cached_keys())

    index, to_author = {}, []
    for rp in paths:
        fm, _body = H.strip_frontmatter(H.read_snapshot(rp))
        d = H.digest_from_frontmatter(fm) if fm else None
        if d:
            index[rp] = {"digest": d, "source": "frontmatter"}
        else:
            to_author.append(rp)

    tokens = cost = 0
    with ThreadPoolExecutor(8) as ex:
        for rp, rec in zip(to_author, ex.map(
                lambda rp: cached("digest", f"digest:{rp}",
                                  lambda rp=rp: author_one(rp, ledger)),
                to_author)):
            index[rp] = {"digest": rec["digest"], "source": "authored",
                         "input_sha256": rec["input_sha256"]}
            tokens += rec["tokens"]
            cost += rec["cost_usd"]

    with open(I_OUT, "w") as fh:
        json.dump({"generator": H.GENERATOR,
                   "snapshot_commit": man["snapshot_commit"],
                   "files": len(index),
                   "frontmatter_n": len(index) - len(to_author),
                   "authored_n": len(to_author),
                   "authoring_tokens_total": tokens,
                   "authoring_tokens_note": "per-call totals incl. nested-CLI "
                   "system-prompt overhead (mostly cache reads) — same "
                   "accounting as policy runs, symmetric by design",
                   "authoring_cost_usd": round(cost, 4),
                   "index": index}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(I_OUT, "rb") as fh:
        print(os.path.basename(I_OUT),
              hashlib.sha256(fh.read()).hexdigest()[:16])
    print(f"files={len(index)} frontmatter={len(index) - len(to_author)} "
          f"authored={len(to_author)} authoring_tokens={tokens}")


if __name__ == "__main__":
    sys.exit(main())
