# BUILD — The Epistemics Program v1

**Date:** 2026-07-02
**Compiles with:** `/scaffold docs/BUILD-epistemics-program-v1.md` (mechanical phases only — see §10 compile/session split)
**Depends on:** `README.md` (the constitution) · `AGENTS.md` · `lineage/exclusions.md` · `observatory/CANON-observation-packet-v0.1.md` · `contribution-strategy-memo.md` · `external-critique-audit-2026-07-02.md` · `/Users/rashid/Desktop/structural-waste/submission/SUBMISSION_GUIDE.md`
**Executor:** claude-opus-4-8 driving mentu recipes (compiled phases) and guided sessions (research phases). Every judgment this document could pre-make has been pre-made. Where judgment is *not* pre-made, the phase is a SESSION or a HUMAN item — never a recipe.

---

## 0. Scope & charter

### 0.1 The program's object

> **Under what conditions does a knowledge system improve itself faster than entropy degrades it?**

Working hypothesis (the program's one-line motivation — explicitly untested):
> *Civilizations do not scale because they know more; they scale because they lose less.*

Formal spine: **R_k — the knowledge reproduction number** — the expected number of causally-live descendants a knowledge item produces before extinction. Decay is the mortality hazard (C3a, supported: mean effective−asserted delta −0.270 at >60 days). Returns are reproduction events (C25 measures them). Provenance chains are genealogies. The **epistemic threshold is R_k = 1** — always *fitted from data*, never asserted as a constant (this is the standing ruling of `lineage/exclusions.md` §7, which subsumed "escape velocity" into C6's fitted growth coefficient).

Four roles, fixed: **Mentu** is the experimental platform. **The ledger** is the instrument. **Structural waste** is the failure mode. **Epistemic acceleration** is the phenomenon.

### 0.2 Sequencing law (violating this is a program failure, not a style choice)

**Anchors → framework → field-naming.**
1. Anchor 1: *Structural Waste in Digital Operations* — submission-ready at EJIS (human steps remain).
2. Anchor 2: *The Return Base Rate* — drafted, preregistered, negative-result empirical paper → arXiv + workshop.
3. Framework: the formal threshold model (R_k), simulation, fits, cross-system tests.
4. Field-naming: essays/manifesto/synthesis — only after ≥1 anchor is public.

No grand claim ships before its anchor. The 2025 canon (`/Users/rashid/Desktop/Workspaces/epistemic-main/`) is **lineage only**: it is never cited in any submission, and its vocabulary ("laws," physics analogies) enters public text only where an estimator exists.

### 0.3 Estate map

| Asset | Path | Role | Write policy for this program |
|---|---|---|---|
| Epistemics corpus | `/Users/rashid/Desktop/epistemics/` | Program home | Per constitution (§1); new dirs `docs/`, `theory/`, `simulation/` allowed |
| 2025 canon | `/Users/rashid/Desktop/Workspaces/epistemic-main/` | Idea reservoir / lineage | **READ-ONLY, never cited publicly** |
| Anchor 1 workspace | `/Users/rashid/Desktop/structural-waste/` | EJIS submission kit | Only `docs/revision/` additions |
| Mentu data home | `~/.mentu/` | The instrument | **READ-ONLY, raw file/SQLite access only** |
| Engine | `/Users/rashid/Desktop/mentu-complete/` | Platform source | **OUT OF SCOPE** (design docs only; no engine edits in this BUILD) |

### 0.4 The contamination trade-off (stated openly)

Executing this program through mentu recipes creates runs that land in `~/.mentu/training/cir-run-outcomes.jsonl` — the same file the C25 experiment counts. Unmitigated, the program would inflate its own experiment's accrual and shift workload composition mid-experiment. **Mitigation (mandatory):** every recipe in this program declares top-level `"run_class": "infra"`, which the C25 analyzer and `observatory/collect.py` exclude (`EXCLUDED = {fixture, smoke, infra}`; `feature` is the analysis class). **Consequence accepted:** program runs never advance any conjecture arm; the C25 gate clock (150 post-marker feature-class runs) stays organic. This decision is recorded pre-hoc in Phase H0 *before any recipe runs*.

### 0.5 Already built — do not rebuild

- The corpus constitution, observatory beat (06:13 daily), C1b sentinel, 24 conjecture files, 2 supported + 1 refuted verdicts, the C25 shipped intervention + dormant analyzer (`analyses/c25-return-intervention/analyze.py`, gate `C25_GATE_PER_ARM = 150`).
- The return-base-rate paper draft (`paper/return-base-rate-paper.md`) with verified citations (`applications/2026-07-01-citations-verified.json`) and 4 local figures.
- Anchor 1's full submission kit (`structural-waste/submission/`), venue decision, empirical program, panel packet.
- The telemetry v1 contract (`instruments/2026-06-19-general-epistemic-telemetry-handles.md`).

### 0.6 Out of scope for v1

Engine implementation of telemetry v2 (design only); E3/E4 cross-system execution (deferred compound); D5/E4/G2–G5 content drafting (sessions, gated); any verdict ratification (human); okf/ regeneration (forbidden while C1b/C3 live); pushing git remotes.

---

## 1. Executor constitution

*The rules below bind every recipe and every session in this program. Sources are pinned; where quoted, the quote is verbatim. On any conflict, the source file wins.*

### 1.1 Corpus constitution (source: `README.md` §"The Constitution")
1. Nothing enters the corpus as a law; claims enter as **conjectures**.
2. Graduation requires (a) a measurement procedure naming exact data sources and fields, and (b) a result computed from real Mentu data.
3. Lifecycle: `conjecture → operationalized → tested → supported | refuted | revised`.
4. Predictions are written **before** results are computed; falsification criteria stated in advance; negative and ambiguous findings reported.
5. Refuted claims are kept in `corpus/refuted/` — never deleted.
6. Claims with no conceivable measurement procedure are not admitted; exclusions are documented in `lineage/exclusions.md`.

### 1.2 Frozen artifacts & the observer rule (sources: `observatory/CANON-observation-packet-v0.1.md`, `AGENTS.md` rules 2–3)
- Verbatim: tasks "may **never** edit frozen predictions, verdicts, results, or anything in `corpus/supported/` / `corpus/refuted/`."
- Verbatim: "Verdicts come only from gate-triggered frozen analyses, never from interpretation." Verdicts are analyzer-proposed, **human-ratified**.
- Verbatim: read Mentu data "via raw read-only SQLite / file reads — never via `mentu` CLI or MCP paths (observer effect)."
- **`README.md` and every `tracking:` frontmatter block are beat-owned.** No recipe or session in this program writes them.

### 1.3 Run-class rule (CRITICAL — the anti-contamination rule)
- Every recipe JSON in this program carries top-level `"run_class": "infra"`.
- Phase H0 records the decision in `instruments/2026-07-03-build-program-run-class-declaration.md` **before the first recipe run**.
- Every phase's Verify block includes: recipe JSON contains `"run_class": "infra"`.
- After the first compound run: read-only grep of `~/.mentu/training/cir-run-outcomes.jsonl` confirms the program's runs landed as `infra` (the summary-path recorder classifies by name only — if any program run landed as `feature`, STOP and escalate; do not edit the jsonl).

### 1.4 Regime boundaries (never pool data across any of them)
1. **2026-06-10** — instrument founding (AGENTS.md: never pool pre/post).
2. **2026-06-15** — C1b footer fix (paper §5 treats as boundary).
3. **2026-07-01T21:18:39Z** — footer diagnostic (engine commit `dbef5dfd`).
4. **2026-07-02T18:43:00Z** — C25 intervention (engine commit `fb85d754`; marker `instruments/c25-intervention-marker.json`; env override `MENTU_C25_INTERVENTION_AT`).

### 1.5 Numeric integrity (the anti-re-derivation rule)
- **Never recompute a frozen paper/corpus number from live `~/.mentu` data.** Live data has grown since every snapshot; a recomputed number that "corrects" a frozen baseline is the program's most dangerous failure mode.
- Number verification means **textual cross-consistency between documents**, against the frozen sources named in §4 (B1).
- Any mismatch → write `docs/escalations/<date>-<phase>-numeric.md` quoting both values and both sources; make **no** edit; emit the completion keyword.

### 1.6 Citation integrity
- No citation enters any paper without in-session verification (Crossref for DOIs, arXiv API for arXiv IDs).
- The canon is never cited in submissions. `ChainProof` is a vendor site, not a scholarly work — it stays out of all bibliographies (per `applications/2026-07-01-citations-verified.json`).
- Never *add* citations during a verification pass; verification can only confirm, correct metadata, or escalate.

### 1.7 Code & environment discipline
- `analyses/` is Python **stdlib-only**, read-only against `~/.mentu`, digest-first (dataset digest printed before any statistic). This rule does **not** apply to `simulation/` (§6, D2), which has its own venv and **never reads `~/.mentu`**.
- Grep hygiene: every search in this repo uses `--exclude-dir=okf --exclude-dir=.scratch_handoff --exclude-dir=__pycache__`. `okf/` is a stale, gitignored projection (2026-06-14); **never regenerate or `okf ingest` during this program** (observer effect on live conjectures).
- Data snapshots: when an analysis must read `~/.mentu/cir.db`, snapshot first — `sqlite3 -readonly ~/.mentu/cir.db ".backup <scratch>/cir-snapshot.db"` — record sha256 + source mtime, and read the snapshot. Never write anything under `~/.mentu`.
- The live ledger is `~/.mentu/.mentu/ledger.jsonl`; the root `~/.mentu/ledger.jsonl` is **STALE** (ends 2026-06-08). C3's audit reads the live one.

### 1.8 Git discipline
- Commit only files the phase itself created or edited, by explicit path. Never `git add -A`. Never push. Commit messages end: `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

### 1.9 Escalation protocol (standard wording, verbatim in every prompt)
> "If an escalation trigger fires: write `docs/escalations/<date>-<phase>.md` describing the trigger, the evidence, and the smallest safe next step; make no further changes; emit the completion keyword."

Triggers: (a) any instruction would touch a frozen artifact, `README.md`, or a `tracking:` block; (b) any verdict-shaped decision; (c) any external publication click; (d) any new-conjecture admission; (e) any numeric discrepancy (§1.5); (f) any citation that fails verification; (g) any program run observed with `run_class` ≠ `infra`.

---

## 2. Target repo layout (NEW items marked)

```
epistemics/
  docs/                       ← NEW (this file; escalations/; referee/; revision templates)
    BUILD-epistemics-program-v1.md
    escalations/              ← NEW (empty until a trigger fires)
    referee/                  ← NEW (B2 lens reports)
  theory/                     ← NEW (the model + PROPOSED registers; NOT corpus material
                                 until human admission — see §5, §6)
    formal-model-v1.md            (D1, session)
    telemetry-v2-design.md        (C1)
    signature-register.md         (D3)
    c25-supplement-1-decision-linkage-PROPOSED.md   (C2d)
    c25-effect-prediction-PROPOSED.md               (D4a)
  simulation/                 ← NEW (D2; own venv; never reads ~/.mentu)
    README.md  requirements.txt  sweep.py  model.py  results/
  instruments/
    2026-07-03-build-program-run-class-declaration.md   ← NEW (H0)
    conservation_audit.py                               ← NEW (C3)
  applications/
    <date>-citations-reverified.json                    ← NEW (B1)
    <date>-conservation-bookkeeping-audit.md            ← NEW (C3)
    <date>-cross-system-feasibility.md                  ← NEW (E1)
    <date>-portable-return-estimator-spec.md            ← NEW (E2)
    <date>-workshop-cfp-scan.md                         ← NEW (B5)
  paper/return-base-rate-paper.md      (B1 edits; B2-apply session edits; nothing else writes it)
  paper/arxiv/                ← NEW (B4a LaTeX package)
  spec/                       ← NEW (F1 protocol spec)
    epistemic-telemetry-spec-v0.1.md
```

Structural-waste workspace additions: `structural-waste/docs/revision/response-matrix-template.md` (A2a), `structural-waste/docs/panel/` (A3 recruitment sheet + invitations).

---

## 3. Build phases

| Phase | Title | Workspace | Effort | Gate (→ verify assertion) |
|---|---|---|---|---|
| H0 | Run-class declaration (pre-hoc) | epistemics | xhigh | Declaration file exists; states `infra` + consequence; dated before any recipe run |
| B1 | Paper freshness + citation re-verification | epistemics | xhigh | No `{{artifact:` in paper; fig1–4 referenced; reverified JSON has 11/11 `verified`; §8 new sentence present; stale phrases absent |
| C3 | Conservation bookkeeping audit | epistemics | xhigh | `conservation_audit.py` exists, stdlib-only, digest header; audit report exists with 4-bucket table + instrument-gaps section |
| E1 | Cross-system feasibility matrix (absorbs B3) | epistemics | xhigh | Matrix exists with all 6 mandatory columns incl. license; ≥5 corpora rows; per-paper verdict column |
| A2a | EJIS revision response-matrix template | structural-waste | xhigh | Template exists; one row per §7 risk-register entry (R1–R7) |
| A3 | Phase-0 panel recruitment kit | structural-waste | xhigh | Shortlist criteria sheet + invitation letter + tracking sheet exist; no new panel packet authored |
| B2 | Referee lenses ×4 (report-only) | epistemics | max | 4 reports exist in `docs/referee/`; fixed rubric columns present; paper file byte-identical (report-only) |
| C1 | Telemetry v2 design (decision linkage + outcome ladder) | epistemics | max | Design doc exists; names v1 fields verbatim; defines decision-linkage fields + 3-rung ladder; states engine-out-of-scope |
| D2 | Simulation harness | epistemics | max | `simulation/` exists w/ README + pinned requirements; sweep produces `results/` artifact discriminating sharp-vs-smooth; no `~/.mentu` reads (grep) |
| E2 | Portable return-estimator spec | epistemics | max | Spec exists; defines capture/return/extinction events per corpus type; keyed to E1 columns |
| B4a | arXiv LaTeX package (no submit) | epistemics | xhigh | `paper/arxiv/` compiles via tectonic exit 0; no `artifact:` strings; abstract ≤1,920 chars; byline "Rashid Azarang" |
| C2d | c25s1 supplement PROPOSED draft | epistemics | xhigh | PROPOSED file exists in `theory/`; contains conditional VOID clause; frozen c25 file untouched (hash check) |
| F1 | Protocol spec v0.1 | epistemics | max | Spec exists; unifies 3 pinned sources; version header; no invented engine behavior (quotes sources) |
| D3 | Signature register | epistemics | max | Register exists; maps §III items of the pinned canon doc to model observables; marked PROPOSED; canon cited as lineage only |
| D4a | Mentu fit + C25-effect prediction (PROPOSED) | epistemics | max | Snapshot digest (sha256+mtime) recorded; prediction file exists with simulation commit hash; dated ≤2026-07-25 |
| B5 | Workshop CFP scan | epistemics | xhigh | Scan doc exists; every deadline carries a live-verified source URL + access date |

Phases D1, B2-apply, A2b, D5, E3/E4, G2–G5: **sessions or deferred** — not in this table, not compiled (§10).

---

## 4. Phase details

### Phase H0 — Run-class declaration (FIRST; blocks everything)
- File: `instruments/2026-07-03-build-program-run-class-declaration.md`
- Change: create the pre-hoc declaration: all BUILD-program recipes run as `run_class: infra`; program runs never count toward any conjecture arm; the C25 gate clock stays organic; residual risk (summary-path name-only classification) and the post-first-run confirmation step (§1.3) stated.
- Why: prevents the program from contaminating the experiment it studies (Part 0.4).
**Verify:** file exists; contains `run_class` and `infra` and `C25`; file's date precedes any program recipe run.

### Phase B1 — Paper freshness + citation re-verification
- File: `paper/return-base-rate-paper.md`
- Change (pre-made edits, apply exactly):
  1. §8 Limitations — replace the sentence beginning "The intervention arm (C25) does not yet exist" with, verbatim:
     > "The intervention pathway (C25) shipped 2026-07-02T18:43:00Z (engine commit `fb85d754`), after this baseline was frozen; its preregistered analysis gate (≥150 post-intervention feature-class runs) remains closed. This paper reports the baseline and the preregistration, not an intervention result."
  2. Abstract — apply the same tense correction to the phrase "stays closed until the pathway ships and ≥150…" → "…stays closed until ≥150 post-intervention runs accrue (the pathway shipped 2026-07-02)."
  3. Figure embeds — replace exactly:
     `{{artifact:art_8d1b821f-f787-4a6d-96f7-8c1ff07ec3fe}}` → `fig1_funnel.png`
     `{{artifact:art_4dc65d3d-e75e-4bb5-ac78-72a53f82eb80}}` → `fig2_corroboration.png`
     `{{artifact:art_cafb5f1c-b1bf-46dd-8554-b8e555d4a495}}` → `fig3_footer_diagnostic.png`
     `{{artifact:art_9e42d2f8-b43c-4812-a8ec-f1c28ece75ed}}` → `fig4_preregistration.png`
     (markdown image syntax, paths relative to `paper/`).
  4. Status line — "Draft, 2026-07-01" → "Draft v1.1, <today's date>".
  5. Sweep greps for stragglers: "does not yet exist", "not yet shipped", "until the pathway ships" — each hit gets the tense fix or an escalation if ambiguous.
- File: `applications/<date>-citations-reverified.json`
- Change: re-verify **exactly these 11 in-paper identifiers** against live arXiv API / Crossref; write the JSON in the same schema as `applications/2026-07-01-citations-verified.json`:
  arXiv `2310.08560`, `2504.19413`, `2501.13956`, `2502.12110`, `2410.10813`, `2402.17753`, `2507.05257`, `2508.02866`, `2603.21692`, `2603.22767`; DOI `10.1371/journal.pone.0339920`.
  Acceptance = all 11 `verified`. Anything else → escalation (§1.9). **Never add a citation.** ChainProof stays out.
- Change (number cross-consistency, §1.5 — textual only, no recomputation). The paper's numbers must match these frozen sources:
  `corpus/conjectures/c25-return-intervention.md` (0.0222% · 91/409,404 · arms 24/21 · 6 citing · marker/commit `fb85d754`);
  `applications/2026-07-01-return-funnel-and-footer-root-cause.md` (funnel + 0.0222% derivation);
  `corpus/supported/c3a-mechanical-decay.md` (−0.270 · n=1,964 · 217,629 trust rows; note: c3a rounds the decay share to "55%" — the paper's "55.0%" matches the results file `results/2026-06-10-c3-epistemic-entropy.md`, which is the authoritative table; this formatting difference is NOT a discrepancy).
  Full inventory to check verbatim in the paper: 12,129 · 11,106 · 98.97% · 109 (108) · 1,023 · 409,404 · 424,304 · 0.0222% · 0.0214% · 971 · 24 · 6/24 · 4 · 13/24 (54%) · 11/21 (52%) · 1,847 (1,846) · 76 · 2 (2.6%) · 74 · 21.5 · −0.270 · 55.0% · sha256 `5c3085ef` · commits `dbef5dfd`, `fb85d754`.
- Why: the paper is one stale sentence and four broken figure embeds away from arXiv-ready; its numbers are frozen and must stay so.
**Verify:** `grep -c "{{artifact:" paper/return-base-rate-paper.md` = 0; fig1–fig4 each referenced; the §8 replacement sentence present verbatim; "does not yet exist" absent; reverified JSON exists and contains no status other than `verified`/`corrected`.

### Phase C3 — Conservation bookkeeping audit
- File: `instruments/conservation_audit.py`
- Change: stdlib-only, read-only script (precedent: `instruments/baseline_stats.py`): classify every knowledge event across the live stores into **created / retained / lost / transformed**; print dataset digest first (counts, date ranges, sha256 of inputs); stores pinned: `~/.mentu/.mentu/ledger.jsonl` (live; root ledger is STALE), `~/.mentu/cir.db` signals (via `-readonly` snapshot, §1.7), `~/.mentu/audit.jsonl` if present, `~/.mentu/training/cir-run-outcomes.jsonl`; respect all four regime boundaries (report per-regime, never pooled).
- File: `applications/<date>-conservation-bookkeeping-audit.md`
- Change: run the script; report the 4-bucket table per regime + an **"instrument gaps"** section listing every unclassifiable event type with counts — this section is a mandatory input to C1.
- Why: adopts the conservation identity as bookkeeping discipline (never as a "law"); unclassifiable events reveal exactly where telemetry v2 must add fields.
**Verify:** script exists, contains no `import` outside stdlib (grep against an allowlist), contains `readonly`; report exists with `## Instrument gaps` section.

### Phase E1 — Cross-system feasibility matrix (absorbs old B3)
- File: `applications/<date>-cross-system-feasibility.md`
- Change: evaluate ≥5 candidate corpora for portable return-rate estimation — minimum set: Wikipedia edit/reuse dumps, GitHub/OSS reuse (forks/imports/clone-detection datasets), StackOverflow duplicates/links (Stack Exchange dump), one public PKM/zettelkasten export corpus, one agent-trace corpus (from B-paper related work). Mandatory columns: **corpus | access mechanism | license (SO/Wikipedia = CC BY-SA share-alike; GitHub = ToS constraints) | return-event operationalizability (keyed to E2's event definitions) | size | verdict-per-paper** (B-paper external-validity mention vs E-paper full analysis).
- Why: one scan serves both the B-paper's limitations section and the E-workstream's dataset selection; licensing decides publishability before any download.
**Verify:** file exists; header row contains all six column names; ≥5 data rows; `license` column non-empty in every row.

### Phase A2a — EJIS revision response-matrix template (workspace: structural-waste)
- File: `docs/revision/response-matrix-template.md`
- Change: template with one row per risk-register entry R1–R7 from `/Users/rashid/Desktop/structural-waste/VENUE_DECISION.md` §7, columns: reviewer objection (verbatim quote slot) | register row | manuscript section that pre-empts | response draft slot | change-made slot.
- Why: when the EJIS decision arrives, the response letter assembles instead of being invented.
**Verify:** file exists; contains R1…R7; contains "response draft".

### Phase A3 — Phase-0 panel recruitment kit (workspace: structural-waste)
- File: `docs/panel/recruitment-shortlist-criteria.md`; File: `docs/panel/invitation-letter.md`; File: `docs/panel/tracking-sheet.md`
- Change: derive strictly from `EMPIRICAL_PROGRAM.md` Phase 0 (§0.2–0.6) + `submission/panel_packet.md`: shortlist criteria (8–12 experts: IS + OM academics, senior architects/ops practitioners; conflict rules mirror EJIS reviewer-conflict rules), a ready-to-send invitation letter (panel task, time ask ~60–90 min, no compensation claim unless human adds one), and a tracking sheet (invited/agreed/completed/CVR-columns). **Do not author a new panel packet** — the packet exists.
- Why: Phase 0 is the minimum viable first study and the revision-window asset; recruitment is its only unbuilt piece. Actual sending = human.
**Verify:** three files exist; invitation contains no invented compensation/IRB claims (grep "IRB", "compensat" → 0 or escalate); criteria sheet cites `EMPIRICAL_PROGRAM.md`.

### Phase B2 — Referee lenses ×4 (report-only; parallel)
- File: `docs/referee/B2-stats.md`
- File: `docs/referee/B2-field.md`
- File: `docs/referee/B2-validity.md`
- File: `docs/referee/B2-repro.md`
- Change: four independent adversarial reviews of `paper/return-base-rate-paper.md` — lenses: (1) empirical methods/statistics (denominators, censoring, the 25%-floor logic, multiple-comparison exposure); (2) agent-memory field positioning (against the 11 cited works — is the gap claim right?); (3) measurement validity (funnel stage definitions, regime boundaries, run-class filters, footer-credit contract); (4) reproducibility (are the analyzer conventions — digest-first, stdlib, read-only — sufficient to re-derive every table?). Fixed rubric per finding: **claim attacked | severity | exact quoted line | proposed fix**. Mandatory pinned input: `external-critique-audit-2026-07-02.md` (do not re-derive its points). **Report-only: the paper file is not edited.**
- Why: same adversarial pass that took Anchor 1 from good to submission-grade; parallel lenses, serialized application.
**Verify:** 4 files exist; each contains the four rubric column names; `git diff --stat paper/return-base-rate-paper.md` empty for this phase.

### Phase C1 — Telemetry v2 design (decision linkage + the outcome ladder)
- File: `theory/telemetry-v2-design.md`
- Change: design (not implement) `mentu.epistemic_handle.v2`: (a) quote v1's fields verbatim from `instruments/2026-06-19-general-epistemic-telemetry-handles.md` (conjecture ids, evidence roles, evidence tiers, capture boundaries, score schemas, score sources, exposure-model inclusion; CLI flags `--conjecture`, `--evidence-role`, `--evidence-tier`, `--capture-boundary`, `--score-schema`, `--score-source`, `--exclude-from-exposure-model`, `--handle-id`, `--artifact-id`); (b) add **decision-linkage fields**: `decision_id` (the commitment a return influenced), `decision_edge` (offered→cited→decision-changed), `prior_decision_id` (provenance chain edge); (c) define the **three-rung outcome ladder** — rung 1 artifact-level return (v1 status quo), rung 2 decision-linked return (new fields), rung 3 outcome-linked return (join to `~/.mentu/training/cir-run-outcomes.jsonl` via `run:<id>` entity tags); (d) ingest C3's instrument-gaps section as requirements; (e) state explicitly: **engine implementation out of scope for this BUILD; storage stays in `SemanticContext.domain`/`entities` (no Merkle-breaking schema change), same constraint as v1.**
- Why: adoption #9 (decision as unit) + the critique's outcome ladder, turned into a buildable contract the engine team can implement later.
**Verify:** doc exists; contains `decision_id`, `decision_edge`, three-rung ladder section, "out of scope" statement, and ≥3 verbatim v1 flag names.

### Phase D2 — Simulation harness (after D1 session exists)
- File: `simulation/README.md`; File: `simulation/requirements.txt`; File: `simulation/model.py`; File: `simulation/sweep.py`
- Change: implement D1's model (`theory/formal-model-v1.md` is the spec — REQUIRED input; if absent, escalate, do not improvise): typed-graph knowledge system with demographic core — per-item mortality hazard (calibratable to C3a's shape: delta −0.009 at 0–7d → −0.270 at >60d), reproduction via return events, R_k computed from simulated genealogies; staged thresholds (capture→retrieval→structural→generative→autonomous) as orderable parameters. `sweep.py` sweeps S/M/I-style parameters, writes `simulation/results/<date>-sweep.json` + a summary md; the headline output: **does the return-on-structure curve show a sharp transition or smooth growth, and do stages admit skipping?** README states: own venv, pinned requirements (numpy allowed; this is not `analyses/`), **never reads `~/.mentu`**.
- Why: the theory core — turns the threshold from rhetoric into a discriminating, falsifiable model with derived observables.
**Verify:** four files exist; `grep -r "\.mentu" simulation/ --include=*.py` = 0 hits; `results/` contains ≥1 dated sweep artifact; README contains "never reads".

### Phase E2 — Portable return-estimator spec
- File: `applications/<date>-portable-return-estimator-spec.md`
- Change: define, per corpus type in E1's matrix, the **capture event**, **return event**, **extinction event**, and denominator, such that R_k and the return base rate are computable identically across systems (measurement-invariance section mandatory; Mentu's definitions from the paper's §3 funnel are the reference implementation, quoted).
- Why: cross-system claims die without invariant estimators; this is E3/E4's contract.
**Verify:** spec exists; contains sections for ≥3 corpus types; contains "measurement invariance"; quotes the funnel stage definitions.

### Phase B4a — arXiv LaTeX package (no submission)
- File: `paper/arxiv/return-base-rate.tex` (+ `references.bib`, figs copied)
- Change: convert the post-B1 markdown to LaTeX (pandoc at `/opt/homebrew/bin/pandoc`, compile with `tectonic` — both proven on this machine); byline **Rashid Azarang** (Mentu, San Pedro Garza García, Nuevo León, Mexico; rashid@mentu.ai) — same identity decision as the EJIS kit; abstract ≤1,920 chars (arXiv limit); figures from `paper/fig*.png`; bib from the 11 verified identifiers.
- Why: arXiv is the anchor's publication venue; the click itself is human (B4b in the manual register with category + license pre-locked in §8).
**Verify:** `tectonic paper/arxiv/return-base-rate.tex` exit 0; `grep -c "artifact:" paper/arxiv/*.tex` = 0; abstract char-count ≤1,920 (scripted); "Rashid Azarang" present.

### Phase C2d — c25s1 supplement, PROPOSED draft
- File: `theory/c25-supplement-1-decision-linkage-PROPOSED.md`
- Change: draft (as PROPOSED, id `c25s1`, lineage → `corpus/conjectures/c25-return-intervention.md` + `theory/telemetry-v2-design.md`) a **conditional, additive** secondary outcome: decision-linked returns per the v2 fields. Mandatory clause, verbatim: "This supplement is computed ONLY IF the v2 decision-linkage fields ship (dated engine commit recorded in an instrument doc) before the C25 gate opens; otherwise it is recorded VOID — a void is not a refutation." Header: "PROPOSED — not corpus material until human admission (RAT-1)."
- Why: extends C25's readout to the causal rung without touching the frozen preregistration.
**Verify:** file exists with VOID clause verbatim and PROPOSED header; sha256 of `corpus/conjectures/c25-return-intervention.md` identical before/after phase (frozen-file hash check).

### Phase F1 — Protocol spec v0.1
- File: `spec/epistemic-telemetry-spec-v0.1.md`
- Change: one versioned spec (PROV/OpenTelemetry genre) unifying: (1) `mentu.epistemic_handle` v1 (quote the contract) and v2 (from C1); (2) the observation-packet canon (`observatory/CANON-observation-packet-v0.1.md` — packet lifecycle, two-region frontmatter, constitutional guards); (3) the commitment protocol (source: the public `mentu-ai/protocol` repository — "The Commitment Protocol — A substrate for accountable action"; if a local canonical file exists in `mentu-complete`, pin it; otherwise mark `[HUMAN pins the canonical protocol source]` and proceed with the public repo reference). Spec sections: data model, event types, conformance levels, versioning policy. **No invented engine behavior: every normative statement quotes a source.**
- Why: protocols outlive theories (adoption #5); this is the program's infrastructure deliverable.
**Verify:** spec exists; contains version header `v0.1`; quotes ≥2 pinned sources by path; contains "Conformance".

### Phase D3 — Signature register (after D1)
- File: `theory/signature-register.md`
- Change: map each observable signature from the canon acceleration doc — pinned absolute source: `/Users/rashid/Desktop/Workspaces/epistemic-main/canon/foundational-documents/the-law-of-epistemic-acceleration.md`, §III (and the five §III signatures of the escaping-epistemic-threshold whitepaper at `/Users/rashid/Desktop/Workspaces/epistemic-main/science/knowledge-architecture/whitepapers/escaping-epistemic-threshold.md`: production acceleration, evolutionary coherence, structural leverage, reduced friction, generative feedback) — to a **model observable** from D1/D2 (e.g., reuse-fraction, genealogy depth, friction proxy, marginal-cost slope). Each mapping: canon phrasing (lineage citation only) | model observable | measurable proxy in Mentu fields | status `PROPOSED`.
- Why: the 2025 poetry becomes the 2026 predictions sheet — the loop the program exists to close.
**Verify:** register exists; ≥5 mappings; each row has a Mentu-field proxy; file contains "lineage only".

### Phase D4a — Mentu fit + C25-effect prediction (PROPOSED; deadline ≤2026-07-25)
- File: `theory/c25-effect-prediction-PROPOSED.md`
- Change: (1) snapshot `~/.mentu/cir.db` per §1.7 (record sha256 + mtime in the doc); (2) fit D1/D2's model parameters to the snapshot **within the frozen baselines** (decay shape from C3a's published table — not re-derived; return rate = the frozen 0.0222% baseline; friction from C2's operationalization); (3) locate Mentu on the model's curve (expected: deep sub-critical); (4) register the **quantitative predicted C25 effect** (predicted post-arm organic-offer rate ± interval, and the predicted sign/absence of downstream movement) with the simulation commit hash; (5) header: "PROPOSED — becomes a registered prediction only on human admission (RAT-2). VOID if the observatory logs the C25 gate-event before admission; never backdate."
- Why: the model earns its keep by predicting the intervention's result *before* the gate opens; the accrual clock (0/150 at ship, ~weeks to fill) sets the deadline.
**Verify:** file exists; contains a sha256, a simulation commit hash, a dated prediction, and the VOID clause; date ≤2026-07-25.

### Phase B5 — Workshop CFP scan (re-runnable)
- File: `applications/<date>-workshop-cfp-scan.md`
- Change: live-verify (fetch, don't recall) current CFPs/deadlines for: NeurIPS/ICLR/ICML agent- and memory-adjacent workshops, COLM, and empirical-SE venues open to measurement studies;每 row: venue | deadline (with source URL + access date) | fit note keyed to the paper's genre (real-world-evidence, negative result) | required format/anonymity.
- Why: B4b's click needs a target; recalled deadlines are the classic failure.
**Verify:** scan exists; every deadline row contains `http` and an access date; ≥4 rows.

---

## 5. Sessions (never compiled — run as guided Fable/Opus sessions with this document in context)

| Session | Deliverable | Gate to start | Notes |
|---|---|---|---|
| D1 | `theory/formal-model-v1.md` | none — **first mover** | The R_k model: typed graph; hazard (C3a shape); reproduction (return events); genealogies + generation-depth stats; staged thresholds; survival-analysis operationalization of continuity; MUST cite `lineage/exclusions.md` §7 and route every threshold through fitted quantities; PROPOSED register semantics (§6) |
| B2-apply | edits to `paper/return-base-rate-paper.md` | B2 reports done | Serialized after B1; human-guided triage of the 4 reports |
| A2b | EJIS response letter | EJIS decision email | Uses A2a template |
| D5 | Paper 3 draft (threshold model) | D2 + D4a done | |
| E4 | Paper 4 draft (cross-system) | E3 done (deferred) | |
| G2/G3/G4/G5 | Triad paper / manifesto essay / law synthesis / book spine | See §9 gates | Creative content stays human-voiced |

## 6. The `theory/` register (constitutional bridge)

`theory/` is **not corpus material**. Files there carry `PROPOSED` headers and become corpus conjectures/supplements only via **human admission** (RAT-1: c25s1; RAT-2: the D4a prediction) performed in a human-approved session that follows the constitution's admission procedure. This is how the program preregisters model predictions without recipes ever creating corpus files or touching `tracking:` blocks — the defect the adversarial review flagged as having "no constitutional home" is closed by this register.

## 7. Execution algebra

```
HUMAN REGISTER (ordered; outside all compounds):
  G1a ORCID×2 → G1b tectonic title_page.tex recompile → G1c co-author sign-off
      → A1 EJIS portal submission          [SUBMISSION_GUIDE.md, structural-waste/submission/]
  G1d arXiv endorsement check   G1e Scholar profile + site /research index
  RAT-1 admit c25s1   RAT-2 admit D4a prediction   B4b arXiv submit click

SESSION PRECONDITION: D1  ──feeds──▶ D2, D3, E2-review

COMPOUND EPI-NOW  (every layer type:"formula"; every recipe run_class:"infra"):
  L1 (parallel): H0 → then {B1, C3, E1, A2a, A3}
  L2:            B2-stats ∥ B2-field ∥ B2-validity ∥ B2-repro   [dep B1]
                 C1 [dep C3]     D2 [dep D1-file-exists]     E2 [dep B1]
  L3:            B4a [dep B1 + B2×4]   C2d [dep C1]   F1 [dep C1]
                 D3 [dep D1]           D4a [dep D2]
  L4:            B5 [dep B4a]
  Serialization: only B1 writes paper/return-base-rate-paper.md inside the compound;
                 B2-apply (session) follows outside it.
  compound { h0 ; parallel {b1,c3,e1,a2a,a3} ; parallel {b2s,b2f,b2v,b2r,c1,d2,e2} ;
             parallel {b4a,c2d,f1,d3,d4a} ; b5 }

DEFERRED COMPOUNDS (named stubs — compiled only when their trigger fires; never now):
  EPI-POSTGATE  ⇐ observatory logs C25 gate-event
                 (paper v2 results section, D4a-prediction-vs-outcome comparison,
                  D5 inputs, RAT verdict ratification support docs)
  EPI-REVISION  ⇐ EJIS decision email          (A2b support)
  EPI-PUBLIC    ⇐ ≥1 anchor public / C6 graduation (≥2026-07-12)
                 (G2/G3/G4 session-support material)
```

**No C25 sentinel recipe** — gate-events are observatory-owned (`AGENTS.md` §5); a second watcher would race the beat. Instead, H2 (below) adds one line to the weekly synthesis.

## 8. Locked decisions

1. All program recipes: `run_class: "infra"` (§1.3). 2. arXiv: primary **cs.SE**, cross-list **cs.AI**; license **CC BY 4.0** [human may override at B4b]; byline **Rashid Azarang** (identity decision already made in the EJIS kit — one scholarly identity everywhere). 3. `theory/` register semantics (§6). 4. Simulation may use numpy; `analyses/` stays stdlib. 5. E1 licensing column decides corpus eligibility before download. 6. No day-estimates on research phases — token-bound, gate-bound. 7. Weekly-synthesis line (H2, applied by the *human or beat*, not a recipe, since README is beat-owned): "if C25 n_post ≥ 120, alert: D4a admission window closing." 8. The four regime boundaries and the frozen number inventory (§4 B1) are program constants.

## 9. Gate table for the positioning pipeline

| Item | Gate (unblocking condition) |
|---|---|
| G2 triad paper | Anchor 1 first review round received |
| G3 manifesto essay | ≥1 anchor publicly available (arXiv counts) |
| G4 law synthesis | C6 graduated with fitted k (per exclusions §7) AND D5 drafted |
| G5 book spine | ≥2 papers public |
| E3/E4 | E1+E2 ratified AND D2 results reviewed |
| EPI-POSTGATE | observatory C25 gate-event packet |

## 10. What gets handed to scaffold

- **Compile:** H0, B1, C3, E1, A2a, A3, B2×4, C1, D2, E2, B4a, C2d, F1, D3, D4a, B5 — as the `EPI-NOW` compound above.
- **Recipe params (all):** `auth: rashid`, `model: claude-opus-4-8`, `backend: claude`, `permission_mode: bypassPermissions`, `run_class: "infra"`, `effort: xhigh` — except `max` on: B2×4, C1, D2, D3, D4a, F1.
- Workspaces: `/Users/rashid/Desktop/epistemics` for all phases except A2a/A3 (`/Users/rashid/Desktop/structural-waste`).
- The compiler applies `MAX_THINKING_TOKENS=63999`, completion keywords, and terminal `-verify` steps from the **Verify:** blocks; this document deliberately does not hand-write them.
- Every prompt embeds §1.9's escalation wording verbatim.
- **Do not compile:** anything in §5 (sessions), §7's human register, or the deferred compounds.

## 11. Manual-steps register (human-only; nothing here is a recipe)

1. G1a — register ORCID ×2 (rashid@mentu.ai; mazarang@itesm.mx) at orcid.org.
2. G1b — paste ORCIDs into `structural-waste/submission/title_page.tex`; `tectonic title_page.tex`.
3. G1c — co-author reads final PDF + cover letter; confirms byline + his degree line (Ph.D., City University, London, 1998).
4. A1 — EJIS portal submission per `structural-waste/submission/SUBMISSION_GUIDE.md` (SE/AE nominations from the live board).
5. G1d — arXiv endorsement check for cs.SE (first-time submitter).
6. B4b — arXiv submission click (category/license per §8).
7. RAT-1 / RAT-2 — corpus admission of `c25s1` and the D4a prediction (constitutional procedure; human session).
8. G1e — Google Scholar profile; rashidazarang.com/research index page.
9. H2 — add the weekly-synthesis alert line (or instruct the beat's prompt maintainer to).

## 12. Verification-commands appendix (per-phase DoD is the Verify: block; these are the program-level checks)

```bash
EX="--exclude-dir=okf --exclude-dir=.scratch_handoff --exclude-dir=__pycache__"
# 1. No recipe or doc instructs edits to frozen artifacts:
grep -rn $EX -E "corpus/(supported|refuted)|tracking:" docs/BUILD-epistemics-program-v1.md | grep -v "never"
# 2. Run-class rule present in every generated recipe (post-scaffold):
for f in .mentu/recipes/epi-*.json; do grep -L '"run_class": "infra"' "$f"; done   # expect empty
# 3. Post-first-run contamination check (read-only):
grep '"run_class"' ~/.mentu/training/cir-run-outcomes.jsonl | tail -50            # program runs must show infra
# 4. Frozen-file hash guard (before/after any epistemics phase):
shasum -a 256 corpus/conjectures/c25-return-intervention.md corpus/supported/*.md
# 5. Paper state after B1:
grep -c "{{artifact:" paper/return-base-rate-paper.md                              # 0
grep -c "does not yet exist" paper/return-base-rate-paper.md                       # 0
# 6. Simulation isolation:
grep -rn "\.mentu" simulation/ --include="*.py"                                    # no hits
```

---
*Authored 2026-07-02 by Fable 5 under the program mandate. This document pre-makes the judgment; the constitution (§1) outranks it; the source files outrank the quotes. When in doubt: escalate, never improvise.*
