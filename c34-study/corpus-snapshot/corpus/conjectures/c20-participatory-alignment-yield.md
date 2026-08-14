---
id: c20
name: participatory-alignment-yield
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/ci-os-the-operating-system.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/cir-memory-as-infrastructure.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/dcos-semantic-coordination.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/epistemic-computer.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/epistemic-engine-compiler.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/infrastructure-transformation.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/intelligence-as-infrastructure.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/participatory-epistemic-interfaces.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/recursive-epistemic-infrastructure.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/self-referential-infrastructure.md
verdict: null
---

# C20 - Participatory alignment yield

## Claim

Human participation invoked at explicit semantic boundaries should improve alignment,
correction, trust calibration, and downstream utility per unit of human attention
compared with autonomous execution or ad hoc review.

The claim is not that every human intervention helps. It is that participation becomes
scientifically useful only when captured as a contract: why the human was asked, what
semantic disagreement or risk existed, what option was chosen, how much attention it
cost, and what downstream outcome followed.

## Origin

The foundations folder repeats many already-admitted ideas: CIR as memory (C1/C9/C17),
DCOS contracts and conditional execution (C16), compiler semantics (C15), governed
evolution (C19), and epistemic-computer architecture (C18). The new residue is the
participatory layer: NarrativeSignal, PromptContract, LineagePatch, AgentManifest,
ArbitrationContract, ExecutionTraceBundle, ConceptHandshake, SemanticDiff,
AlignmentLedger, AttentionBudget, and ParticipationContract.

C20 keeps that residue as a measured human-agent alignment claim. The rest of the
stack language remains lineage, not evidence.

## Operationalization

**Datasets**:

- Future participation event logs:
  - `participation_id`, `run_id`, `artifact_id`, `contract_id`;
  - `participation_type` (`narrative_signal`, `prompt_contract`,
    `lineage_patch`, `arbitration`, `human_review`, `concept_handshake`,
    `semantic_diff`, `alignment_ledger_entry`, `approval`, `rejection`,
    `request_more_info`);
  - trigger source (`confidence_delta`, `semantic_mismatch`, `trust_boundary`,
    `ethical_boundary`, `resource_contention`, `explicit_user_request`);
  - candidate options shown to the human and default action;
  - attention cost: time, decision count, lineage depth, prompt/detail bytes;
  - semantic state before and after participation: handshake score, diff size,
    unresolved concepts, trust vector;
  - human action and rationale;
  - downstream execution result, correction/revert, trust update, and utility outcome.
- Current partial surfaces:
  - CIR has related but non-contractual kinds such as `approval`, `correction`,
    `correction.judge`, `prediction.judge`, `semantic_gate_eval`, `agent_spawn`,
    and `step_contract`.
  - `~/.mentu/desktop/approvals.json` records local desktop approvals, but not
    semantic-boundary triggers or downstream outcomes.
  - `~/.mentu/training/cir-run-outcomes.jsonl` has run outcomes, but no participation
    opportunity/decision linkage.

**Predeclared predictor**:

Participation-contract completeness score at decision time:

- `0`: no participation event; only outcome artifacts exist.
- `1`: human approval/review recorded without trigger or options.
- `2`: trigger and options recorded.
- `3`: trigger, options, human action, and attention cost recorded.
- `4`: semantic diff/handshake state and trust/confidence state recorded.
- `5`: all above plus downstream outcome, correction/revert, trust update, and
  utility linkage.

**Outcomes**:

- semantic alignment success and handshake miss rate;
- correction, revert, invalid-use, or trust-decrease rate;
- downstream execution success and utility;
- later read/use/citation or saved/acted-on response;
- attention ROI: useful outcome per human minute or decision;
- arbitration latency and default-action rate;
- unresolved semantic divergence after participation.

**Controls**:

- task class and risk class;
- run duration, cost, and step count;
- agent count and conflict count;
- trigger type and confidence delta;
- artifact type and workspace;
- human attention load during the window;
- C7 handle richness;
- C13 semantic redundancy;
- C15 compiler invocation readiness;
- C16 conditional activation selectivity;
- C19 governed-evolution completeness.

## Predictions (stated 2026-06-19, before C20 verdict analysis)

- **P1**: Boundary-triggered participation with semantic diff/handshake context will
  reduce later corrections and invalid uses compared with ad hoc approval.
- **P2**: Human review without trigger, options, or downstream linkage will show weak
  or negative attention ROI.
- **P3**: Participation will help most when confidence deltas, trust boundaries, or
  semantic mismatches are high, and least on low-risk routine execution.
- **P4**: Lineage patches that recompile affected reasoning paths should outperform
  free-form comments on later trust calibration and correction avoidance.
- **P5**: Excessive arbitration will reduce utility through attention burden even when
  individual decisions are locally correct.

## Falsification criteria

- Contract-complete participation has no positive association with correction
  reduction, alignment success, trust calibration, downstream utility, or attention ROI
  after controls -> **refuted**.
- Benefits disappear after C15/C16/C19 controls -> **revised** as compiler,
  activation, or governance quality rather than participation.
- Human participation improves correctness but costs more attention than its utility
  justifies across non-critical tasks -> **revised** toward a high-risk-only claim.
- Any verdict excluding ignored prompts, skipped reviews, timeouts, rejected patches, or
  default actions is invalid.

## Gate

C20 may produce a verdict only when all are true:

- participation-contract scoring rules are frozen before outcome modeling;
- at least 1,000 participation opportunities are logged, including skipped/defaulted
  opportunities;
- at least 300 invoked-human and 300 autonomous/ad hoc matched opportunities exist;
- each opportunity records trigger, options shown, default action, human action or
  timeout, attention cost, semantic state, trust/confidence state, and downstream
  outcome linkage;
- at least 150 semantic handshakes or semantic diffs are logged;
- at least 100 lineage patches or structured human corrections are logged;
- outcome windows cover at least 4 weeks;
- C7/C13/C15/C16/C19 controls are computable.

Current data has adjacent signals and approval traces, but not first-class
participation contracts, attention budgets, semantic handshakes/diffs, lineage patches,
or participation-to-outcome linkage. C20 is therefore readiness-gated.

## Known limitations

- Human participation is usually invoked for harder cases. Matching and trigger/risk
  controls are mandatory.
- Some participation value is negative prevention: avoiding harmful execution. Outcome
  classes must include prevented failures and default deferrals.
- Attention is part of the claim. A correct intervention can still fail C20 if it
  consumes more human attention than its downstream value justifies.
- Retrospective explanations do not count. The trigger, options, and semantic state
  must be captured before the decision.
