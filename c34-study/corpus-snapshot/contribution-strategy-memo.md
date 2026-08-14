# Where the meaningful contribution is

*Positioning memo, 2026-07-01 — not a corpus artifact.*

**Provenance of claims in this memo (read before citing):** A web search this
session returned only **title/URL metadata** for ~35 recent papers across four
queries (agent memory, "agents forget" production failures, agent provenance
ledgers, preregistered AI measurement) — it did **not** return full text, and I
did not fetch any of these papers. The *specific named systems and studies below*
(MemGPT/Letta, Mem0, Zep, A-MEM, LongMemEval, LoCoMo, MemoryAgentBench,
ChainProof, PROV-AGENT, ReplicatorBench, and any "PLOS ONE study") are **from my
own training knowledge, not from the in-session search results**, and carry **no
verified DOI/PMID/accession**. Treat every such name as a recall pointer to
verify, not a citation. What the searches *did* establish is only the shape of
each field (see "actually-returned titles" note at the end). Anything about the
Epistemics corpus's own numbers is measured and traceable to this repo; the
external-literature names are not.

## What the field is already doing (so we don't rebuild it)

1. **Memory systems are a crowded, benchmark-driven space.** Named systems below
   (MemGPT/Letta, Mem0, Zep, A-MEM) and benchmarks (LongMemEval, LoCoMo,
   MemoryAgentBench) are **from recall, unverified** — but the field's *shape* is
   corroborated by the in-session search, which returned titles like a
   long-horizon agentic-memory benchmark (AMA-Bench), a "second half" foundation-
   agent memory survey, and "Are We Ready For An Agent-Native Memory System?".
   These systems *build better memory* and evaluate retrieval on curated
   benchmarks; the "~55–62% utilization" figure is a recalled ballpark, **verify
   before quoting.**

2. **They share one load-bearing assumption:** that the model will *honor*
   retrieved memory once it is injected. The open, admitted-but-unmeasured
   production question is precisely "are retrieved memories actually being used,
   or ignored?" — everyone lists it; almost no one measures the base rate
   longitudinally in the wild.

3. **Hash-chained agent ledgers now exist** (ChainProof, nono, truescreen,
   PROV-AGENT, and recompute-verifiable per-decision chains in finance-agent
   work). But their framing is **compliance / tamper-evidence** — "prove the log
   wasn't altered." None uses the ledger as a *measurement instrument for
   epistemic dynamics.* So our ledger primitive is no longer novel; what we do
   *with* it can be.

4. **Preregistered, longitudinal AI measurement is an emerging, respectable
   method.** A 2026 PLOS ONE study runs a preregistered human-anchored
   longitudinal drift study with a frozen prompt bank and change-point detection
   explicitly to prevent selective reporting; COS's ReplicatorBench makes agents
   *preregister* their analysis plan. Our frozen-prediction / gated-verdict /
   kept-negatives discipline has a home in this literature — and is ahead of the
   anecdotal "agents forget" blog genre.

## The contribution we are uniquely positioned to make

**A preregistered, ledger-backed, real-world-evidence study of the
knowledge-return base rate in a production agent system — whose headline is a
negative result: capture ≫ return.**

The whole memory field optimizes retrieval and injection *quality* on benchmarks
that assume return happens. We measured the thing upstream that everyone assumes:
**does captured knowledge ever get returned at all, in the wild?** Our own
instrument's answer, on 200k+ epistemic signals over three months:

- **Return gauge ≈ 0.02%** of signals ever accessed.
- **Crystallized patterns: 0% reuse** (C9 — 1,846 patterns, zero appear in any
  run's used/injected set; a true-zero join, not an instrument bug).
- **A randomized fair test of injected-vs-withheld context (C1b) shows no reuse
  advantage** at current n — and, being a purpose-built prove-positive-reuse
  recipe, it *validates the instrument, not the hypothesis.*
- Decay of unreinforced confidence is **supported** (C3a); contradiction
  accumulation outpaces resolution.

This lands because it is (a) an **observational / real-world-evidence** study,
not a benchmark — rare and increasingly valued in agent evaluation; (b) a
**negative result delivered with rigor** — preregistered, gated, tamper-evident;
(c) positioned exactly against the field's blind spot.

## What would make it land harder (ranked next steps)

1. **Answer the external-validity objection.** Right now we measure *Mentu*, not
   "agents." Replicate the return-base-rate measurement on ≥1 independent agent
   memory system (e.g. Mem0 / Letta production traces, or an open agent-trace
   corpus). "Production agent memory does not return, across ≥2 independent
   systems" is a far stronger claim than one system's telemetry. **Highest
   leverage.**

2. **Ship the base-rate result now; it is already gate-open.** The return-gauge /
   pattern-reuse / decay findings do not depend on the C1b gate. They are
   publishable as an empirical measurement paper today. C1b (the randomized
   causal arm) is underpowered (24/21 arms vs ~128/arm needed) — keep it
   dormant and observational, don't gate the paper on it.

3. **Drop the "physics of knowledge / knowledge-as-energy" framing** from any
   external write-up. It is a liability at a serious venue; keep it as internal
   motivation only (the corpus's own `exclusions.md` discipline already does
   this). Lead with measurement, not metaphor.

4. **Name the mechanism, carefully.** Our data can distinguish "retrieval never
   fires" from "retrieval fires but the model ignores it" — a distinction the
   benchmark literature cannot make because it forces gold memory into context.
   That mechanistic split (return never *offered* vs. offered-and-not-*used*) is
   a genuinely novel readout if we can attribute it in the ledger.

## Venue framing

Empirical measurement / real-world-evidence paper positioned against the
benchmark-heavy memory literature. Natural homes: a NeurIPS/ICLR agent-memory or
agent-evaluation workshop, COLM, or an empirical-methods venue; arXiv first. The
one-line pitch: *"The memory field is optimizing how well agents use retrieved
context. We measured whether they retrieve it at all — in production, over three
months, with a preregistered protocol and a tamper-evident ledger — and they
mostly don't."*

## Actually-returned in-session search titles (the only verified retrieval)

Title/URL metadata only — no full text fetched. These corroborate field *shape*,
not the named-system claims above.

- Agent memory: "AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications";
  "Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey";
  "Are We Ready For An Agent-Native Memory System?"; "MemTool"; a "Memory in the
  Age of AI Agents" survey paper-list (GitHub).
- "Agents forget" genre: mostly vendor/blog posts (memory decay, context window
  as RAM); one academic "memory utilization" lens paper on embodied/personalized agents.
- Provenance ledgers: "ChainProof — Hash-Chained Audit Trails for AI Agents" (site);
  "Reasoning Provenance for Autonomous AI Agents" (arXiv); tamper-evident audit-trail
  posts. Framed as compliance/tamper-evidence, not epistemic measurement.
- Preregistered measurement: "Can LLM Agents Generate Real-World Evidence?
  Evaluating Observational Studies in Medical Databases" (arXiv); a human-anchored
  longitudinal bias-calibrated LLM-as-judge study (PMC); COS "Benchmarking LLM
  Agents on Scientific Tasks".

To turn this memo into a citable positioning section, fetch and verify each named
work (DOI/arXiv id) — do not cite from the recalled names alone.
