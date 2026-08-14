# What the burned pilot taught (2026-08-12)

**Status:** meta-lessons essay; candidate for canon metabolization at the next
weekly synthesis. Evidence anchors are commits in the C33 worktree
(`codex/agent-harness-c33`) and the agent-graph-runtime provenance notes.

On 2026-08-12 the C33 excluded pilot ran twice. The first run (`0a43aa0`) was
structurally immaculate and scientifically empty: all 70 provider calls were
rejected at the API boundary before inference, zero tokens moved, and the
pilot's own audit passed green. The second run (`59203b1`), after repairs,
produced real inference and a real result. Between them sit six freezes, two
Operon preflight stops on a sibling paper, and an unusually clean dataset
about how this program errs. These are the lessons, stated as claims about
method, each with the observation that forced it.

## 1. Gates verify parts; failures live in wholes

Every gate we had built checked components: M1 verified the runtime, launcher,
auditor and authorization gate each existed and behaved — nothing verified an
executable study existed (none did). The freeze pinned 52 artifacts — nothing
asked whether an entrypoint was among them. The pilot auditor verified counts,
seals, and replay determinism — nothing asked whether a single provider call
succeeded. The launcher's environment allowlist was security-relevant and
asserted by no test. Four gates, one blindness: verification crystallizes
around what is easy to check (structure) and away from what matters
(function).

**Corrective, adopted:** every gate ships with its own dead run — a
constructed total failure the gate must catch. If you cannot write down the
failure your check would miss, you do not yet know what your check checks.
Instances now installed: `provider_output_not_degenerate` in the pilot
auditor; the entrypoint-existence and registered-panel probes in the freeze
audit; the transport-failure regression that replays the sealed 400 envelope.

## 2. Green is the most dangerous color

The hollow pilot passed its audit. The executor's report to the author said
"zero authenticated H safety events" — true, and meaning nothing, because no
proposal ever existed to be gated (`not_exercised`, not safety evidence). Red
results investigate themselves; green results get believed.

**Corrective, adopted:** no fully-green result is believed until a
non-author, incentivized to refute it, has failed to. The builder-audits-
executor inversion found the hollow pilot within one audit pass. Role
separation, not intelligence, is what produced the truth: every participant
in this episode — both agent sessions and the orchestrator — made at least
one confidently wrong claim that another role caught.

## 3. Do not freeze claims about surfaces you do not control

Operon r1 stopped on an undeclared platform tool name; r2 stopped on an
undeclared export envelope field; C33's first pilot died on a request schema
no one had ever shown the real API. One seam, three costs: a pre-registration
that pins the *world's* behavior, rather than *our* decisions, discovers the
world one mismatch at a time, after the budget is spent.

**Corrective, adopted:** enumerate reality before freezing claims about it
(the r3 envelope model was derived from four real exports), and buy reality
contact deliberately when it cannot be enumerated — the one-call
schema-acceptance probe, explicitly budgeted and accounted, is the template.
Reality contact is cheap when purchased on purpose and ruinous when purchased
by accident.

## 4. Every zero carries its denominator

`not_exercised` versus `zero_events` is the deepest distinction the C33
registration enforces, and it generalizes: a metric reported without its
exposure conditions is an invitation to self-deception. The re-run's "zero
safety events" is reported with its true denominator — three valid proposals
produced actions; the gate was exercised exactly that often.

## 5. Concentrate ceremony on the irreversible; make everything else cheap

Six freezes in one day, minutes each, made it affordable to be wrong often,
early, and on record. Authorizations, identity exposure, and one-shot budgets
got ceremony — a human hand, a named digest, a durable artifact. The
asymmetry is the design principle, not an accident of tooling.

## 6. Supersede, never amend — failures are data about the instrument

The burned pilot's green audit artifact is retained unchanged even though the
repaired auditor would now fail it: it is the evidence for why the gate
needed repair. The reason the re-run's result is believable is that we kept a
specimen of what a hollow result looks like in this instrument. A corpus that
amended its failures away would have deleted the very thing that certifies
its successes.

## 7. The warning: instruments are not the question

This episode produced more knowledge about our instruments than about our
conjectures. That ordering is correct — instrument validity precedes claim
validity — but it has a failure mode: process perfection as a substitute for
asking the question. C33's actual question (does a deterministic admission
gate cost task success?) remains unanswered. Meta-cognition should sharpen
the aim, not become the target.

## 8. The trail is the contribution

The manuscripts this program feeds are stronger carrying their failure trails
in full — an instrument-insufficient first pilot, the repairs, the low-Haiku-
validity finding — than presenting clean results. The structural-waste paper
already demonstrated the stance (its decided null is load-bearing). Publishing
the trail is the difference between reporting results and demonstrating a
method for deciphering truth.
