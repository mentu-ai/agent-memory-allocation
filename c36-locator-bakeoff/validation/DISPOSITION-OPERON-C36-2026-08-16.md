# Disposition — Operon-c36 v1 returns (2026-08-16)

Both sessions completed and exported per custody rules (Session V root
status `completed` 19:43:03Z; Session L `completed` 19:59:50Z). Raw
exports, the validator's recomputation CSV, and both final JSON objects
are archived under `operon-c36/returns/`.

**Session V overall: `validated-with-findings`.** 22 recomputation rows,
21 exact matches; the validator applied the frozen verdict mapping to its
own recomputed values and confirmed **`revised` follows**. The verdict
stands untouched. Every defect below is adjudicated adopt/decline; none
alters any adjudicated number or the verdict — they bind the companion
paper's text and the successor designs.

## Session V defects

| # | Class / severity | Disposition |
|---|---|---|
| D1 | CLAIM_MISMATCH / minor — P4's +147.4 ms not exactly reproducible (validator: 147.5 difference-of-medians, 148.2 median-of-paired-differences) | **Adopt.** Estimator ambiguity, not an error: the recorded value is `median(L2)−median(L0)` on unrounded floats. All estimators agree within 1.4 ms against a 500 ms bound (357×–338× margin). Paper states the estimator explicitly. |
| D2 | DISCLOSURE_GAP / material — registration §5 measures not fully delivered: marginal tokens absent (only `prompt_chars`), index-build peak RSS absent from metrics, cross-language subset measurement absent | **Adopt.** True and undisclosed until now. Paper's limitations section names all three; `prompt_chars` is reported as the token proxy it is; the cross-language subset is vacuously empty (same fact as P3's n = 0) and stated as such; the D3-trigger check on it is recorded as not evaluable on this corpus. No adjudicated quantity involved. |
| D3 | DISCLOSURE_GAP / material — no uncertainty statements; the FTS5 +3.4 pp margin is **not significant** while the narrative called it "a real but modest margin" | **Adopt, with thanks.** The validator's exact McNemar tests enter the paper as descriptive statistics: P1 17-vs-1 discordant, p = 0.00014; P2 2-vs-11, p = 0.0225; L1-vs-L0 28-vs-3, p < 1e-5. The FTS5 comparison is restated as "not statistically distinguishable from the FTS5 control on this n." The frozen results document is not edited; this disposition is the dated correction of its narrative claim 3. |
| D4 | DISCLOSURE_GAP / minor — "fully accounted for by localization" overclaims; decomposition is +7.47 pp localization − 2.25 pp conditional-accuracy | **Adopt.** The paper reports the decomposition: the gain is localization-driven and partly offset by a small conditional-accuracy decline (53.7% → 50.0% given located). |
| D5 | DISCLOSURE_GAP / minor — premature-adjudication incident unfalsifiable from the attached records | **Adopt as boundary.** The incident's evidence (task logs, discarded output) lives in the session record, not the bundle. The paper carries the disclosure with its unfalsifiability stated; the successor fix — the adjudicator asserting P5 denominator completeness before computing — is a registered design requirement for any follow-up study. |
| D6 | RECORD_INCONSISTENCY / minor — q105/q106 share the gold string "Claude Code 2.1.220" across different gold documents; P5 scoring cannot distinguish which document was reached for those two | **Adopt.** Disclosed as an instrument note (symmetric across arms; localization is path-based and unaffected; worst-case P5 effect is 2/115 per arm). Successor gate: gold strings unique across accepted questions. |
| D7 | INSTRUMENT_CONTRADICTION / material — L2 hit lists not reconstructible from the truncated top-8 legs | **Adopt as documentation.** Expected consequence of recording only top-8 per leg while fusion runs over full rank lists; the validator itself notes it is not evidence of error. Successor requirement: record legs to fusion depth so the fusion is externally replayable. |

Unverifiable boundaries (10 listed by the validator — corpus hashes,
navigator build, model identity, commit ordering, machine self-report):
all acknowledged; they are exactly the repro-bundle's job. The public
deposit ships the corpus manifest, harness, and pinned code so an external
runner can close every one of them; the paper lists them verbatim as the
validation's limits.

## Session L adoption

13/13 works verified live, zero failed verifications. The
`recommended_confrontations` list (Cormack 2009; Bruch TOIS 2023;
2508.01405; 2603.02153; 2608.05886; RAGGED 2403.09040; 2606.22417;
2503.09089 + 2503.01763; BEIR; 2605.15184 + 2608.01507) is **adopted as
mandatory** for the related-work section. The novelty framing is adopted
verbatim in substance:

- Finding (i): novel-on-substrate, not novel-in-kind; scoped to
  localization recall (CodeGrep's precision-threshold bound cited).
- Finding (ii): the phenomenon is occupied; **the pre-registered,
  mechanically adjudicated retirement of a shipped default is the claim**;
  the unswept RRF k = 60 is conceded as a live confound.
- Finding (iv): presented as a third convergent replication, with RAGGED
  confronted as the strongest counter-framing.
- The verified gap — no empirical pre-registered retrieval-composition
  study for agents exists — is the paper's positioning slot.

## Consequence

Paper build **unblocked** under these bindings. Two additions to the
successor queue: (a) RRF parameter sweep + rank-aware exact leg under
fresh registration; (b) gold-uniqueness gate and fusion-depth recording
in any follow-up harness.
