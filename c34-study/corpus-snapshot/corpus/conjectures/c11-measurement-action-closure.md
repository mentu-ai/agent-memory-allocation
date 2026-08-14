---
id: c11
name: measurement-action-closure
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/ese/science/epistemic-thermodynamics/anti-patterns/metric-mirage-canonical-source.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/science/behavioral-intelligence/anti-patterns/metric-mirage.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/science/knowledge-architecture/anti-patterns/dashboard-theater.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/science/knowledge-architecture/protocols/cir-canonical-source.md
verdict: null
---

# C11 - Measurement-action closure

## Claim

Measurement only improves a knowledge system when it closes into a response path.
Signals, verdicts, dashboards, gates, and evaluation packets that do not cause or
route action tend to become ritual. Measurement families with explicit response
contracts should later show shorter closure latency, lower recurrence, and better
reliability than measurement families that only accumulate observations.

This conjecture is the measurable residue of Metric Mirage and Dashboard Theater.
It does not claim that every measurement must cause immediate work. It asks whether
the system has a traceable route from observation to response when response is needed.

## Origin

The science corpus repeatedly names a failure mode: data presentation and metric
collection can create the appearance of intelligence while decisions and behavior
remain unchanged. The operational claim is smaller and harder: if a measurement
event cannot be linked to a downstream response, it should not be counted as a
closed feedback loop.

## Operationalization

**Datasets**:

- `~/.mentu/cir.db`, read-only:
  - `signals.kind`, `signals.ts`, `signals.run_id`, `signals.workspace`,
    `signals.summary`, and `signals.body`;
  - `relations.source_id`, `relations.target_id`, `relations.relation_type`.
- `~/.mentu/training/cir-run-outcomes.jsonl`, read-only, for later recurrence and
  reliability outcomes by run and recipe family.

**Measurement events**:

- `semantic_gate_eval`
- `cir_run_outcome`
- `verdict`
- `gate_decision`
- `sentinel_triggered`
- `sentinel_escalated`
- `sentinel_resolved`
- `temporal_result`
- `correction.judge`
- `prediction.judge`
- `relevance_verdict`

**Action proxies for readiness only**:

- `git_commit`
- `commitment`
- `step_contract`
- `step_closure`
- `formula_feedback`
- `promotion`
- `ratchet`
- `correction`
- `reflection`
- `sentinel_resolved`
- `sentinel_escalated`

Temporal proximity to these proxies is diagnostic context, not proof. A verdict
requires explicit causal edges.

**Closure edge requirement**:

The first verdict-producing analyzer must use explicit relation types or signal-body
fields that mean one of:

- measurement caused action;
- action responded to measurement;
- action resolved measurement;
- action escalated measurement into a tracked obligation.

Run-id adjacency alone may not support or refute the conjecture.

**Outcomes**:

- closure latency from measurement to first caused action;
- unresolved measurement age;
- recurrence of the same measurement family after closure;
- later run success, warning/failure outcome, and step ratio.

**Controls**:

- measurement family;
- recipe family;
- workspace;
- week/cohort;
- workload/step count;
- C2 friction surface;
- C10 structure debt where workspace identity is uncertain.

## Predictions (stated 2026-06-19, before verdict analysis)

- **P1**: Measurement families with explicit response contracts will have lower
  recurrence after first response than families without response contracts.
- **P2**: Semantic gates and sentinels that close into tracked actions will predict
  better next-run reliability than gates/sentinels with no traceable response.
- **P3**: High measurement volume without closure edges will predict lower
  production per measurement unit, even if raw signal count rises.
- **P4**: The effect of closure will be strongest for warning/failure measurements
  and weakest for passive periodic telemetry.

## Falsification criteria

- Explicitly closed measurements do not predict recurrence suppression, closure
  latency improvement, or later reliability after controls -> **refuted**.
- Apparent closure benefits disappear after controlling for recipe family or
  workspace maturity -> **revised** as maturity confounding.
- Closure edges mostly describe bookkeeping after action already happened -> **revised**
  as attribution hygiene, not measurement-action closure.
- Any verdict based only on timestamp adjacency is invalid.

## Gate

C11 may produce a verdict only when all are true:

- at least 300 measurement events in scope;
- at least 100 action events in scope;
- at least one explicit closure relation or signal field exists before outcome
  comparison;
- closure edges are computed before recurrence/reliability outcomes;
- at least 8 weeks of post-closure outcome history;
- C2 and C10 controls are available for the same window.

The current corpus has measurement and action substrates, but no explicit causal
closure edge. C11 is therefore readiness-only today.

## Known limitations

- Some measurements are intentionally passive and should not cause action.
- Action can happen outside CIR. The conjecture only measures instrumented closure.
- A response contract can be wrong; closure is necessary for feedback, not sufficient
  for wisdom.
- Measurement-action closure overlaps C8 guardrail dividends but is distinct: C8 asks
  whether predeclared gates pay back; C11 asks whether observed signals route into
  traceable response.
