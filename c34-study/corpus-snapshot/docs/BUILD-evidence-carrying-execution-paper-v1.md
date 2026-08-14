# BUILD — Evidence-Carrying Execution (the platform-anchor paper) v1

**Date:** 2026-07-03
**Compiles with:** `/scaffold docs/BUILD-evidence-carrying-execution-paper-v1.md` (mechanical phases only — see §9 split)
**Depends on:** the four canons (`CANON-Compositional-Calculus.md`, `CANON-Execution-Model.md`, `CANON-CIR-Operational-Memory.md`, `CANON-Genesis-Key-Enforcement.md`) · the program BUILD (`docs/BUILD-epistemics-program-v1.md`, whose executor constitution this inherits) · `contribution-strategy-memo.md`
**Executor:** claude-opus-4-8 driving mentu recipes (compiled phases) + guided sessions (writing/formal phases). All judgment pre-made; where it can't be, the phase is a SESSION or HUMAN item.
**Working title:** *Evidence-Carrying Execution: A Calculus and Production System for Accountable Agent Orchestration.*

---

## 0. Scope & thesis

### 0.1 The one-sentence claim

> An agent-orchestration system in which **every execution transition is forced to co-produce cited evidence, trust is mechanically derived from observable execution (never self-reported), provenance survives composition, and the rules governing agents are tamper-evident inside the ledger the agents write to** — demonstrated in production, with quantified evidence that prompt-level governance fails where mechanical enforcement holds.

This is **one systems paper**, not four. The four canons supply the material; the paper is their composite. The contribution is the *coupling* (evidence⊗trust⊗provenance⊗governance under composition), not any single carrier — the individual carriers have prior art (§0.4).

### 0.2 Genre & venue (locked)

- **Genre:** systems / new-paradigm paper with a running artifact and honest empirics. Onward!, ICSE-SEIP, or FSE-Industry shaped. **arXiv first** (cs.SE primary, cs.AI cross-list).
- **Not** a formal-methods submission in v1 — the algebra is *descriptive*. A POPL/OOPSLA path exists later only if the optional formal core (§Phase F2, the uniqueness theorem) is completed; v1 does not depend on it.
- **Positioning clock:** the June-2026 survey *From Agent Traces to Trust* (arXiv:2606.04990) explicitly calls for systems that connect operational traces to semantic evidence relations — i.e. describes what this engine already runs. The field is converging here; this paper should reach arXiv before the gap closes. This is the **platform anchor** of the program's three-leg arc (science = return base rate · engine = this paper · theory = R_k model), prepared once Anchor 2 is on arXiv.

### 0.3 The paper's assets (what makes it more than a design doc)

1. **A four-carrier organizing frame** `σ:(E,K,T,S)→(E',K',T',S')` with **seven cross-carrier invariants** (`CANON-Compositional-Calculus` §5) — the spec.
2. **Honest operator laws**, including the ones that *fail*: par non-commutative for git state, challenge asymmetric, bind directional (§4 of the calculus canon). Publishing the failures is a credibility asset, not a weakness.
3. **The governance audit** — the empirical centerpiece: prompt-level governance leaked (canon claims 92 double-claims, 166 airlock breaches, 3,295 rogue ops, 799 unresolved actors), then a single mechanical gate (`Ledger.append` G1) closed it. **These numbers must be RE-DERIVED from production ledgers in this program (Phase E1) — the canon is not a citable source for a published number.**
4. **The usage-proof taxonomy** (useful/ignored/not_injected/unproven/broken) + the `mentu cir eval --matrix cir:on,off` harness (`CIREvalCommand.swift`, confirmed present) — an actual experiment the paper can run.
5. **Scale as evidence** — 150+ sequences, ~245K signals, ~3.9M relations, the Spectre compound (5 engines, 4 waves, one invocation). All **re-measured fresh** (Phase E2), never asserted from canon.

### 0.4 Prior art to cite (verify every one in-session, Phase L1 — none from memory)

- **Concurrent Kleene Algebra** (Hoare, Möller, Struth, Wehrman, CONCUR 2009) — the `(P,;,‖,ε)` near-semiring is CKA; the *exchange law* `(A‖B);(C‖D) ⊆ (A;C)‖(B;D)` is the free open question (does it hold per-carrier — evidence yes, git no?).
- **Kleene Algebra with Tests** (Kozen) — the Gate operator.
- **Truth Maintenance Systems** (Doyle JTMS 1979; de Kleer ATMS 1986) — citation-propagated confidence, contradiction records, degradation cascade are a production TMS.
- **Trust/subjective logic** (Jøsang) — trust propagation lineage.
- **W3C PROV-DM**, **PROV-AGENT** (arXiv:2508.02866), the **agent-traces-to-trust survey** (arXiv:2606.04990), the **scheduler-theoretic agent-graph** paper (arXiv:2604.11378) — the nearest neighbors this paper differentiates from.

### 0.5 Out of scope (v1) / keep OUT

- The "Law of Epistemic Acceleration" (`V(Fₙ) > ΣV(Sᵢ)`, `CANON-Execution-Model` §"Law of…") — this is C6's unproven territory; **it must not leak into this paper.** The paper reports the *mechanism* (evidence compounding across steps) descriptively, never as a proven law.
- Optimality of the epistemic constants (0.1 penalty, 1.05× reinforcement, 30-day half-life) — reported as empirically chosen, explicitly open.
- Any engine code change. This BUILD reads `mentu-complete` **static source, read-only**; it writes only paper artifacts.

---

## 1. Executor constitution (inherits the program BUILD §1; deltas below)

The full constitution is `docs/BUILD-epistemics-program-v1.md` §1. This paper adds/sharpens:

1. **Canon is not a citable number source.** Every quantitative claim in the paper (audit counts, signal/relation totals, sequence counts, eval results) must be **re-derived this program from the live ledgers / stores**, read-only, with a dataset digest. A canon-stated number may appear only as "reported in internal design records" and never as a headline result. Mismatch between canon and re-derived → report the re-derived value; note the delta in a footnote; do not edit the canon.
2. **Static-source reads only.** `mentu-complete` source is read read-only for grounding invariants to files/lines. **No engine edits, no builds that mutate state, no `mentu` CLI runs that write to the production ledger.**
3. **The eval experiment is quarantined.** `mentu cir eval --matrix cir:on,off` (Phase E3) creates runs. It MUST run in a **dedicated throwaway eval workspace** (`~/.mentu-eval-<date>/` or an explicit `--workspace`), never in `epistemics/`, `mentu-complete/`, or any workspace whose CIR is under measurement — otherwise it contaminates both the paper's own measurement and the epistemics C25 experiment. Every eval run is `run_class: infra`. If a dedicated workspace cannot be confirmed, **do not run the experiment** — mark it "future work" and ship the paper on the audit + scale evidence.
4. **Read-only ledger access pattern** (audit re-derivation): copy the production ledger JSONL to scratch, or read with `sqlite3 -readonly`; record sha256 + row count + date range; never write under any `.mentu`.
5. **Honesty-tag preservation.** The canon's `observed pattern / design principle / open hypothesis` tags are load-bearing scientific hedges. The paper must carry each claim at its canon-declared tag or weaker — never upgrade a hypothesis to a law. Grep the draft for "law", "prove", "guarantee" before submission (Phase W3).
6. Escalation triggers (inherit) + one new: **any re-derived audit number that materially contradicts the canon's claimed number** → escalation file, human decides framing before it enters the draft.

---

## 2. Target layout (NEW)

```
epistemics/
  paper/evidence-carrying-execution/          ← NEW (this paper's home)
    paper.md                                   (W-series draft; single source)
    arxiv/  paper.tex references.bib figs/     (W4 package)
    evidence/                                  ← re-derived numbers live here, immutable
      <date>-governance-audit.md   audit.py    (E1 — re-derives 92/166/3295/799)
      <date>-scale-census.md       census.py   (E2 — signals/relations/sequences)
      <date>-cir-eval.md           (E3, if quarantine confirmed; else "future work" stub)
      digests.json                             (sha256 + counts for every source read)
    lit/                                        ← L-series verified-citation records
      <date>-prior-art-verified.json           (CKA, KAT, TMS, PROV, surveys — all checked)
    formal/                                     ← F-series
      invariant-spec.md            (F1 — 7 invariants grounded to file:line, from static read)
      operator-laws.md             (F1 — what holds / what fails, with the code evidence)
      uniqueness-note.md           (F2, OPTIONAL — evaluation-order theorem; session)
    referee/  B-<lens>.md                       (adversarial pass, report-only)
  docs/escalations/                             (shared; canon/number conflicts land here)
```

---

## 3. Build phases

| Phase | Title | Effort | Gate (→ verify assertion) |
|---|---|---|---|
| L1 | Prior-art verification | xhigh | `lit/<date>-prior-art-verified.json` exists; every §0.4 work has a resolved DOI/arXiv-id + one-line "what it is / how we differ"; 0 unverified |
| E1 | Governance-audit re-derivation | max | `evidence/audit.py` (read-only, digest header) + report; re-derives the four counts from live ledgers; each number carries a source digest; canon-vs-derived deltas noted |
| E2 | Scale census | xhigh | `evidence/census.py` + report; fresh signal/relation/sequence totals + date range; digest recorded; supersedes canon's ~245K/~3.9M |
| E3 | CIR-eval experiment (quarantined) | max | EITHER `evidence/<date>-cir-eval.md` with matrix results from a **confirmed dedicated eval workspace** (all runs `run_class: infra`) OR a "future work" stub stating why quarantine wasn't confirmed |
| F1 | Invariant + operator spec (from static source) | max | `formal/invariant-spec.md` grounds all 7 invariants to `file:line` in `mentu-complete` (read-only); `formal/operator-laws.md` states holds/fails with code evidence incl. the 3 failures |
| B | Referee lenses ×3 (report-only) | max | `referee/B-formal.md`, `B-systems.md`, `B-claims.md` exist; fixed rubric; `paper.md` byte-identical this phase |
| W4 | arXiv LaTeX package | xhigh | `paper/.../arxiv/` compiles (tectonic exit 0); no `{{artifact:`/`artifact:`; abstract ≤1,920 chars; byline "Rashid Azarang"; every number traces to `evidence/` or `lit/` |

Sessions (not compiled, §9): **W1** outline+claims ledger, **W2** full draft, **W3** honesty-tag + fix-application pass, **F2** optional uniqueness theorem, **B-apply** referee triage.

---

## 4. Phase details

### L1 — Prior-art verification
- File: `paper/evidence-carrying-execution/lit/<date>-prior-art-verified.json`
- Change: for each §0.4 work, resolve identifier (Crossref/arXiv API, in-session) and record `{key, canonical_title, authors, year, id, one_line_what_it_is, one_line_how_we_differ, verified:true}`. The differentiation lines are the paper's related-work spine. **Never cite from memory; anything unresolved → escalation, not a guess.**
- Why: the paper's novelty claim ("nobody published the composite") is only as strong as its command of CKA/TMS/PROV; a mis-cited foundation is a desk-reject.
**Verify:** JSON exists; ≥8 entries; every entry `verified:true` with a non-empty differ-line; no `null` ids.

### E1 — Governance-audit re-derivation (the empirical centerpiece)
- File: `paper/evidence-carrying-execution/evidence/audit.py`
- Change: read-only script re-deriving, from the production ledger(s) named in `CANON-Genesis-Key-Enforcement` grounding (`Ledger.swift` JSONL + the SQLite materialized view), the four pre-enforcement pathologies: (a) double-claims (same commitment claimed by same actor >1× across multi-step recipes), (b) accountability-airlock breaches (close/approve by `agent:` actors), (c) rogue non-canonical operations (ops outside the 9 v2.0 ops — esp. `cancel`), (d) unresolved actors (`"user"` with no `type:name`). Digest header first (files, sha256, row counts, date range). Snapshot pattern per §1.4.
- File: `evidence/<date>-governance-audit.md`
- Change: report each count with its digest; a "before mechanical gate vs after" split if the ledger's G1-enabled boundary is identifiable; a canon-vs-derived table with deltas footnoted. If a count materially differs from canon (92/166/3,295/799) → escalation before it enters the paper.
- Why: "prompt-level governance fails, mechanical enforcement works" is the paper's most quotable claim and the agent-safety field's open question — it must rest on a number the reviewer can, in principle, reproduce, not on a canon assertion.
**Verify:** script exists, stdlib/`sqlite3 -readonly` only (grep import allowlist), digest header present; report has all four counts + a canon-vs-derived table.

### E2 — Scale census
- File: `evidence/census.py` + `evidence/<date>-scale-census.md`
- Change: fresh counts — total signals, total relations, distinct recipe runs / sequences, contradiction records, patterns, date range — from the live CIR store (`CIRStore.swift` schema v7, `sqlite3 -readonly`). Digest recorded. These supersede the canon's ~245K/~3.9M in the paper.
- Why: a paper states current, reproducible scale; canon numbers age.
**Verify:** script + report exist; report states a captured-at timestamp and a source sha256; numbers are non-zero and internally consistent (relations ≥ signals).

### E3 — CIR-eval experiment (quarantined; conditional)
- File: `evidence/<date>-cir-eval.md` OR a future-work stub.
- Change: **first confirm a dedicated eval workspace** (fresh `mentu init` in a throwaway dir; NOT epistemics/mentu-complete/any measured workspace). If confirmed: run `mentu cir eval run <recipe> --trials N --verifier <v> --matrix cir:on,off` with every run `run_class: infra`; record verifier success, repeated-work count, contradiction alerts, cost, time, injected/used IDs, missing-footer count, outcome label — the measures the canon's Evaluation section names. If quarantine cannot be confirmed → write the stub: "CIR-as-intervention A/B deferred; harness exists (`CIREvalCommand.swift`); not run to avoid contaminating the return-base-rate experiment (C25)." Ship the paper either way.
- Why: an on/off experiment elevates the paper from description to evaluation — but not at the cost of the sibling science.
**Verify:** either a results doc whose runs are all `infra` and whose workspace ≠ any measured workspace, OR a stub naming the contamination reason and the harness file.

### F1 — Invariant + operator spec (static-source grounding)
- File: `formal/invariant-spec.md`
- Change: restate the seven invariants (Evidence Accompaniment, Mechanical Trust, Temporal Monotonicity, Provenance Preservation, Contradiction Legibility, Budget Boundedness, Closure) each grounded to `mentu-complete` `file:line` read read-only (e.g. Invariant 1 → `SequenceRunner`/`CIRMemory.ingest`; Invariant 2 → `TrustComputer.swift:67` seven weights; Invariant 4 → `Ledger.swift` merkle + K1). Carry each at its canon honesty-tag.
- File: `formal/operator-laws.md`
- Change: the six operators with the descriptive laws — **and the three documented failures** (par ≠ commutative for git; challenge asymmetric; bind directional), each with its code evidence (`FleetRunner` merge lock; `MENTU_ADVERSARIAL_EVIDENCE` forwarding). State the CKA exchange-law question as explicitly open, per-carrier.
- Why: this is the paper's §"The Calculus"; grounding every claim to code is what separates it from "category theory cosplay" (the canon's own phrase — keep the disclaimer).
**Verify:** both files exist; ≥7 invariants each with a `file:line`; ≥3 failure laws with code evidence; contains the exchange-law open question and the cosplay disclaimer.

### B — Referee lenses ×3 (report-only, parallel)
- Files: `referee/B-formal.md` (is the CKA/TMS positioning correct; is any "law" overclaimed?), `referee/B-systems.md` (is the artifact evaluation sufficient; are the audit numbers reproducible as described?), `referee/B-claims.md` (does every sentence's strength match its evidence tag; any acceleration-law leak?).
- Change: fixed rubric per finding — claim | severity | quoted line | fix. Report-only; `paper.md` untouched.
**Verify:** 3 files exist with rubric columns; `git diff --stat paper.md` empty this phase.

### W4 — arXiv package
- File: `paper/evidence-carrying-execution/arxiv/paper.tex` (+ `references.bib` from L1, figs)
- Change: pandoc+tectonic (`/opt/homebrew/bin`); byline **Rashid Azarang** (Mentu, San Pedro Garza García, Nuevo León, Mexico; rashid@mentu.ai); abstract ≤1,920 chars; every headline number cites an `evidence/` digest; every prior-art cite from `lit/`.
**Verify:** `tectonic … exit 0`; `grep -c "artifact:"`=0; abstract char-count ≤1,920; "Rashid Azarang" present.

---

## 5. Sessions (not compiled)

| Session | Deliverable | Gate to start |
|---|---|---|
| W1 | `paper.md` outline + a claims-ledger (every claim → its evidence source → its honesty tag) | L1 + E1 + E2 done |
| W2 | Full draft | W1 + F1 done (E3/B feed later) |
| W3 | Honesty-tag audit + apply B + apply E3 result | B + E3 done |
| F2 (optional) | `formal/uniqueness-note.md`: prove the §11 order (execute→record→trust→recalibrate→schedule) is the unique order satisfying Invariants 1–2 | W2 done; only if pursuing a formal-venue path |
| B-apply | draft edits from the 3 referee reports | B done |

## 6. Execution algebra

```
SESSION SPINE:  W1 ─▶ W2 ─▶ W3 ─▶ (F2 optional)
COMPOUND ECX-NOW (all recipes run_class:infra):
  L1a: L1  (prior-art)   ∥  F1 (static-source spec)          [independent]
  L1b: E1  (audit)       ∥  E2 (census)                       [independent; read-only]
  L2:  E3  (eval)         [dep: dedicated-workspace confirmed; else stub]
       B-formal ∥ B-systems ∥ B-claims   [dep: F1 + E1 + E2 exist as draftable inputs]
  L3:  W4  (arxiv)        [dep: W3 session complete — so W4 compiles AFTER the session spine]
  gate: W4 requires the paper.md the sessions produce.
```
No deferred compounds; this is a single-paper build. External-clock item: **arXiv submit click = HUMAN** (endorsement for cs.SE if first-time).

## 7. Locked decisions

1. One paper, systems genre, arXiv cs.SE/cs.AI, CC BY 4.0 [human may override]. 2. Byline "Rashid Azarang" (program-wide identity). 3. Every number re-derived (§1.1); canon numbers never headline. 4. Acceleration law stays out (§0.5). 5. Eval experiment quarantined or deferred (§1.3). 6. Honesty tags preserved or weakened, never upgraded. 7. Reads `mentu-complete` static, writes only under `paper/evidence-carrying-execution/`.

## 8. Manual-steps register (human-only)

1. Confirm/authorize the dedicated eval workspace for E3 (or approve deferral).
2. Decide whether to pursue F2 (formal venue) — changes nothing in v1 if declined.
3. arXiv endorsement check (cs.SE, first-time submitter).
4. arXiv submit click (category/license per §7).
5. Sequencing gate: **do not start W-series until Anchor 2 (return-base-rate) is on arXiv** — platform anchor follows the science anchor (program sequencing law).

## 9. What gets handed to scaffold

- **Compile:** L1, E1, E2, E3, F1, B×3, W4 (the `ECX-NOW` compound; all `run_class:infra`; params `auth: rashid`, `model: claude-opus-4-8`, `backend: claude`, `permission_mode: bypassPermissions`, `effort: max` on E1/E3/F1/B, else `xhigh`).
- **Sessions (never compiled):** W1, W2, W3, F2, B-apply.
- Workspace: `/Users/rashid/Desktop/epistemics` (reads `mentu-complete` by absolute path, read-only).
- Compiler applies `MAX_THINKING_TOKENS=63999`, completion keywords, terminal `-verify` steps from the Verify blocks. Escalation wording (program §1.9) embedded in every prompt.

## 10. Verification (of the BUILD doc + its outputs)

```bash
EX="--exclude-dir=okf --exclude-dir=.build --exclude-dir=__pycache__"
# every referenced canon + engine file exists (read-only targets):
for f in CANON-Compositional-Calculus CANON-Execution-Model CANON-CIR-Operational-Memory CANON-Genesis-Key-Enforcement; do
  test -f "/Users/rashid/Desktop/mentu-core-workspace/children/spine/mentu-complete/docs/canon/$f.md" || echo "MISSING $f"; done
test -f "/Users/rashid/Desktop/mentu-core-workspace/children/spine/mentu-complete/mentu-engine/Sources/MentuEngine/CIREvalCommand.swift" || echo "MISSING eval harness"
# acceleration-law leak guard (must stay OUT of the paper):
grep -rin "law of epistemic acceleration\|V(F" paper/evidence-carrying-execution/paper.md   # expect empty
# canon-number-as-headline guard (numbers must cite evidence/, not canon):
grep -rn "245K\|3.9M\|92 \|166 \|3,295" paper/evidence-carrying-execution/paper.md | grep -vi "evidence/"   # review each hit
# eval quarantine check (if E3 ran): no eval run in a measured workspace
grep -l "workspace.*epistemics\|workspace.*mentu-complete" paper/evidence-carrying-execution/evidence/*cir-eval* 2>/dev/null  # expect empty
```

---
*Authored 2026-07-03 by Fable 5. One paper: the composite is the contribution, the re-derived numbers are the proof, the honest failures are the credibility. Canon supplies material, never citations. When canon and the ledger disagree, the ledger wins — and you escalate before you write it down.*
