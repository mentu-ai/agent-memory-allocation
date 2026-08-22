# Reading More, Finding Less: release bundle

*Reading More, Finding Less: A Pre-Registered Anatomy of Progressive
Disclosure for AI Agents*. Rashid Azarang, Independent Researcher.
Preprint, 2026-08-16. DOI
[10.5281/zenodo.21960138](https://doi.org/10.5281/zenodo.21960138); the
concept DOI
[10.5281/zenodo.21938412](https://doi.org/10.5281/zenodo.21938412)
resolves to the current version.

## Companion study (2026-08-16)

**Finding More, Fusing Less: A Pre-Registered Locator Bake-off for AI
Agents**. DOI
[10.5281/zenodo.21969901](https://doi.org/10.5281/zenodo.21969901),
mirrored here under [`c36-locator-bakeoff/`](c36-locator-bakeoff/).
It tests the constructive converse of this paper: whether the search
arm's own miss ceiling is reducible by ranked retrieval. Verdict:
**revised**. BM25 beat exact search by +21.7 pp on localization, but
the pre-registered fusion prediction failed (-7.8 pp vs BM25-alone) and
the shipped RRF default was retired by rule. Full harness, gated
question set, run records, mechanical adjudicator, and the independent
validation sessions ship in that directory.

## What is here

| File | What it is |
|---|---|
| `agent-memory-allocation.pdf` | the preprint, typeset (30 pp) |
| `paper.html` | the same text as a single self-contained page |
| `paper.md` | the canonical markdown the renders are built from |
| `fig1_misrouting.png`, `fig2_c29_policies.png` | the two figures |
| `references.bib` | full BibTeX for the reference list |
| `c34-study/` | the public replication in full: corpus snapshot, frozen questions, index, harness, adjudicator, run records, results, tests, registration chain, and `ORDER-PROOF.md` (the commit chain exported for bundle-only readers) |
| `repro-kit/` | the C29 public demonstrator: harness, 17 operator-owned English methodology documents, frozen public question set, reference result (see the paper's §10 and §8 Limits (b′) for what it does and does not establish) |

## One note on the corpus snapshot

`c34-study/corpus-snapshot/` contains the 141 documents the replication
measured, snapshotted at the byte and pinned in
`corpus-manifest.json`. Files inside it with configuration-sounding names
(`CLAUDE.md`, `AGENTS.md`, and similar) are **measured corpus
documents**, not configuration of this bundle: the frozen questions are
about them, the gold answers are substrings of them, and the adjudicator
recomputes generation-input hashes from them. Removing any of them breaks
the manifest, the questions, and the replay.

## Where to start

`c34-study/` is a complete empirical study you can re-run: 141 releasable
documents, 120 frozen confirmatory questions with gold answers, the
one-line-digest index (model-written under the committed prompt, as the
paper's §3 states), all 390 run records with per-attempt logs, the full
registration chain, and the harness, adjudicator, and test suite. The paper's
§4 anatomy derives from a withheld production corpus and re-derives
descriptively from this bundle's records (§5); §5 re-derives from
`c34-study/` entirely.

### Re-running the adjudicator from a clone

The adjudicator is deterministic over the committed run records and reproduces
`effect-table-2026-08-14.json` byte for byte. From a clone of this repository
it needs one extra step, for a reason worth stating plainly.

```sh
cd c34-study
mkdir -p /tmp/c34 && cp questions-2026-08-13.json /tmp/c34/
python3 adjudicate.py --questions /tmp/c34/questions-2026-08-13.json \
                      --out /tmp/c34/replay.json
diff effect-table-2026-08-14.json /tmp/c34/replay.json   # empty
```

The adjudicator carries a contamination check that asks whether any run
started before the question set was frozen. It reads the freeze time from the
git commit that first added `questions-2026-08-13.json`. In the private
research repository that commit is the real freeze, on 2026-08-13, and every
run postdates it. This public repository is an export: its first commit added
the whole bundle at once, on 2026-08-14, after the runs had already happened.
Run against the export's own git metadata, the check therefore reports all 360
records as predating the freeze and returns `verdict: void`,
`question_set_contamination`.

That is the check misreading an export date as a freeze date. It is not a
finding about the study. Reading the question set from outside the checkout,
as above, leaves the freeze time undetermined, the check stands down, and the
adjudication runs on the committed records as it did originally: verdict
`revised`, sha256
`e73c072fcf1c29d699d998dc5d87f726a76dc4583bd6d6e9d05c5af7ce46c83b`.

The real ordering evidence for bundle-only readers is
`c34-study/ORDER-PROOF.md`, which exports the commit chain with author
timestamps. The question set froze at 2026-08-13T18:03:32-06:00 and the first
policy-run provider call is 2026-08-14T01:07:02Z. The call ledger's hash chain
in `call-ledger.jsonl` cross-checks it.

### Running the tests

```sh
cd c34-study && python3 run_tests.py
```

193 tests. From a clone, expect one failure and two errors, all three in
`test_corpus_rule.py` and `test_leak_gate.py`, and all three from the same
cause: `corpus_rule.py` enumerates the corpus by reading a pinned git tree
(`cb73654`) from the private research repository. That tree is not in this
export, so those tests cannot run here. The corpus they would rebuild ships
directly as `c34-study/corpus-snapshot/`, pinned by sha256 in
`corpus-manifest.json`, which is checkable without git.
