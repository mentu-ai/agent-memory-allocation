# B2v2 — Reproducibility re-referee (confirmation pass)

**Paper:** `paper/return-base-rate-paper.md` (Draft **v1.2**, 2026-07-04)
**Lens:** reproducibility only — can an external reader re-derive every number from what the paper states, and does provenance/data-availability now cover the artifacts?
**Method:** v1.2 read in full (esp. §2, §3, §4, §5, §6, Data and code availability, Provenance). Cross-checked **statically** against the regenerated `paper/stage0_robustness.json`, the re-derivation instrument `instruments/2026-07-04-return-baseline-rederivation.py`, and `paper/figs.py`. Prior report `docs/referee/B2-repro.md` and resolution claims `docs/escalations/2026-07-04-return-base-rate-B2.md` used as the checklist. **The instrument was NOT executed against `~/.mentu`** (per hard rule); snapshot values are read from the instrument's own hardcoded notes + escalation B5. Numbers treated as frozen — traced, never recomputed.

**Bottom line:** every blocker and nearly all majors/minors are genuinely resolved, and the Stage-0 numbers now reconcile exactly across body / figure-data / figure script. But the snapshot-pinning fix (resolving old B2) was **over-generalized in the provenance**: two headline corroborating numbers (1,847 patterns; 76 contradictions) are cited as coming from the pinned 2026-07-04 snapshot, where the instrument's own notes say the values are different (2,004 / >76). And Figure 4 still renders the **superseded** "≥10×" P1. These are new trace/consistency regressions, below.

---

## 1. Prior-finding disposition

### Blockers

**B1 — no data/code availability statement → RESOLVED.**
A dedicated section now exists: *"## Data and code availability … the production trust-state store and hash-chained ledger are proprietary and are not released. To make the results verifiable without them, we publish: (a) the cryptographic digest and row count of the offer-experiment snapshot … (b) the collection and analysis scripts … (c) the frozen figure-data JSONs backing Figures 1–4."* The proprietary stance is stated explicitly and the released set is enumerated.

**B2 — SQLite store had no digest / no snapshot / live mutating file → RESOLVED.**
The store is now pinned and digested: *"computed against a single pinned snapshot produced by `sqlite3 -readonly \".backup\"` (sha256 `0b320d9d…`, 2,271,764,480 bytes, `PRAGMA integrity_check = ok`)."* Digest, byte size, and integrity check all match `stage0_robustness.json` (`0b320d9d3d66…`, `2271764480`, `"ok"`). Live-file hazard is disclosed: *"the live store continues to mutate … and is never queried without snapshotting."*
*Residual (minor):* the paper does not quote `PRAGMA user_version` (the instrument records it) and gives no single as-of instant for the *historical* 409,404 read (that read predates the pinned snapshot). The invariance framing (below) makes this survivable, but the user_version is a cheap add.

**B3 — "pattern non-reuse = true zero" → RESOLVED.**
Demoted throughout. §4: *"We report this as a floor rather than a confirmed zero: the reuse-detection channel is the same class of model-trace instrument shown to fail silently at Stage 2 … and the C9 readiness gate … is not yet met."* Abstract (*"show no detected downstream reuse"*), Fig 2b caption (*"none show **detected** downstream reuse — a floor"*), and `figs.py` (*"no detected reuse (floor)"*) all agree. The §8 contradiction is gone.

### Majors

**M1 — body denominators disagreed with figure data → RESOLVED.**
The orphan `424,304` is gone. Body §3 now quotes *"0.0232% as-of the frozen instant, 0.0222% at the frozen read, 0.0210% on the later snapshot's 433,155 trust-state rows, 0.0203% against all 447,709 signals."* These match `stage0_robustness.json` `robustness_rows` exactly (392,947 / 409,404 / 433,155 / 447,709 → 0.0232 / 0.0222 / 0.0210 / 0.0203) and `figs.py` fig1(b) (`denoms = ["/392,947","/409,404","/433,155","/447,709"]`, `rates = [0.0232,0.0222,0.0210,0.0203]`). Arithmetic verified: 91/392,947 = 0.0232%, 91/409,404 = 0.0222%, 91/433,155 = 0.0210%, 91/447,709 = 0.0203%.
*Minor:* the body states the 392,947 denominator only implicitly ("as-of the frozen instant") — the other three are printed. Harmless.

**M2 — "accessed/context_used/cited" undefined → RESOLVED.**
Inline now: *"'accessed' is a recorded access against the row in the operational store (`access_count > 0`), written by the engine independent of any model output; 24 `context_used` events (`event_type = 'context_used'`)"* and Stage 2 *"6 cite prior evidence (`use_rate > 0`)."* All three predicates match the instrument (`WHERE access_count>0`; `event_type='context_used'`; `use_rate>0`).

**M3 — Stage-1 arm filter unspecified → RESOLVED.**
§3: *"24 runs were in the injected arm, 21 in the withheld arm — feature-class runs (i.e. excluding `fixture`, `smoke`, and `infra` run classes) started after the 2026-06-15T02:57:24Z footer-fix boundary."* Matches the instrument's baseline filter (`C1B_FOOTER_FIX <= started(r) < INTERVENTION and run_class(r) not in {fixture,smoke,infra}`). The `run_class()` name-heuristic lives in the released instrument, and the fix date disambiguates the 2026-06-15 boundary from the 2026-07-01 diagnostic.

**M4 — decay figures: no script, no snapshot, 217,629 vs 409,404 → PARTIAL.**
The reconciliation is done and correct: §4 *"the C3/C3a decay analysis is computed on an earlier corpus snapshot, 2026-06-10, with 217,629 trust-state rows, and is not pooled with the 2026-06-29 funnel snapshot."* Provenance attributes it honestly to *"the frozen C3/C3a analysis (2026-06-10 snapshot)."* **Still open:** the 2026-06-10 decay snapshot carries **no digest** (unlike the pinned cir.db), "effective/asserted confidence" and the "decayed" predicate are not defined inline, and `n=1,964` is not verifiable from any provided artifact (the escalation itself defers this: *"Confirm n=1,964 against the C3a source at final proof"*). Decay is the least-provenanced surviving finding.

**M5 — "2 resolved" via undocumented semantics vs "observatory verbatim" overclaim → RESOLVED (with residual).**
The blanket claim is scoped: §2 now says only Stages 1–3 use *"the observatory's canonical semantics,"* and *"the contradiction 'resolved' count … counts genuine resolutions rather than backfilled `resolved_at` timestamps"* is flagged as analysis-specific. The count is traceable: the instrument computes both `resolved_at IS NOT NULL` and `resolution IS NOT NULL` and notes *"both resolved semantics agree at 2 on current data."*
*Residual (minor):* "genuine resolution" is still not given an exact predicate in the paper (it is `resolution IS NOT NULL` per the instrument); a reader can't know that without the script.

**M6 — `observatory/collect.py` unresolvable → RESOLVED (contingent on release).**
Data availability commits to releasing *"`observatory/collect.py` for the funnel semantics and the `analyses/{…}/` trees."* Resolves once the release actually ships (same contingency as B1).

**M7 — hash-chain integrity not reproducible; 98.97% arithmetic → PARTIAL.**
The **arithmetic defect is fully resolved**: the derived "98.97% intact" percentage is **dropped**; §2 now reports only consistent counts — *"a 100% content-integrity check (11,106/11,106) … 109 are breaks and 108 of those coincide exactly with a workspace-context switch … with 1 residual break … none are content-hash failures."* The residual 1 break is now characterized (prior report wanted this). **Still open (inherent):** the ledger is proprietary and the canonicalization routine is not published as a standalone verifier, so the 100% content-integrity check and the 108/1 break split cannot be recomputed by an external reader. This is consistent with the proprietary-data decision, not a new defect — but it means the §2 integrity claims remain take-it-on-faith for outsiders.

**M8 — undisclosed "database disk image is malformed" → RESOLVED.**
Disclosed in Data availability: *"a direct read of the mutating file was the source of an earlier malformed-read on one auxiliary count, resolved by the snapshot."* The regenerated JSON confirms the clean value (`"distinct_accessed": 91`, no `ERR:` string) and `"integrity_check": "ok"`. The `distinct_accessed` field is no longer errored.

**M9 — "signals" named three populations → RESOLVED (minor residual).**
The load-bearing collision is fixed: the abstract and §3 now say *"trust-state rows"* for the 409,404 (was "signals"), and §3 adds *"The ledger's 12,129 signals (§2) are a distinct population and are not the base for this rate."* Conclusion uses *"12,129 ledgered signals; 409,404 trust-state rows."*
*Residual (minor):* "signals" is still used for two things — the 12,129 ledger signals and the 447,709-row `signals` table (*"0.0203% against all 447,709 signals"*). The paper flags them as distinct populations, so it's disambiguated by context, not by vocabulary.

**M10 — single-system external validity not scoped → RESOLVED.**
§8: *"The result is expected to transfer to systems that share Mentu's enabling conditions — capture-at-scale with no default organic-offer/retrieval pathway, a strict trace-credit contract, and no automatic reinforcement loop — and is not expected to describe systems whose architecture surfaces prior context by default."*

### Minors

**m1 — 98.97% vs 109 breaks → RESOLVED.** Percentage dropped; only mutually consistent counts remain (see M7).

**m2 — "12 tests green" unverifiable → RESOLVED.** Provenance now cites the path: *"dormant analyzer (12 tests green; `analyses/c25-return-intervention/test_analyze.py`)"* and the tree is committed for release.

**m3 — contradiction figures lack an as-of instant → NOT RESOLVED.** §4 still says *"74 of 76 open … at the snapshot; the longest unresolved has stood 21.5 days"* with **no UTC instant**. "At the snapshot" is ambiguous between the 2026-06-29 funnel cut and the pinned 2026-07-04 snapshot (see Regression R1). "21.5 days" is not produced by the re-derivation instrument (it computed `resolved`/`total`, not ages) and floats against `julianday('now')` in `retest.py`; it is not pinned to any frozen instant.

**m4 — 1,847 patterns vs 1,846 crystallize ops → RESOLVED (as an off-by-one).** The parenthetical "(1,846 crystallize operations)" was removed and the +1 is explained (instrument note: *"kind=pattern exceeds op=crystallize by exactly the count of seed/non-crystallize pattern signals"*). But the *number's provenance* is now mis-attributed — see R1.

**m5 — "median missing-footer rate 1.00" not observatory semantics → RESOLVED.** §2 scopes it as analysis-specific: *"the median missing-footer rate (§5; the observatory tracks the mean)."*

### Nits

**n1 — superseded citation file → RESOLVED.** Provenance now points at *"`applications/2026-07-04-citations-reverified.json` (11/11 verified against the live arXiv API and Crossref, 2026-07-04)."*

**n2 — dangling companion-paper ref → PARTIAL (pending, acceptable pre-submission).** Still *"Evidence-Carrying Execution (Azarang, 2026; arXiv identifier to be inserted at submission)."* This is a flagged human step in the escalation ("insert the companion ECX arXiv id"); it must not survive to the posted version.

**n3 — two "24"s → RESOLVED.** Disambiguated by context: *"24 `context_used` events … exist in the entire history"* vs *"24 runs were in the injected arm."*

---

## 2. Regressions / new reproducibility gaps

### R1 — MAJOR (most serious). Provenance attributes the pattern and contradiction figures to the pinned snapshot, but that snapshot yields different values.

Both provenance blocks claim all cir.db figures come from the pinned 2026-07-04 snapshot:
- Provenance: *"Stage-0, pattern, and contradiction figures re-derived read-only on the pinned `cir.db` snapshot (sha256 `0b320d9d…`) via `instruments/2026-07-04-return-baseline-rederivation.py`."*
- Data availability: *"The `cir.db`-derived figures (Stage 0, patterns, contradictions) are computed against a single pinned snapshot (sha256 `0b320d9d…`)."*

But the paper reports the **2026-06-29 frozen-cut** values, not the pinned-snapshot values:
- §4: *"The system crystallized **1,847** reusable patterns."*
- §4: *"**76** contradictions detected, 2 resolved, 74 open at the snapshot."*

The instrument's own hardcoded notes and escalation B5 say the pinned snapshot gives **different** numbers:
- Instrument patterns note: *"the +1 (**paper: 1,847 patterns / 1,846 crystallize ops**) is structural…"* — i.e. 1,847 is the *paper's* number, distinct from the snapshot fields `kind_pattern_now` / `crystallize_ops_now` it computes.
- Escalation B5: *"kind=pattern exceeds op=crystallize by exactly one **on the current snapshot too (2,004 vs 2,003)**."*
- Instrument contradictions note: *"the **frozen 76/2 is the 2026-06-29 cut** … only detection grew (76->%d)."* — i.e. on the pinned snapshot, detected contradictions > 76.

**Consequence:** an external reader who runs the cited instrument on the cited snapshot (`0b320d9d…`) will get **~2,004 patterns and >76 contradictions**, not the paper's 1,847 and 76. Two headline corroborating numbers do not trace to the source the provenance names. This is exactly the trace failure this lens exists to catch, and it is **new** — it was introduced by the (correct) resolution of old-B2, which pinned one snapshot and then over-claimed that *all* cir.db figures derive from it.

Note the asymmetry: Stage 0 handles this correctly — it reports the invariant numerator (91) and explicitly labels 409,404 the *"frozen read"* while giving the snapshot's own 433,155 / 447,709. Patterns and contradictions get no such treatment: single frozen-cut numbers, attributed to the snapshot.

**Fix (mirror the Stage-0 discipline):** attribute 1,847 / 76 / 2 / 74 to the *frozen ~2026-06-29 cir.db read* (as decay is attributed to the 2026-06-10 read), give that read an as-of instant, and — if the pinned snapshot is to be cited at all for these — add the invariance-style note (crystallization grew to 2,004; contradiction detection grew past 76; genuine resolutions stable at 2). Do **not** claim 1,847/76 were "computed against the pinned snapshot."

### R2 — MAJOR. Figure 4 still renders the superseded "≥10×" P1, contradicting the corrected §6.

`figs.py` `fig4()` draws the pre-amendment preregistration:
- *`"FROZEN BASELINE\n(pre-intervention arm)\norganic offer 0.0222%\nuse-when-offered floor 6/24"`*
- *`"FROZEN PREDICTIONS\nP1: return ≥ 10× baseline …"`*

But §6 explicitly supersedes both:
- *"the earlier per-row '≥10×' two-proportion formulation compared incommensurable units and is **superseded** — see the C25 amendment."*
- *"The pre-intervention baseline of this quantity … is **0/244 (0.0%)** for organic runs and **6/289 (2.08%)** … the 0.0222% per-trust-state-row access rate is the Stage-0 descriptive statistic, **not the P1 comparator**."*

So the rendered Figure 4 shows (a) the "≥10×" prediction the text calls superseded, and (b) `0.0222%` labelled as the P1 "FROZEN BASELINE," which §6 explicitly demotes to a descriptive statistic. The figure was not regenerated after the A1 amendment landed in the text. A reader taking Figure 4 at face value gets the wrong primary hypothesis. **Fix:** regenerate `fig4` to the per-run baseline (0/244; 6/289 = 2.08%) and the Wilson-lower-bound predictions; remove "≥10×" and the 0.0222% baseline label.

### R3 — MINOR. Figure 2(a) still annotates "0 ever boosted" as a finding, which §4 demotes.

`figs.py` fig2(a): *`a.text(..., "55.0% decayed at >60d\n0 ever boosted", ...)`*. But §4 and the Fig-2 caption reframe zero-boost as guaranteed by construction, not a finding: *"the informative quantity is the magnitude and monotonicity of decay, not the absence of upward drift, which the filter guarantees."* The rendered figure lags the demotion. **Fix:** drop or re-label the "0 ever boosted" annotation to match the caption.

### R4 — MINOR (loose attribution). P1's per-run baseline is sourced to cir.db, but is computed from the outcomes JSONL.

§6: *"The pre-intervention baseline of this quantity, re-derived read-only from a pinned, integrity-checked **store snapshot**, is 0/244 (0.0%) … and 6/289 (2.08%)."* In the instrument, `per_run_baseline` is computed entirely from `~/.mentu/training/cir-run-outcomes.jsonl` (the `OUTCOMES` file, sha256 `5c3085ef…`), not from the cir.db snapshot. The numbers reconcile (244 organic + 45 arm = 289 baseline feature runs; 6 offered-and-used, all injected; 0 organic), so this is attribution wording, not a wrong number — but "store snapshot" should read "the offer-outcomes snapshot (`cir-run-outcomes.jsonl`, sha256 `5c3085ef…`)."

---

## 3. What now reconciles exactly (positive confirmations)

- **Stage-0 numerator invariance:** 91 accessed, 91 distinct, 24 context_used — identical in body §3, `stage0_robustness.json` (`numerator_accessed: 91`, `numerator_distinct_accessed: 91`, `context_used: 24`), and `figs.py`. `distinct_accessed` no longer errors.
- **All five Stage-0 denominators** (392,947 / 409,404 / 433,155 / 447,709) and **rates** (0.0232 / 0.0222 / 0.0210 / 0.0203%) match across body, figure-data JSON, and figure script. Every rate is arithmetically correct against numerator 91.
- **Snapshot provenance** (sha256 `0b320d9d3d66…`, 2,271,764,480 bytes, integrity_check ok) is identical in the paper, the JSON, and the instrument's `PRAGMA` reads.
- **Experimental arms 24 / 21 / 6** match the instrument's baseline filter (post-2026-06-15 footer fix, pre-2026-07-02 intervention, feature-class), and the per-run baseline (0/244 organic; 6/289 experiment-inclusive = 2.08%) reconciles internally (244 + 45 = 289).
- **The instrument computes what §3 claims:** accessed = `access_count>0`; context_used = `event_type='context_used'`; per-run baseline over post-fix, pre-intervention, feature-class runs (`run_class ∉ {fixture,smoke,infra}`).

*Numbers in the paper NOT computable from the re-derivation instrument (traced to other frozen sources, acceptable but noted):* Stage-2 "4 useful" and Stage-3 success counts 13/24, 11/21 (from `c1b`/`collect.py`, not this instrument); median missing-footer 1.00 (baseline application doc); decay −0.270 / 55.0% / n=1,964 (2026-06-10 C3/C3a, undigested).

---

## 4. Verdict

**17 RESOLVED, 3 PARTIAL (M4 decay provenance, M7 ledger-integrity inherent, n2 companion id pending), 1 NOT-RESOLVED (m3 contradiction as-of instant).** Plus **4 new regressions**: R1 (major, snapshot mis-attribution of pattern/contradiction figures), R2 (major, Figure 4 shows superseded ≥10× P1), R3 (minor, Fig 2 "0 boosted"), R4 (minor, P1 baseline source wording).

The v1.1 blockers are genuinely closed and the Stage-0 core is now reproducible-by-design. The paper is **not yet postable** only because the snapshot-pinning fix was over-claimed: the two corroborating cir.db numbers (1,847; 76) do not reproduce from the pinned snapshot the provenance cites, and Figure 4 contradicts the corrected primary hypothesis. Both are cheap, text/figure-only fixes — no headline rate moves. **Recommendation: minor revision** (fix R1 attribution + regenerate figs 4 and 2a + add m3 as-of instant), after which the paper matches the reproducibility standard its preregistration design already sets.
