# B2 — Reproducibility referee report

**Paper:** `paper/return-base-rate-paper.md` (Draft v1.1, 2026-07-04)
**Lens:** reproducibility only — can an external reader re-derive every number from what the paper states, and is provenance/data-availability sufficient for arXiv?
**Method:** paper read in full; cross-checked against `observatory/collect.py`, `analyses/{c1b,c3-epistemic-entropy,c9-pattern-crystallization-utility,c25-return-intervention}/`, `applications/2026-07-01-return-funnel-and-footer-root-cause.md`, and the figure-data files `paper/stage0_robustness.json` / `paper/contradiction_series.json`. **Numbers treated as frozen — flagged, never recomputed.** Report-only.

Each finding: **claim attacked | severity | exact quoted line | proposed fix.**

---

## Blockers

### B1 — No data or code availability statement anywhere
**Claim attacked:** That the paper's results are, in principle, reproducible from a public release.
**Severity:** blocker
**Exact quoted line:** *(none exists)* — the closest the paper comes is the provenance footer: "*Provenance.* Funnel: `cir-run-outcomes.jsonl` sha256 `5c3085ef…`, 971 rows, source mtime 2026-06-29T15:33:35Z, observatory/collect.py semantics." and §2 "read strictly read-only for this study (raw file/SQLite reads only…)". There is no "Data availability" or "Code availability" section.
**Why it blocks:** For arXiv, a paper whose entire selling point is "ledger-backed real-world evidence" must state whether *anything* (ledger, SQLite store, `cir-run-outcomes.jsonl`, the `analyses/`+`observatory/` scripts, or only digests) will be released, and if not, why. As written, a reader has *zero* path to any artifact and no statement that this is intentional.
**Proposed fix:** Add an explicit Data & Code Availability statement. The honest version is likely "the production store is proprietary; we publish (a) cryptographic digests, (b) the analysis/collection scripts under `analyses/` and `observatory/`, (c) the de-identified `cir-run-outcomes.jsonl` snapshot, (d) the frozen figure-data JSONs." State exactly which of these ship and where.

### B2 — The SQLite store backing four of the paper's findings carries no provenance digest, no snapshot, and is a live mutating file
**Claim attacked:** That the provenance block ("sha256 + mtime + row count") covers the paper's numbers.
**Severity:** blocker
**Exact quoted line:** "Ledger integrity, decay, pattern, and contradiction figures from the frozen corpus analyses (C1b, C3/C3a, C7, C9)."
**Why it blocks:** The provenance block stamps only `cir-run-outcomes.jsonl` (the offer experiment). But Stage 0 (91/409,404), the decay finding, pattern non-reuse, contradiction backlog, and the hash-chain integrity claims all derive from `~/.mentu/cir.db`, for which the paper gives **no sha256, no byte size, no mtime, no schema version, no snapshot date**. The corpus's own scripts *do* capture these (`c3-epistemic-entropy/retest.py` records `db_size_bytes`, `db_mtime_utc`, `schema_user_version`); the paper drops them. Worse, `cir.db` is live and mutating (post-intervention runs accrue into it), so a bare row count is not a snapshot. The referee-prompt question "is sha256 + mtime + row count sufficient?" — it is provided for the JSONL only, and is *absent* for the store that backs most headline numbers.
**Proposed fix:** Add a full provenance line for the `cir.db` snapshot used (sha256 of the file or of a dumped canonical form, byte size, mtime, `PRAGMA user_version`, and the UTC "as-of" instant every db query was evaluated against). Pin one snapshot and reference it for Stage 0, decay, patterns, and contradictions.

### B3 — "Pattern non-reuse (true zero)" contradicts both the paper's own §8 and the C9 artifact, which classifies this state as an instrument gap, not a zero
**Claim attacked:** That pattern non-reuse is a *true zero* "distinct from a measurement gap."
**Severity:** blocker
**Exact quoted line:** "We find no evidence that crystallized patterns are selected or used in later runs — a true zero, distinct from a measurement gap: the patterns exist and are queryable; they are simply not returned into subsequent work." (and Fig 2b: "a true zero, not a measurement gap")
**Why it blocks:** This is unreproducible *and* self-contradicted. (a) §8 says of the same finding: "Pattern non-reuse and the contradiction backlog are measured, but their gated verdicts (C9, C3 re-test) remain closed pending accrual." A finding whose verdict is "closed pending accrual" cannot simultaneously be a "true zero." (b) The C9 artifact `analyses/c9-pattern-crystallization-utility/analyze.py` is explicitly a *readiness* check ("intentionally does not produce a verdict effect table until crystallized patterns are exposed to runs and measured as used"), whose gates include `post-first-exposure runs >= 50`, `pattern-injected runs >= 30`, `pattern-used runs >= 10`. When those fail, its own verdict string is `INSTRUMENT INSUFFICIENT: pattern substrate exists, but exposure/use gates fail` — i.e. precisely a *measurement gap*, the opposite of the paper's claim. The paper is upgrading an "instrument not ready" state into a headline "true zero." This is exactly the absent-vs-unmeasurable distinction the paper (correctly) insists on for Stage 2; applying the opposite standard to C9 is a reproducibility and faithfulness defect.
**Proposed fix:** Either (i) demote to "no reuse observed; the reuse-detection channel is present (pattern IDs are queryable against `injected_signal_ids`/`used_signal_ids` in run outcomes) but exposure is below the C9 readiness gate, so this is a *floor*, not a confirmed zero," or (ii) if a true zero is genuinely defensible, show the detection channel *fired and returned zero* over ≥ the gate thresholds, and state the exact query and denominators. Drop "true zero, not a measurement gap" until one of these holds. Reconcile with §8.

---

## Major

### M1 — Body denominators for Stage 0 disagree with the figure's own data file
**Claim attacked:** Robustness of the 10⁻⁴ rate "to the choice of denominator."
**Severity:** major
**Exact quoted line:** "The rate is robust to the choice of denominator — 0.0214% against all 424,304 signals in the store, 0.0222% against trust-state rows".
**Detail:** The figure-data file `paper/stage0_robustness.json` (which backs Fig 1b) reports the "all signals" denominator as **424,321** and the trust-state denominator as **409,768** (its `robustness_rows`), while the frozen Stage-0 denominator is **409,404** (`frozen_denom`). The paper's body quotes **424,304** (matches *neither* the live 424,321 *nor* any frozen field) and **409,404**. So the body's "424,304" is an orphan, and Fig 1b's denominators (424,321 / 409,768) differ from the body (424,304 / 409,404). The *percentages* round to the same values, so the headline survives — but three of the four denominators that appear cannot be reconciled with each other, and a reader re-deriving 0.0214% cannot reproduce "424,304."
**Proposed fix:** Pick one snapshot (frozen), regenerate Fig 1b from it, and quote denominators identical to the figure-data JSON. Explain the frozen-vs-live split (409,404 vs 409,768) or eliminate it.

### M2 — "Accessed", "context_used", and "cited" are never operationally defined in the paper
**Claim attacked:** That Stage-0/Stage-2 numbers are re-derivable.
**Severity:** major
**Exact quoted line:** "91 / 409,404 signals (**0.0222%**) were ever accessed after capture; 24 `context_used` events exist in the entire history."
**Detail:** The operational definitions exist only in `observatory/collect.py`: accessed = `trust_state.access_count > 0`; context_used = `trust_events.event_type='context_used'`; cited = `use_rate > 0`. None appears in the paper. A reader cannot know what "accessed" counts, over which table, without the (unreleased) script.
**Proposed fix:** Give the exact predicate for each funnel quantity in-text or in a methods box (table, column, condition), independent of the script.

### M3 — The Stage-1 arm filter (24 injected / 21 withheld) is not specified
**Claim attacked:** Reproducibility of the offer-experiment arm counts.
**Severity:** major
**Exact quoted line:** "24 runs were in the injected arm, 21 in the withheld arm (post-measurement-fix, feature-class runs)."
**Detail:** Reproducing 24/21 requires four filters found only in `c1b/analyze.py`/`collect.py`: (1) `started_at >= 2026-06-15T02:57:24Z` (the "measurement fix" — *which* fix is never dated in the body; the 2026-06-15 date appears only parenthetically in §5, and the paper also introduces a *different* boundary at 2026-07-01T21:18:39Z, so "post-measurement-fix" is ambiguous between two fixes); (2) `run_class ∉ {fixture, smoke, infra}` with the exact `run_class()` name-heuristic; (3) `randomization_arm ∈ {injected, withheld}`; (4) the run-class fallback rules (e.g. `rcsleep→infra`, `fortress/ane-→infra`). None is stated.
**Proposed fix:** State the arm-construction filter precisely, disambiguate which fix defines "post-measurement-fix" (2026-06-15, not the 2026-07-01 diagnostic), and either publish `run_class()` or enumerate its rules.

### M4 — Decay figures cite no script and no snapshot, and use a trust-state total inconsistent with §2
**Claim attacked:** Reproducibility of the decay finding.
**Severity:** major
**Exact quoted line:** "mean effective−asserted confidence is −0.270 at >60 days, with 55.0% of >60-day signals decayed and 0 boosted (n=1,964 in that stratum; 217,629 trust-state rows overall)."
**Detail:** "217,629 trust-state rows overall" cannot be reconciled with §2's "409,404 trust-state rows" (nor the live 409,768) and is left unexplained (different snapshot? a filtered subset with confidence fields?). The retest script explicitly does *not* recompute decay ("does NOT re-open the decay half of P1… already graduated as corpus/supported/c3a-mechanical-decay.md"), so the number comes from an unnamed C3a analysis with no digest and no as-of date. Neither "effective confidence," the ">60 days" stratum boundary, nor "decayed"/"boosted" is defined.
**Proposed fix:** Name the C3a script, pin its db snapshot + as-of instant, define effective/asserted confidence and the decay/boost predicate, and reconcile 217,629 vs 409,404.

### M5 — "2 resolved (2.6%)" is computed by an undocumented "resolution semantics" that differs from the observatory semantics the paper claims to use
**Claim attacked:** "All funnel numbers below are computed with the observatory's canonical semantics verbatim, so they reconcile exactly with the system's own daily tracking."
**Severity:** major
**Exact quoted line:** "76 contradictions detected, 2 resolved (resolution rate 2.6%), 74 open".
**Detail:** Both `observatory/collect.py` and `c3-epistemic-entropy/retest.py` count resolved as `resolved_at IS NOT NULL`. But `paper/contradiction_series.json` states: "resolved_at is largely a batch backfill; the C3 gate counts 2 genuinely-resolved by resolution semantics." So the "2" does **not** come from the observatory's `resolved_at` count — it comes from a different, undefined "resolution semantics." The paper's blanket claim that numbers reconcile with observatory semantics is therefore false for this figure, and "genuinely resolved" is never defined, so 2.6% is not re-derivable.
**Proposed fix:** Define "resolved" precisely (what makes a resolution "genuine" vs a backfilled `resolved_at`), and either correct the "computed with observatory semantics verbatim" claim or align the contradiction count to the stated semantics.

### M6 — The `observatory/collect.py` semantics reference is unresolvable for an external reader
**Claim attacked:** That "observatory/collect.py semantics" is a usable provenance anchor.
**Severity:** major
**Exact quoted line:** "…source mtime 2026-06-29T15:33:35Z, observatory/collect.py semantics." / "computed with the observatory's canonical semantics verbatim".
**Detail:** `collect.py` reads `~/.mentu/training/cir-run-outcomes.jsonl` and `~/.mentu/cir.db` — private paths — and is not stated to be released. Citing it as the canonical semantics is citing an artifact the reader cannot see. Combined with B1, the semantics are effectively unpublished.
**Proposed fix:** Release `collect.py` (or a de-pathed excerpt) alongside the paper, or inline the semantics; then the reference resolves.

### M7 — Hash-chain integrity claims are not reproducible from what is given
**Claim attacked:** The §2 integrity results (100% content-integrity; 98.97% chain intact).
**Severity:** major
**Exact quoted line:** "all 11,106 reproduce exactly under the engine's canonicalization (zeroed hash/prevHash keys, sorted-key JSON, ISO-8601, escaped solidus) — a 100% content-integrity check. The single global chain is 98.97% intact; the 109 breaks are almost all (108) workspace-context switches, not tampering."
**Detail:** The canonicalization is described in prose but no script/spec is named, and the ledger is unreleased, so neither the 100% nor the 98.97% can be recomputed. See also m-Minor-1: 98.97% does not arithmetically follow from 109 breaks over 11,106 rows.
**Proposed fix:** Publish the canonicalization routine (or a standalone verifier) and the ledger digest; state the exact denominator used for "% intact."

### M8 — Stage-0 robustness is reported as clean, but the backing artifact contains an integrity error the paper does not disclose
**Claim attacked:** "The rate is robust to the choice of denominator."
**Severity:** major
**Exact quoted line:** "…because the numerator (91 accessed signals) is the binding quantity, not the denominator (Figure 1b)."
**Detail:** `paper/stage0_robustness.json` contains `"distinct_accessed": "ERR:database disk image is malformed"`. One of the robustness measures failed on a corrupted read of the 2.1 GB store. The paper presents robustness without disclosing that a robustness computation errored, and §2 calls the store simply "2.1 GB SQLite store" with no mention of integrity trouble. An undisclosed "database disk image is malformed" directly undermines the credibility of the very store whose read-only integrity the paper leans on.
**Proposed fix:** Disclose the malformed-read, state which snapshot was used for the *clean* numbers, and confirm (via `PRAGMA integrity_check` on the pinned snapshot) that the reported figures come from an intact copy.

### M9 — "signals" denotes three different populations, leaving the headline denominator ambiguous
**Claim attacked:** The definition of the population behind 0.0222%.
**Severity:** major
**Exact quoted line:** Abstract: "an append-only, hash-chained ledger of 12,129 epistemic signals and an operational store of 409,404 trust-state rows… Only 91 of 409,404 signals (0.0222%)…".
**Detail:** "Signals" is used for (i) 12,129 ledger rows, (ii) 409,404 trust-state rows, and (iii) 424,304 "signals in the store." The abstract calls trust-state rows "signals," which collides with the ledger's 12,129 "signals." A reader cannot tell what the 0.0222% base population *is* without reverse-engineering the scripts.
**Proposed fix:** Reserve "signals" for one thing; call the 409,404 "trust-state rows" consistently and never "signals."

### M10 — Single-system external validity is stated but not scoped
**Claim attacked:** Generalizability of "the base rate the whole field assumes."
**Severity:** major
**Exact quoted line:** "The study is a single production system and cohort."
**Detail:** The paper's thesis is that a field-wide assumption is wrong, resting on n=1 system. §8 acknowledges single-system but does not state *which properties of Mentu* would need to hold elsewhere for the base rate to transfer (e.g., no default organic-offer/retrieval pathway; a strict footer-credit contract; capture-at-scale with no reinforcement loop). Without that, a reader cannot judge whether 0.0222% is a Mentu artifact or a general phenomenon.
**Proposed fix:** Add one paragraph naming the enabling conditions (architecture/telemetry properties) under which the result is expected to replicate, and the conditions under which it would not.

---

## Minor

### m1 — 98.97% chain-intact does not reconcile with "109 breaks"
**Severity:** minor
**Exact quoted line:** "The single global chain is 98.97% intact; the 109 breaks…".
**Detail:** With 11,106 hashed rows (≈11,105 links), 109 breaks give ~99.02% intact, not 98.97%; 98.97% implies ~114–115 breaks. The stated break count and the stated intact-percentage do not agree, and the denominator for the percentage is unstated.
**Proposed fix:** State the exact link denominator and recompute; make "% intact" and "N breaks" consistent.

### m2 — "12 tests green" is unverifiable from the paper
**Severity:** minor
**Exact quoted line:** "Preregistration: corpus conjecture C25 + dormant analyzer (12 tests green)."
**Detail:** The claim is checkable *in the repo* (`analyses/c25-return-intervention/test_analyze.py` does contain exactly 12 test methods, runnable via the README's `PYTHONPATH="$PWD" python3 test_analyze.py`), but the paper gives no pointer, no command, and no release, so an external reader cannot confirm "green" — only take it on faith. The count is correct; the verifiability is not.
**Proposed fix:** Cite the test file path and the run command, and release the `analyses/c25-return-intervention/` directory (self-contained: the tests use tempdirs and do not touch `~/.mentu`).

### m3 — Contradiction figures lack an as-of snapshot date
**Severity:** minor
**Exact quoted line:** "the longest unresolved has stood 21.5 days."
**Detail:** "21.5 days" and the 76/2/74 counts are snapshot-dependent (the store is live), but no as-of instant is given; `retest.py` computes ages against `julianday('now')`, so the number floats with run time.
**Proposed fix:** State the UTC as-of instant for the contradiction snapshot.

### m4 — 1,847 patterns vs 1,846 crystallize operations is unexplained
**Severity:** minor
**Exact quoted line:** "The system crystallized 1,847 reusable patterns (1,846 crystallize operations)."
**Detail:** The off-by-one between patterns and operations is flagged but not explained; a reader re-running C9's `op='crystallize' AND kind='pattern'` count gets one number, not two.
**Proposed fix:** One clause explaining the +1 (e.g., a pattern with two source ops, or a non-op-tagged pattern), or reconcile to a single count.

### m5 — "median missing-footer rate 1.00" is not an observatory-semantics quantity
**Severity:** minor
**Exact quoted line:** "the median missing-footer rate is 1.00 — for half the injected arm the use-recording channel is entirely silent (§5)."
**Detail:** `collect.py` computes the *mean* `missing_footer_rate` (0.70 per the baseline doc), not the median. The median (1.00) comes from the baseline application doc, not the observatory script, so it is not covered by "all funnel numbers… computed with the observatory's canonical semantics verbatim."
**Proposed fix:** Define the median statistic explicitly (it is legitimate and stronger than the mean here), and scope the "observatory semantics verbatim" claim so it does not over-reach.

---

## Nits

### n1 — Provenance cites a superseded citation-verification file
**Severity:** nit
**Exact quoted line:** "Citations: `applications/2026-07-01-citations-verified.json` (11 verified, 1 corrected, 1 not-found; arXiv IDs confirmed against the arXiv API)."
**Detail:** A newer `applications/2026-07-04-citations-reverified.json` (same date as this draft) exists in which MemoryAgentBench is now "verified" (was "corrected") and the not-found/non-scholarly entries (ChainProof, ReplicatorBench) are dropped. The provenance line describes the older state. (No cited arXiv ID in §7 is "not-found" — the not-found entry is ChainProof, correctly *not* cited — so this is cosmetic, not a broken reference.)
**Proposed fix:** Point provenance at the 07-04 reverification and update the "1 corrected, 1 not-found" tally.

### n2 — Dangling companion-paper reference
**Severity:** nit
**Exact quoted line:** "A companion paper, *Evidence-Carrying Execution* (Azarang, 2026; arXiv identifier to be inserted at submission)".
**Detail:** A placeholder identifier is fine pre-submission but must not survive to the posted version; a reader cannot resolve the companion.
**Proposed fix:** Insert the arXiv id (or mark "in preparation") before posting.

### n3 — Two distinct "24"s invite confusion
**Severity:** nit
**Exact quoted line:** "24 `context_used` events exist in the entire history." vs "24 runs were in the injected arm".
**Detail:** Two unrelated quantities both equal 24 in adjacent stages; a reader can easily conflate them.
**Proposed fix:** Disambiguate in text (e.g., "24 context_used events, all-time" vs "the injected arm's 24 runs").

---

## Overall verdict

The paper is unusually disciplined about *statistical* provenance for its one released-format artifact (`cir-run-outcomes.jsonl`: sha256 + rows + mtime), and its preregistration machinery (dormant gated analyzers, frozen baselines) is genuinely reproducible-by-design. But as an arXiv reproducibility object it is **not yet acceptable**, for three converging reasons. First, there is **no data/code availability statement at all** (B1), and the artifacts that would make the paper reproducible are private `~/.mentu` paths plus unreleased scripts, so a reader has no path to any number. Second, the **SQLite store that backs four of the five headline findings has no digest, no snapshot, and is a live mutating file** (B2) — and its own robustness artifact reveals an undisclosed "database disk image is malformed" error (M8) — so even the digest discipline the paper is proud of does not cover most of its results. Third, the **"pattern non-reuse = true zero" claim is contradicted by the paper's own §8 and by the C9 readiness artifact** (B3), which classifies exactly this situation as an instrument gap; this is the same absent-vs-unmeasurable error the paper elsewhere (correctly) makes its central methodological point, applied backwards. Underneath the blockers sits a layer of *specification* gaps: operational definitions of "accessed/cited/context_used/resolved/decayed" live only in unreleased scripts (M2, M5), the arm and decay filters are not stated (M3, M4), body denominators disagree with the figures' own data files (M1), and "signals" names three different populations (M9). None of the frozen headline percentages moved under my checks — the internal-consistency failures are in *denominators, definitions, and provenance*, not in the top-line rates — but a reproducibility referee cannot certify a paper whose numbers are internally reconcilable only to someone holding the private store. **Recommendation: major revision.** The path is concrete and cheap: (1) add data/code availability; (2) pin and digest one `cir.db` snapshot with an as-of instant and publish `collect.py`/the `analyses/` tree; (3) inline the operational definitions and filters; (4) reconcile every denominator to its figure-data file; (5) downgrade "true zero" to a floor or substantiate it against the C9 gate. With those, the paper becomes as reproducible as its preregistration design already promises.
