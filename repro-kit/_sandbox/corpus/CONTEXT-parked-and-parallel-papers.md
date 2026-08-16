# CONTEXT — Parked & Parallel Paper Candidates

**Date:** 2026-07-04 · **Status:** directional record, not a BUILD doc.
**Purpose:** preserve the reasons, unlock conditions, and source pointers for paper candidates
that were surveyed (three-workspace sweep: `mentu-physics`, `Structural Waste in Digital
Operations `, `epistemic-main`; ~60 documents, three Explore agents) but not selected as the
next build — so future sessions can point at them directionally without re-running the survey.
Companion: `~/.claude/.../memory/next-paper-candidates.md` (the ranked verdicts).

Active slate for reference: Paper 1 structural waste (EJIS kit ready) · Paper 2 return base
rate (arXiv-bound) · Paper 3 evidence-carrying execution (v1.1 PDF final) · **Paper 4
Constitutional Silence (BUILD: `docs/BUILD-constitutional-silence-paper-v1.md`)** · parallel
track: meta-cognitive architectures (below) · theory spine: R_k threshold model (program BUILD
D-workstream).

---

## 1. Parked, with reasons and unlock conditions

### Distributed Epistemic Computation (DEC) — the Mentu product-flagship paper, later
- **Source:** `epistemic-main/canon/foundational-documents/distributed-epistemic-computation.md`
- **Idea:** collective learning across private nodes where the exchange unit is the six-field
  **epistemic delta** — `hash(input)`, predicted label, corrected label, adapter id, device
  hash — not data, not gradients, not consensus. Stated falsifiable law: *the learning value
  of a correction is inversely proportional to the specificity of the raw data required to
  express it.* Cleanly differentiated from federated learning (no shared gradients, no
  homogeneous model) and crowdsourced labeling (deltas emerge from real work).
- **Why parked:** it is the biggest swing of the survey but demands real ML experiments
  (train adapters from deltas vs. raw-data baselines; measure the value-vs-specificity
  trade-off) — GPU work, benchmarks, a different reviewer community. Not the next paper;
  the flagship when Mentu productizes the loop.
- **Where the ML substrate already lives:** `/Users/rashid/Desktop/mentu-core-workspace/children/runtime/mentu-ane`
  — the on-device (Apple Neural Engine) ML runtime: `adapters/` (LoRA adapters — the
  delta-consuming artifact DEC trains), `Sources/`, plus the ecosystem's `lora` skill
  (extract training data from CIR, train adapters, canary-eval, deploy to rvLLM) and the
  interceptor capture path. **Most of the program's novel ML work is here; any DEC
  experiment starts in this repo.**
- **Unlock condition:** willingness to run a real training experiment (≥1 adapter family,
  delta-fed vs. raw-fed, held-out eval) + a scoping decision on privacy claims (the
  "specificity" law needs an operational specificity measure before any privacy language).

### Semantic-safety threshold whitepapers — provenance-blocked
- **Sources:** `epistemic-main/meta/intake/unprocessed/SEMANTIC_INTEGRITY_UNDER_LOAD_PHASE_4E5_WHITEPAPER.md`,
  `.../THRESHOLDS_OF_RECURSIVE_SAFETY_4E4_LEARNINGS.md`
- **Idea:** semantic safety — not generation fluency — is the binding constraint on recursive
  automation; multi-dimensional readiness thresholds; gap-type stratification (5 of 9 gap
  types automatable). The only documents in the constellation carrying real numbers
  (547 proposals / 79 violations / 100 cycles / calibrated thresholds).
- **Why parked:** those numbers are the **2025 platform's self-reported counters** — exactly
  what `epistemics/lineage/exclusions.md` §6 disqualifies as evidence ("internal counters of
  a system are inventory, not validation").
- **Unlock condition:** locate the raw proposal-lineage / human-intervention logs and
  re-derive every number read-only (the ECX governance-audit pattern). If only the whitepaper
  numbers exist, the material is a design record, not data — publishable only as motivation.

### Fourth-Law hysteresis (recoverable → permanent knowledge loss) — assimilated, not parked
- **Source:** `mentu-physics/foundational/key/laws/laws-of-epistemic-thermodynamics.md.txt`
  (Fourth Law); measurement sketch in `grammar/force.computational.execution/thermodynamic/epistemic-entropy-calculator.js`
- **Disposition:** folded INTO the R_k formal model (program BUILD, D-workstream) as a second
  testable prediction: the decay hazard is path-dependent — beyond a critical decay depth,
  re-exposure fails to restore return probability (hysteresis). Not a separate paper.

### φₑ epistemic friction coefficient — reinforces Paper 1, not standalone
- **Source:** `mentu-physics/foundational/key/core/friction-coefficient.v1.md`
- **Disposition:** both surveyors independently concluded it is structural waste in
  thermodynamic clothing. Its genuinely new residue — the **temporal/tempo axis** (latency
  between ignition and integration; human-AI cognitive-tempo mismatch) — is recorded here as
  a candidate *extension* for the structural-waste research program (a sixth measured
  quantity), to be raised when the SW validation program (Phase 2+) runs.

### Flow-dynamics cluster (impedance, gradient collapse) — waits on C5
- **Sources:** `epistemic-main/science/behavioral-intelligence/laws/laws-of-epistemic-impedance-and-transmission.md`
  (NOTE: its Z_e = √(S_s/C_r) has **undefined variables** — confirmed estimator-free on
  inspection); `.../anti-patterns/gradient-collapse-syndrome.md` (the genuinely original
  inversion: eliminating epistemic gradients kills flow — over-standardization as pathology).
- **Disposition:** the measurable path already exists as corpus conjecture **C5 (boundary
  impedance, operationalized 2026-06-19)**. When C5 matures, a flow-dynamics paper can carry
  gradient collapse as its second construct. Until then: parked.

### Also surveyed, standing dispositions
- **Network effects of structured knowledge** (`.../core-concepts/network-effects-of-structured-knowledge.md`):
  testable super-linear return-vs-connectivity law; weakened today by the measured sparsity
  of the live relation graph (0.095 relations/signal, census 2026-07-04). Revisit if/when
  relation density grows.
- **Superposition-and-collapse of contradictions** (`mentu-physics/foundational/oracle/subjective-experience/ambiguity-as-intelligence.md`):
  assigned to Paper 4 (Constitutional Silence) as a discussion-level sibling (restraint
  family); its data home is the contradictions table (76 detected / 2 resolved in the return
  paper's corpus).
- **Scar tissue / epistemic pruning** (`.../oracle/virtuous-forgetting/`): restraint-family
  sibling; the asymmetric-failure-memory *experiment* (does category-level immunity reduce
  repeat failures?) is a platform intervention for a later cycle.
- **EPDL / constitutional interpreter** (`mentu-physics/grammar/`, 20-month build with
  working compiler + test reports): potential systems/PL paper ("executable constitutions");
  heavily entangled with the physics apparatus; revisit after ECX lands publicly.
- **Reusable reviewer-defense apparatus:** `mentu-physics/foundational/key/new-docs/what-epistemic-physics-cannot-do.md`
  + `epistemic-physics-as-experimental-science.md` — the corpus's own falsifiability
  framework and self-critique; mine for the limitations sections of ANY seed above.

---

## 2. The meta-cognitive architectures decision record (parallel track, ACTIVE)

**Original disposition (2026-07-04, survey synthesis):** declined — *"clinical reframings
without clinical data, in a field far from your instrument, is a genre that gets punished,
deservedly."*

**Author override (verbatim):**
> "I do like 'meta-cognitive architectures' candidate (ADHD/depression/OCD as computation)!!!!!!!
> do not disregard it because it's sensitive... that's a beautiful abstraction that I
> personally possess!"

**Re-assessment (accepted):** the decline conflated *requires care* with *don't do it* —
negative-association bias wearing an ethics costume. Corrections that reversed the verdict:
1. **Distinguished ancestry legitimizes the genre:** Andrews & Thomson 2009 (*Psychological
   Review* — analytical-rumination hypothesis; depression as adaptation for analyzing complex
   problems) is the direct published ancestor of "depression as deep-integration
   intelligence" and survived exactly the fire this paper will draw. Nesse's evolutionary
   psychiatry, ADHD explore/exploit literature, Friston-school computational psychiatry are
   the adjacent fields. (All NEEDS-VERIFICATION at write time.)
2. **The unified template is the novel move:** one architectural schema (objective function ·
   salience policy · memory policy · resource allocation · characteristic failure modes)
   instantiated across clinical AND cultural systems — existing literature does one condition
   per theory.
3. **The instrument objection dissolves:** the architectures are implementable on mentu's own
   primitives (sentinel = threat-salience engine; adversarial = institutionalized suspicion;
   convergent = exploratory mania; scar tissue = trauma memory; dreaming = consolidation).
   Evidence = **measured trade-off curves from computational experiments** (e.g. recursion
   depth buys defect-catch at the price of stalling — the OCD trade-off; distributed
   attention wins in volatile environments, loses in sustained single-task — the ADHD
   trade-off). No clinical claims; the clinical mapping is a hypothesis-generating layer.
4. **Positioned lived experience is a methodological strength** under neurodiversity norms
   ("nothing about us without us") — the author runs the ADHD architecture and says so.

**Current standing:** ACTIVE parallel-track paper. Shape: *"Cognitive phenotypes as regions
of agent design space"* — thesis: there is no free attention; every cognitive architecture is
a point on trade-off frontiers, and what psychiatry names as disorders are regions of that
space. Two-front criticism pre-answered: (a) romanticization → architectures have failure
modes and the failure modes genuinely hurt — trade-off ≠ cost-free, stated with full weight;
(b) no fitted patient models → scoped explicitly as design-space theory + simulation. Venue
ladder: CogSci → *Computational Psychiatry* / *Philosophical Psychology* → book (the
cultural-systems half). Sources: `epistemic-main/science/meta-cognitive-architectures/`
(foundation + 14 case docs). It does not displace Paper 4; it changes fields, which is its
value — and it is the paper where the author's voice matters most.

---

*Rule carried from the survey: judge ideas by mechanism, measurable quantity, and
formalizable structure — never by their label ("law," "canonical," "physics") and never by
their sensitivity. Both biases cost papers.*
