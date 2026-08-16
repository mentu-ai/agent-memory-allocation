# Finding More, Fusing Less — replication bundle (v1)

Companion study to "Reading More, Finding Less" (doi:10.5281/zenodo.21960138).
This record: doi:10.5281/zenodo.21969901. Verdict: revised (P1 pass +13.9pp,
P2 fusion FAIL -7.8pp -> RRF default retired by pre-registered rule).

- `locator-bakeoff-v1.pdf` / `paper-v1.md` — the report.
- `c36-locator-bakeoff/` — frozen harness, gated question set (115,
  sha256 b8f12a5b…), generation log + candidate cache, all run records
  (localization all arms; downstream L0/L2), metrics, mechanical
  adjudicator + its output, FREEZE + three dated corrections.
- `registration-lineage/` — conjecture (predictions frozen before any
  question existed), registration, question-regeneration protocol,
  adjudicated result document.
- `validation/` — the two isolated Claude-session validation kits
  (prompts + byte manifests), their complete exports and final JSON
  returns, and the dated disposition of all findings.
- `corpus-manifest.json` — sha256 manifest of the 141-document corpus
  snapshot; the snapshot itself is published in the parent deposit.

Re-run: verify the corpus against the manifest, then
`python3 c36-locator-bakeoff/tests/test_c36.py` (freeze tests),
`run_arms.py a` / `run_arms.py b`, `adjudicate_c36.py`.
Contact: rashid@mentu.ai
