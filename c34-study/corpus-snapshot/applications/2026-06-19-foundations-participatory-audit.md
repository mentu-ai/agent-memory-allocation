# Foundations participatory audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/ese/engine/foundations/`

No predecessor files were edited.

## Decision

Admit **C20 participatory alignment yield**:
`corpus/conjectures/c20-participatory-alignment-yield.md`.

The folder repeats several claims already admitted elsewhere: CIR memory, DCOS
contracts, CI-OS orchestration, compiler semantics, recursive infrastructure, governed
evolution, and the Epistemic Computer stack. The new scientific residue is narrower:
structured human participation at semantic boundaries should improve alignment and
downstream utility per unit human attention.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| CIR as active memory | **Already covered** | C1/C9/C17 carry the measurable return, pattern, and processing residues. |
| DCOS epistemic contracts | **C16/C20 lineage** | Conditional mode selection remains C16; human arbitration and participation contracts enter C20. |
| CI-OS cognitive resource management | **C20 lineage** | Attention budget and trust-mediated participation become measurable C20 predictors. |
| Epistemic Engine compiler | **Already covered by C15** | Compiler-readiness and validation belong to C15 unless tied to human participation outcomes. |
| Recursive/self-referential infrastructure | **C19/C20 lineage** | Governed system evolution stays C19; participatory feedback into that evolution is C20. |
| Participatory epistemic interfaces | **Admitted as C20** | Has explicit primitives, telemetry, and metrics: prompt contracts, lineage patches, arbitration, handshakes, semantic diffs, attention ROI. |
| Post-agent intelligence / collective intelligence endpoint | **Excluded as evidence** | Architecture destiny language is not an empirical result. |

## Live readiness digest

`analyses/c20-participatory-alignment-yield/analyze.py` checks source vocabulary,
CIR signal kinds, desktop approvals, and run outcomes.

Current source snapshot:

- source files: 10;
- logical source lines: 10,517;
- source term counts: arbitration 53, contract/trace 205, infrastructure stack 740,
  multi-agent 86, participation 82, semantic alignment 101, telemetry/metrics 72,
  trust/attention 24;
- source coverage: all 10 files contain infrastructure-stack language; 8 contain
  semantic-alignment language; 7 contain contract/trace and telemetry/metrics
  language; 6 contain arbitration language; 5 contain participation and multi-agent
  language; 4 contain trust/attention language.

Current live substrate is adjacent but not verdict-ready:

- desktop approvals file exists with 5 entries, all carrying grants;
- run outcome rows: 629;
- run rows with participation-adjacent terms: `judge` 11, `approval` 5, `contract`
  4, `review` 3;
- participation-adjacent CIR kinds: `agent_spawn` 1,490; `correction.judge` 630;
  `prediction.judge` 619; `correction` 215; `step_contract` 111;
  `semantic_gate_eval` 104; `formula_feedback` 94; `correction.perceive` 85;
  `agent_complete` 36; `agent_event` 33; `platform_agent_created` 6; `approval` 3;
  `platform_subagent` 3.

The blocker is structural: current records do not log participation opportunities,
skipped/defaulted opportunities, trigger conditions, options shown, attention cost,
semantic handshakes/diffs, lineage patches, trust state, or participation-to-outcome
linkage. The analyzer found 0 exact participation events.

## Next push

Add a first-class `participation_contract` event for human-agent boundary decisions:

- `participation_id`
- `run_id`
- `artifact_id`
- `contract_id`
- `participation_type`
- `trigger_source`
- `trigger_metrics`
- `candidate_options`
- `default_action`
- `human_action`
- `human_rationale`
- `attention_cost`
- `semantic_state_before`
- `semantic_state_after`
- `trust_state_before`
- `trust_state_after`
- `linked_execution_id`
- `linked_correction_ids`
- `linked_outcome_ids`

Most important: log skipped, timed-out, rejected, and defaulted participation
opportunities. Otherwise the corpus will only measure visible approvals, which is
exactly the review theater C20 is designed to prevent.
