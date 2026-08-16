# BUILD — Constitutional Silence (Paper 4) v1

**Date:** 2026-07-04
**Compiles with:** `/scaffold docs/BUILD-constitutional-silence-paper-v1.md` (mechanical phases only — §9 split)
**Depends on:** the silence canon (`/Users/rashid/Desktop/Workspaces/mentu-physics/foundational/key/silence/` — `silence.md`, `silence-architecture.md`, `silence-lite.md`, `llm-guide.md`) · program BUILD (`docs/BUILD-epistemics-program-v1.md`, whose executor constitution this inherits) · ECX paper grounding (`paper/evidence-carrying-execution/formal/`) · `docs/CONTEXT-parked-and-parallel-papers.md`
**Executor:** claude-opus-4-8 driving mentu recipes (compiled) + guided sessions (theory/writing). All judgment pre-made; where it can't be, the phase is a SESSION or HUMAN item.
**Working title:** *When Not to Act: Abstention as a First-Class, Measurable Operation in Autonomous Agent Systems.*

---

## 0. Scope & thesis

### 0.1 The one-sentence claim

> Autonomous agent systems need **abstention as a governed, logged, measurable operation** —
> not the absence of action but a typed epistemic act with reasons, gestation, override
> rights, and outcome metrics — and a production orchestration engine already exhibits a
> measurable population of such events whose downstream outcomes can be joined and reported.

### 0.2 What the paper is (and is not)

Theory + first measurement. It contributes: (1) the **abstention operator** — a typed
non-action with a state machine (ACTIVE ↔ SILENT), a reason taxonomy, gestation-and-release
dynamics, and an override protocol; (2) a **taxonomy of non-response** that the field
currently conflates — *epistemic abstention* (integrity reasons) vs. *economic throttling*
(budget/rate reasons) vs. *scheduling deferral* (readiness reasons) — with different
semantics and different metrics for each; (3) **metric definitions with estimators** —
Silence-Coherence Ratio (fraction of abstentions that averted a downstream failure) and
Gestational Yield (fraction of deferred items later completed successfully) as
outcome-joined quantities, never asserted constants; (4) a **first production census** of
abstention-shaped events already recorded by a running engine (gate skips/aborts, judge
early-stops, sentinel watch-without-escalation, budget-gated challenge skips), with outcome
joins where the ledger supports them and honest readiness verdicts where it does not.

It is NOT: a claim that silence improves outcomes (that is what SCR*/GY* measure — results
reported as they land, incl. negative); a consciousness/experience claim (none, anywhere); a
fresh analysis of the C1b/C25 withheld arms (fenced — §1.4); a rate-limiting paper (the
taxonomy explicitly separates throttling from abstention).

### 0.3 Genre, venue, positioning clock

- arXiv first (cs.MA primary, cs.AI cross-list); workshop target from a live-CFP scan
  (agent-safety / agent-evaluation venues); CogSci-adjacent framing possible later.
- Conversation: the field's loudest agent-autonomy complaint is over-action (unwanted tool
  calls, forced answers, premature resolution). The ML lineage is the **reject option**
  (Chow), **selective prediction**, **learning to defer**, and 2024–26 **LLM abstention**
  work — all classifier/QA-centric. The gap this paper fills: abstention as a *governed
  operational act in agentic execution*, with rights/duties/override and production
  measurement — not a confidence threshold on a single prediction.
- Arc position: Paper 3 (ECX) governs action; Paper 2 measures memory return; **Paper 4
  theorizes and measures restraint.** The restraint *family* (held contradictions as
  superposition; scar tissue as retained failure memory) appears as discussion-level
  siblings only — no measured claims for them in v1.

### 0.4 Sources and their standing

The silence canon is an **internal design record** (2025): it supplies the operator, the
five lawful conditions (boundary maintenance, recursive holding, modal integrity, temporal
structuring, coherence preservation), the 204-LCI response contract, the gestation engine,
the override workflow, and the metric *names*. It is **never cited** in the paper. Its
asserted constants (SCR ≥ 0.8, GY ≥ 0.6, Θₛ > 1.2, φₑ-leak ≤ 0.1) are **inadmissible as
numbers** (program exclusions-§4 discipline: asserted-not-fitted); the *directional* claims
survive and the constants are fitted from data or dropped. Its physics-flavored quantity
(Curvature Deficit ΔGm) is dropped — no estimator. Silence-Lite is reclassified honestly:
a token-bucket rate-limiter is *throttling*, not epistemic abstention — it seeds the
taxonomy, not the operator.

### 0.5 Already built — do not rebuild

ECX grounding pass already anchors the abstention machinery to code: Gate operator
(`GateCondition.swift`, actions inject/skip/abort), judge stopping rules
(`CIRCognitive.judge()`, four rules), sentinel escalation/auto-resolve
(`SentinelRunner.swift`), adversarial budget skip (`AdversarialRunner.swift:59`), limits
enforcement (`LimitsEnforcer.swift`) — at engine commit `ca285e8a`. Reuse those anchors;
re-verify only what F1 newly cites.

---

## 1. Executor constitution (inherits program BUILD §1; deltas)

1. **Run-class rule:** every recipe carries `run_class: "infra"` (program §1.3; pre-hoc
   declaration already on file). Program runs never count toward any conjecture arm.
2. **Canon-source rule:** the silence canon supplies material, never citations, never
   numbers. Any constant appearing in the paper must be fitted from ledger data in an
   E-phase or explicitly absent.
3. **The C1b/C25 fence (CRITICAL):** the corpus's randomized withheld arms are the property
   of gated conjectures. This paper may restate only *published baseline facts* (from the
   return-base-rate paper) and may NOT run fresh analyses on arm data, compare arms, or
   report arm outcomes before the corpus gates open. Verify-step grep: the words
   "withheld arm" in the paper must co-occur with "published" or "future work" in the same
   paragraph; `analyses/c25*`/`analyses/c1b*` are never invoked by this BUILD's scripts.
4. **Regime boundaries** (program §1.4: four boundaries) apply to every census/join; splits
   reported per-regime, never pooled.
5. **Read-only instrument access** (raw file/`sqlite3 -readonly` snapshots; never `mentu`
   CLI); digests-first; okf/ grep exclusions; git discipline; escalation protocol — all
   inherited verbatim.
6. **No-consciousness rule:** the paper contains no claims about experience, awareness, or
   sentience. Verify-step grep: "conscious", "sentien", "aware of itself" → 0 hits (the
   word "awareness" allowed only in "situational-awareness" tool contexts; escalate any
   other hit).
7. **Honesty tags** (design principle / observed pattern / open hypothesis) on every claim;
   no upgrades; failures and null results published.

---

## 2. Target layout (NEW)

```
epistemics/paper/constitutional-silence/
  paper.md                       (W-series; single source)
  arxiv/                         (W4 package)
  theory/
    silence-operator-spec.md     (T1, SESSION — the operator, taxonomy, metric estimators)
  evidence/
    silence_census.py            (E1 — read-only event census)
    <date>-silence-census.md     (E1 report)
    silence_joins.py             (E2 — outcome joins + readiness verdicts)
    <date>-silence-outcomes.md   (E2 report)
    digests.json
  lit/<date>-prior-art-verified.json   (L1)
  formal/abstention-grounding.md       (F1 — file:line anchors at pinned commit)
  design/silence-event-contract.md     (G1 — first-class telemetry gap spec)
  referee/B-field.md B-measure.md B-claims.md   (B — report-only)
  figs/                          (state machine · census · gestation funnel)
```

---

## 3. Build phases

| Phase | Title | Effort | Gate (→ verify assertion) |
|---|---|---|---|
| L1 | Prior-art verification | max | JSON exists; ≥10 works verified (Crossref/arXiv in-session) each with a differ-line; 0 unverified; includes reject-option, selective prediction, learning-to-defer, ≥2 LLM-abstention works, mixed-initiative HCI |
| E1 | Abstention-event census | max | `silence_census.py` stdlib+readonly, digest header; report counts gate skip/abort, judge stops by rule, sentinel triggered-vs-escalated-vs-resolved, adversarial budget-skips, limits stops — per regime window, `feature`-class only, unknown-ts bucket surfaced |
| E2 | Outcome joins + readiness | max | `silence_joins.py`; SCR*/GY* estimators computed where join fields exist; explicit READY/NOT-READY verdict per estimator (instrumented-lab style); no C1b/C25 arm reads (grep script for c1b/c25 paths = 0) |
| F1 | Code grounding | xhigh | `formal/abstention-grounding.md`: every mechanism at `file:line`, commit pinned; reuses ECX anchors where valid; ≥5 mechanisms |
| G1 | Silence-event contract spec | xhigh | `design/silence-event-contract.md`: typed SilenceEvent (reason codes from the five conditions + throttling/deferral tags), release/override events, joins to run outcomes; engine impl explicitly out of scope; composes with telemetry-v2 (`theory/telemetry-v2-design.md`) |
| B | Referee lenses ×3 (report-only) | max | 3 reports, fixed rubric (claim/severity/quoted line/fix); paper.md byte-identical this phase |
| FIGS | Three figures | xhigh | state-machine, census (from E1 numbers only), gestation-funnel; validated palette (dataviz skill); PDF+PNG in figs/ |
| B5 | Venue CFP scan | xhigh | every deadline carries live-verified URL + access date; ≥4 rows |
| W4 | arXiv package | xhigh | tectonic exit 0; no `{{artifact:`; abstract ≤1,920 chars; byline "Rashid Azarang"; every number traces to evidence/ |

Sessions (§5, never compiled): **T1** operator spec (FIRST MOVER), W1 outline + claims
ledger, W2 draft, W3 honesty pass + B-apply.

---

## 4. Phase details

### T1 — Silence-operator spec *(SESSION; first mover — feeds everything)*
- File: `theory/silence-operator-spec.md`
- Distill the canon into the paper's own apparatus: (a) **operator definition** — abstention
  as a typed transition returning a structured non-output (reason code, guidance,
  timestamp), the ACTIVE↔SILENT machine; (b) **reason taxonomy** — the five epistemic
  conditions, PLUS the honest three-way split: epistemic abstention / economic throttling
  (Silence-Lite's token bucket, reclassified) / scheduling deferral; (c) **metric
  estimators** — SCR* := P(no downstream failure signal within window W | abstention) vs.
  matched action baseline; GY* := P(deferred item later completed successfully) via
  commitment capture→(no claim)→later claim/close chains; both defined on fields that exist
  (E2 confirms) with W and matching rules stated a priori; (d) **constants demoted** — every
  canon threshold becomes "to be fitted"; (e) **rights/duties/override** as the governance
  layer (ties to ECX's mechanical-governance result: prompt-level "don't act" leaks; this
  operator is the mechanical form of "don't act *yet*, lawfully").
- Must cite exclusions-§4 discipline for the demoted constants; canon = design record only.
**Session output gate (checked by W1):** spec contains the three-way taxonomy, both
estimators with window + matching rules, and zero asserted thresholds.

### L1 — Prior-art verification
- File: `lit/<date>-prior-art-verified.json`
- Verify in-session (Crossref/arXiv), each with canonical metadata + one-line
  how-we-differ: Chow's rejection option (1957/1970); selective prediction (El-Yaniv &
  Wiener, JMLR 2010); learning to defer (Madras et al., NeurIPS 2018); ≥2 recent LLM
  abstention/refusal-calibration works (2024–26, search live); selective generation;
  mixed-initiative interaction (Horvitz 1999) and interruption/attention-cost HCI; calm
  technology (Weiser & Brown) as UX ancestry; optionally option-value/real-options for the
  deferral economics. **Never cite from memory; unresolved → escalation.**
**Verify:** ≥10 entries, all `verified:true`, non-empty differ-lines.

### E1 — Abstention-event census
- File: `evidence/silence_census.py` + `evidence/<date>-silence-census.md`
- Read-only over ledger JSONLs + CIR store snapshot (program §1.7 snapshot pattern): count
  and classify the abstention-shaped events the engine already records —
  `gate_triggered` signals split by action (inject/skip/abort); judge early-stops by rule
  (budget / confidence-saturation / contradiction-ceiling / diminishing-returns) where
  recorded; sentinel lifecycle ratios (started → triggered → escalated vs. auto-resolved:
  watch-without-escalation IS the abstention); adversarial budget-skips; limits-enforcer
  terminations. Per regime window; run-class filter (`feature` analysis class; program
  runs excluded as `infra`); unknown-ts bucket surfaced per category; digests first.
- Honest framing baked into the report: these are *implicit* abstention records (the engine
  was not built with a first-class SilenceEvent); the census measures what exists and G1
  specifies what's missing.
**Verify:** script read-only + stdlib (import allowlist grep); report has all five
categories + regime splits + unknown-ts table; no path containing `c1b`/`c25` in script.

### E2 — Outcome joins + readiness verdicts
- File: `evidence/silence_joins.py` + `evidence/<date>-silence-outcomes.md`
- Compute SCR*/GY* per T1's estimators where the join fields exist: e.g., compound runs
  containing gate-skips vs. matched compounds without → downstream failure/rework rates
  (from `cir-run-outcomes.jsonl`, feature-class, per-regime); deferred commitments
  (captured, unclaimed ≥ threshold, later claimed+closed) as gestation traces → GY*.
  Where a join field is missing, emit **NOT-READY (missing instrumentation)** — the
  instrumented-lab discipline: distinguish missing instrumentation from insufficient data
  from a real null. All three outcomes are publishable content.
**Verify:** report contains a READY/NOT-READY verdict per estimator; every computed number
carries a digest; matching rule stated; no arm analyses.

### F1 — Code grounding
- File: `formal/abstention-grounding.md`
- Anchor every mechanism to `file:line` at the pinned commit (reuse ECX anchors:
  GateCondition actions, `CIRCognitive.judge()` stopping rules, `SentinelRunner`
  escalation chain + auto-resolve, `AdversarialRunner.swift:59` budget skip,
  `LimitsEnforcer`); note which mechanisms emit CIR signals today and which do not
  (feeding G1). Static reads only; carrier of honesty tags.
**Verify:** ≥5 mechanisms with `file:line` + commit hash; emits-signal column present.

### G1 — Silence-event contract spec
- File: `design/silence-event-contract.md`
- The gap made buildable: a typed `SilenceEvent` (id, reason ∈ five-conditions ∪
  {throttling, deferral}, du/entropy snapshot optional, run/workspace linkage), release +
  override events (override justification logged — the canon's Right-to-Override made
  mechanical), and outcome-join keys — designed to compose with the telemetry-v2 pattern
  (`theory/telemetry-v2-design.md` — a program-BUILD C1 output that may not exist yet; if
  absent at G1 time, compose against the shipped v1 contract in
  `instruments/2026-06-19-general-epistemic-telemetry-handles.md` and note the v2
  dependency) and the three-rung outcome ladder. Engine
  implementation explicitly out of scope.
**Verify:** contains reason enum incl. taxonomy tags, override event, join keys, and the
out-of-scope statement.

### B — Referee lenses ×3 *(report-only, parallel)*
- Files: `referee/B-field.md` (does the positioning survive an ML-abstention expert —
  is this genuinely more than reject-option-at-the-agent-level?), `referee/B-measure.md`
  (estimator validity: matching, confounds — abstention events are not randomized;
  selection-on-difficulty bias MUST be named), `referee/B-claims.md` (tag discipline;
  no canon numbers; no consciousness language; C1b/C25 fence intact).
**Verify:** 3 files, rubric columns, `git diff --stat paper.md` empty this phase.

### FIGS — Three figures
- `figs/fig-silence-statemachine` (ACTIVE↔SILENT with reason taxonomy — diagram),
  `figs/fig-abstention-census` (E1 numbers only; per-category, per-regime),
  `figs/fig-gestation-funnel` (deferred → ripe → released → outcome, with NOT-READY
  stages hatched). Load dataviz skill first; validated palette; direct labels.
**Verify:** three PDF+PNG pairs exist; census figure numbers grep-match the E1 report.

### B5 — Venue CFP scan
- File: `evidence/<date>-venue-cfp-scan.md` — live-verified deadlines for agent-safety /
  agent-evaluation workshops + relevant tracks; format/anonymity requirements per row.

### W4 — arXiv package
- `arxiv/paper.tex` via pandoc+tectonic (reuse the ECX build pipeline incl. the
  unicode→math preprocessing); byline **Rashid Azarang** (Mentu, San Pedro Garza García,
  Nuevo León, Mexico; rashid@mentu.ai); abstract ≤1,920 chars; category cs.MA primary /
  cs.AI cross [HUMAN may override]; license CC BY 4.0 [HUMAN may override].
**Verify:** tectonic exit 0; `grep -c "artifact:"` = 0; abstract length scripted;
byline present.

---

## 5. Sessions

| Session | Deliverable | Gate to start |
|---|---|---|
| T1 | `theory/silence-operator-spec.md` | none — first mover |
| W1 | `paper.md` outline + claims ledger (claim → evidence source → tag) | T1 + L1 + E1 done |
| W2 | full draft | W1 + E2 + F1 + G1 done |
| W3 | honesty-tag audit + apply B reports + FIGS integration | B + FIGS done |

## 6. Execution algebra

```
SESSION SPINE: T1 ─▶ W1 ─▶ W2 ─▶ W3
COMPOUND CS-NOW (all run_class:infra):
  L1a: L1 ∥ F1 ∥ E1                       [independent; E1 needs no T1 — categories are fixed]
  L2 :  E2 [dep T1-spec exists + E1]  ∥  G1 [dep T1 + F1]
  L3 :  B-field ∥ B-measure ∥ B-claims [dep W2 draft exists]   FIGS [dep E1, E2]
  L4 :  B5  ∥  W4 [dep W3 complete]
HUMAN REGISTER: arXiv endorsement/category/license · submit click · the "204-LCI" branding
decision (keep the canon's charming status-code framing in the paper, or neutralize it —
author's voice call) · sequencing vs. the Anchor-2 + ECX coordinated drop (this paper ships
AFTER that pair; no new gate needed).
```

## 7. Locked decisions

1. Byline "Rashid Azarang"; Mentu affiliation (program-wide identity). 2. Canon never
cited; constants fitted or absent. 3. Three-way non-response taxonomy is load-bearing —
throttling is not abstention. 4. C1b/C25 fence absolute in v1. 5. Restraint-family siblings
(superposition, scar tissue) = discussion only. 6. Selection-bias caveat (abstentions are
not randomized) named in abstract-adjacent text, not buried. 7. No consciousness language.
8. All numbers re-derived with digests; NOT-READY verdicts are publishable findings.

## 8. Verification-commands appendix

```bash
P=paper/constitutional-silence
grep -rn "c1b\|c25" $P/evidence/*.py                                  # expect 0
grep -in "conscious\|sentien" $P/paper.md                             # expect 0
grep -n "0\.8\|0\.6\|1\.2" $P/paper.md | grep -vi "fitted\|to be fitted\|not asserted"  # review hits
grep -c "NOT-READY\|READY" $P/evidence/*silence-outcomes*.md          # ≥1 per estimator
grep -rn "mentu-physics" $P/paper.md                                  # expect 0 (canon never cited)
```

---
*Authored 2026-07-04 by Fable 5. The operator is the theory; the census is the proof of
existence; the joins are the first evidence; the fence protects the sibling science. The
paper's own subject is its discipline: measure what restraint does, and where you cannot
measure yet, say NOT-READY — out loud.*
