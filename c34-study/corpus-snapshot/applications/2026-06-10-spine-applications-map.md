# Applications map — 2025 research → the Mentu spine

*Engineering proposals mined from the 2025 corpus (epistemic-main +
mentu-physics + blog), mapped to the four spine components as they exist
today. This is NOT corpus material — no claims, no verdicts — it is the
backlog the research earns. Where a proposal connects to a tested conjecture,
the tie is named: the corpus's results are what turn these from "interesting"
into "motivated."*

Targets: **engine** (mentu-complete/mentu-engine), **daemon** (mentud),
**mcp** (mentu-mcp), **api** (api-server).

## Tier 1 — motivated by our own empirical results, small/medium effort

**1. Attention-decay scheduling** → daemon (temporal executor + schedule tick)
From CI-OS's attention-as-finite-resource (`engine/foundations/ci-os-the-operating-system.md`).
Schedules today fire blindly forever — C4's zombie (166 failures, zero fixes,
still scheduled) is the measured cost. Mechanism: per-schedule attention score
decays on consecutive failures → cooldown grows (exponential backoff) →
escalate to governance approval → auto-disable pending human word.
*Tie: C4 (mass/inertia). Effort: M.*

**2. Trust-scaled autonomy** → engine (sequence dispatch)
From DCOS trust envelopes (`dcos-semantic-coordination.md`): authority scales
with demonstrated competence. `trust_profiles` exists in cir.db and gates
nothing. Mechanism: per-step `permission_mode`/budget derived from the
actor×intent trust profile; recipes boot SUPERVISED, graduate to AUTONOMOUS
after N clean runs, demote on failure. *Tie: closes the loop C1b's trust
telemetry feeds. Effort: S–M.*

**3. Return-counters → precedent promotion** → engine (CIR)
From mentu-physics return-as-intelligence (`epistemic-computer.md`): recurrence
is evidence of significance; at a return threshold, deepen. `access_count` and
`reinforcement_score` already exist — they're just never consulted. Mechanism:
signals crossing a return threshold are auto-promoted (pattern/precedent kind,
durable retention, higher brief priority). Gives C1b's return loop a growth
mechanism. *Tie: C1/C3 (write-only memory, 0.045% access). Effort: S.*

**4. Displacement — substrate forgetting** → engine + daemon (extend
`cir-vacuum-*` temporals)
From displacement-driven intelligence (`science/epistemic-strategy/`):
capability comes from removal; "displacement yield = intelligence gained per
unit of removed mass." The substrate is 3.3GB, ~95% telemetry exhaust.
Mechanism: archive policy — exhaust kinds below a confidence floor with zero
access after N days move to cold storage; measure query-latency and
brief-quality before/after. *Tie: C3a (decay is real; rot should eventually be
buried, not just discounted). Effort: S–M.*

**5. Momentum carry-forward across recipe versions** → engine
From the Newtonian suite's momentum conservation: transitions should convert
momentum, not erase it. Today a recipe hash change orphans its history.
Mechanism: recipe_version transitions create `extends` relations; trust and
reflections inherit across versions with a haircut proportional to diff size.
*Tie: C4-P3 (modification dynamics). Effort: S.*

## Tier 2 — unlocks new measurement, medium effort

**6. Epistemic handles / canonical IDs** → api + engine
From `canonical-ids.md` + mentu-physics epistemic handles (permanent versioned
addresses with implements/constrains/supersedes relations). 65% of commitments
are workspace-`unknown`; C5 is unmeasurable without entity identity across
boundaries. Mechanism: canonical registry (workspace, recipe, entity) in
api-server with bidirectional local-ID mappings; engine stamps canonical refs
at capture. *Tie: prerequisite for C5. Effort: M.*

**7. Impedance-aware boundary crossing** → api (cross-device sync)
From the impedance/transmission suite — the strongest surviving physics
analogy. Mechanism: when a signal crosses workspace/device boundaries, apply
an explicit transmission policy: confidence haircut + re-interpretation pass
for the destination domain (the "matching transformer"). Makes C5's
attenuation measurable as designed behavior rather than accident.
*Tie: C5. Effort: M.*

**8. Cognitive-archetype agent profiles** → engine (convergent/adversarial
runners)
From the meta-cognitive-architectures series — as *agent design patterns*, not
clinical claims. Convergent runs N strategies with ad-hoc diversity; the MCA
essays are precisely-specified diversity: the recursive-QA verifier (multi-pass
completeness checking), the parallel-stream explorer (5–7 channels,
salience-driven reallocation), the deep-integration synthesizer (slow,
thorough, conservative), the threat-salience reviewer (hunts contradictions
and silent failures). Mechanism: named strategy profiles selectable in
convergent/adversarial configs; measure whether principled diversity beats
ad-hoc. *Tie: testable as a future conjecture. Effort: M.*

## Tier 3 — larger bets, sequenced after Tiers 1–2

**9. Activation-threshold diagnostics** → daemon (doctor/boot)
From `threshold-of-epistemic-activation.md`: four measurable conditions
(constitutional closure, recursive generativity, invariance, lawful
compression) gate whether a system may run recursive self-improvement
features. Mechanism: boot-time diagnostic; below threshold → restrict to safe
subset. A principled answer to "when is autonomy earned?" *Effort: M.*

**10. Knowledge compiler stages** → engine (dream queue) + mcp (mcp_compile)
From `epistemic-engine-compiler.md`: intent → structure → logic →
understanding. The reflections/dream machinery is stage one of this compiler,
already shipping. Next stage: compile accumulated reflections into durable
`pattern` signals with eval-gate validation — distillation as compilation.
*Tie: C1's lesson (return presupposes distillation). Effort: L, incremental.*

**11. Participation contracts with attention budgets** → mcp + daemon
governance
From `participatory-epistemic-interfaces.md`: human intent compiles to
contracts; approval is a budgeted resource. mcp_do + governance approvals
exist separately; wiring them gives trust-scaled human-in-the-loop instead of
all-or-nothing permission modes. *Effort: L.*

**12. Constitutional compiler** → engine
From mentu-physics: compile `.mentu/genesis.key` principles into *enforced*
runtime checks rather than prose. The biggest idea in the 2025 corpus that has
a real implementation path — and the largest. *Effort: L.*

## Explicitly not carried over

Epistemic temperature, quantum/relativistic suites, consciousness scoring —
same grounds as `lineage/exclusions.md`. The Oracle's geopolitical
transformations are pattern speculation, not mechanism. Constitutional game
theory's equilibrium proofs are elegant but currently have no decision they
would change in these four components; revisit when multi-tenant authority
conflicts actually exist (api-server multi-user).

## Reading order for implementation

Tier 1 items 1–5 are independent and each lands in days, not weeks. Item 1
(attention-decay) is the one the zombie pays for daily. Items 3+4 together
turn the substrate from append-only into metabolic — write, return, promote,
forget — which is the 2025 vision said in four verbs.
