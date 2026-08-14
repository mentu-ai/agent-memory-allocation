---
id: c30
name: staged-graph-admission
status: operationalized
registered: 2026-07-24
lineage:
  - /Users/rashid/Desktop/mentu-complete/docs/INTENT-admitted-execution-graphs.md
  - /Users/rashid/Desktop/mentu-complete/docs/BUILD-admitted-execution-graphs-v1.md
  - /Users/rashid/mentu-home/skill-library/.claude/skills/scaffold/SKILL.md
  - corpus/supported/c29-curation-vs-search-sufficiency.md
verdict: pending
---

# C30 — Staged graph admission

## Claim

Agent execution policies are better described along independent graph-lifecycle
axes than as separate "static", "dynamic", and "hybrid" runtimes:

1. **construction time** — a graph is declared before the task or synthesized
   from repository state at task time;
2. **freeze boundary** — construction and execution are either continuous, or
   separated by an addressable immutable artifact;
3. **authoring method** — direct authoring or scaffold-like
   orient/decompose/gate authoring; and
4. **execution substrate** — the admitted runner that enacts the qualified
   graph.

On this model, a hybrid policy is not a third runtime. It is dynamic
construction followed by an explicit freeze-and-admit boundary, then execution
through the same runner used for persistent recipes. This staging should retain
task-time discovery while removing planner stochasticity from the execution
invocation and making the inspected graph reproducible and reusable.

The narrower empirical claim is: for matched eligible tasks, staged hybrid
graphs preserve exact executable identity from inspection to admission, require
no planner dispatch during execution, and amortize their one-time planning cost
when reused. This conjecture does **not** assume that scaffold authoring produces
better plans, that hybrid execution produces better task outcomes, or that
static recipes are obsolete.

## Definitions (frozen at registration)

- **Static (S)**: a persistent recipe and prompts exist before the experimental
  task invocation. Execution performs zero graph-planner dispatches.
- **Dynamic one-shot (D)**: one task-time planner dispatch constructs a graph;
  qualification and execution continue in the same invocation without an
  operator-visible freeze boundary.
- **Staged hybrid (H)**: one task-time planner dispatch constructs a graph in
  plan-only mode; the canonical plan is saved and inspected; a later invocation
  requalifies and executes those exact bytes with zero planner dispatches.
- **Scaffold profile**: an authoring frontend that orients and decomposes before
  emitting a candidate graph. It is neither a graph node nor an authority
  source. The primary H arm uses this profile; a direct-profile H control is
  required in the adjudicating experiment to separate staging from authoring
  style.
- **Eligible attempt**: authority is valid, credentials and provider are
  available, repository state has not drifted, and the task reaches
  qualification. Infrastructure refusals are reported but excluded from task
  success denominators.
- **Intervention**: a human edit, retry decision, authority change, or plan
  regeneration between initial invocation and terminal outcome. Mechanical
  state/authority drift refusals are recorded separately and never counted as
  task failures.

## Instrument

Primary source: sealed Mentu run bundles and canonical plan artifacts produced
by the admitted-execution-graph path. The analyzer reads them read-only.

Per attempt, record:

- mode (`S`, `D`, `H-scaffold`, `H-direct`);
- objective id, task-family stratum, order position, repository HEAD, and
  authority-envelope hash;
- planner dispatch count, request/response bytes, input/output tokens, and
  elapsed milliseconds;
- candidate source hash, executable hash, qualification-report hash, admission
  receipt hash, and persistent-projection executable hash where applicable;
- execution success, verification success, changed paths, duration, model cost,
  and run-bundle manifest hash;
- intervention count and typed pre-dispatch refusal count;
- reusable artifact count: canonical plan, persistent recipe, sealed prompts,
  parity record, admission receipt, and run bundle.

Security-relevant values remain hashes; credentials and transcripts are never
copied into this repository.

## Experimental design

### Pilot (instrument validation, non-verdict-bearing)

Run at least one real bounded Mentu task through H-scaffold in this registration
regime. Before execution, save the canonical plan and materialize the persistent
recipe projection; inspect graph shape, authority binding, qualification,
planning metrics, and parity. Execute with `--from-plan` and verify that the
admission receipt binds the inspected executable. Existing static and dynamic
run bundles may be used only as descriptive context, not matched-effect
evidence.

The pilot can validate or falsify protocol invariants, but it cannot support a
comparative performance claim.

### Adjudicating matched experiment

- Freeze at least **30 objectives**, spanning at least three task families and
  three size strata, before running any arm.
- Run each objective in S, D, H-scaffold, and H-direct on resettable repository
  fixtures with the same execution backend/model, authority limits, token
  ceilings, and verification contract.
- Randomize arm order within objective and preserve all attempts, including
  refusals and failures.
- Author static recipes before randomized execution begins. Record their human
  or model authoring time separately; do not silently treat it as zero.
- Analyze paired differences by objective. Report medians and bootstrap
  confidence intervals; do not infer population effects from the pilot.
- Repeat successful unchanged-state executions three times to measure planning
  amortization and artifact reproducibility. Execution outputs may vary; graph
  identity must not.

## Predictions (frozen 2026-07-24, before the first C30 pilot run)

- **P1 — exact staged identity**: for 100% of eligible H executions, the
  inspected executable hash equals both the requalified executable hash and the
  admission receipt's executable hash. Persistent projection parity is also
  exact whenever requested.
- **P2 — no execution-time planning**: H execution invocations record exactly
  zero planner dispatches. D records one planner dispatch per invocation; S
  records zero.
- **P3 — amortization**: over three unchanged-state executions of the same
  objective, H's cumulative graph-planner input+output tokens are at most 50% of
  D's. Static authoring cost is reported separately and is not assumed to be
  lower.
- **P4 — drift fails before work**: every detected authority, objective,
  repository-state, lowering, bundle, or qualification drift in H refuses before
  runner construction and produces zero target-path changes.
- **P5 — staging effect is separable from scaffold effect**: H-direct and
  H-scaffold both satisfy P1–P4. Any difference in task success, intervention
  rate, graph size, or cost is reported as an authoring-profile effect, not as
  evidence for the freeze boundary.

## Falsification and revision criteria

- Any admitted H run whose executable hash differs from the inspected plan, or
  any H execution invocation that dispatches a planner, **refutes the core
  protocol claim**.
- Any drift case that reaches host dispatch or changes a target path
  **refutes the pre-dispatch isolation claim**.
- If H does not meet P3 at three executions, revise the amortization claim and
  report the measured break-even point; do not rescue it with unmeasured
  maintenance benefits.
- If H satisfies the protocol invariants but does not reduce intervention or
  regression rates in the matched experiment, retain it as an auditability and
  reuse mechanism only. Do not claim operational superiority.
- If scaffold and direct profiles differ materially, attribute the effect to
  authoring method. The one-runtime graph abstraction survives either outcome.

## Known limitations

- Planner token counts exclude human inspection time; inspection duration must
  be instrumented before making labor-cost claims.
- Exact graph identity does not imply deterministic model behavior inside a
  node. Outcome reproducibility and graph reproducibility are distinct measures.
- Static recipes can encode substantial unmeasured prior design effort.
- A single Mentu implementation can validate the protocol but not establish
  generality across agent platforms. The paper must state this boundary.
- Refusal is a safety outcome, not a successful task outcome; the two rates
  remain separate.

