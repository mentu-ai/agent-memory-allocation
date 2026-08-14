# Related work: from retrieval quality to the return base rate

The agent-memory literature has largely settled on a shared objective — make the
memory an agent retrieves better, and measure how well the agent answers once
that memory is in context. This study asks a question one step upstream of that
objective: in a production system, does captured knowledge get returned and
reused *at all*? The distinction matters because nearly every result below is
obtained under conditions that presuppose return has already happened, which
leaves the return base rate itself unmeasured. This section separates what the
field optimizes from the gap this work measures, and cites only sources whose
identifiers resolve to a real primary record.

## Memory systems optimize what happens after retrieval

The dominant systems treat memory as an engineering surface to be architected,
and evaluate it by the quality of what is retrieved and injected. MemGPT framed
long-term memory as an operating-system problem, paging information in and out of
a bounded context window under the model's own control
([MemGPT](https://arxiv.org/abs/2310.08560)); it has since been productionized as
the Letta framework, but the citable primary record is the 2023 paper. Mem0
targets production deployment directly, adding a scalable long-term memory layer
whose evaluation centers on retrieval accuracy and latency
([Mem0](https://arxiv.org/abs/2504.19413)). Zep organizes memory as a temporal
knowledge graph so that facts carry validity intervals and can be queried as they
evolve ([Zep](https://arxiv.org/abs/2501.13956)). A-MEM pushes further into
agent-controlled memory, letting the agent structure, link, and revise its own
notes rather than writing to a fixed schema
([A-MEM](https://arxiv.org/abs/2502.12110)). These systems differ in data
structure and in how much control the model has over its own store, but they
share one load-bearing assumption: that once relevant memory is surfaced and
placed into context, the model will honor it. Whether that assumption holds in
the wild — whether surfaced memory is used, or ignored — is acknowledged but not
measured longitudinally by any of them.

## Benchmarks score use, having already assumed return

The benchmarks that drive this field encode the same assumption at the level of
experimental design: they supply the memory and then score the answer. LongMemEval
constructs long interactive histories and tests whether an assistant can recall
and reason over earlier turns, reporting accuracy on curated question types
([LongMemEval](https://arxiv.org/abs/2410.10813)). LoCoMo evaluates very
long-term conversational memory over machine-generated multi-session dialogues,
again scoring question-answering and reasoning against a known gold context
([LoCoMo](https://arxiv.org/abs/2402.17753)). The benchmark commonly referenced as
MemoryAgentBench is published under the title *Evaluating Memory in LLM Agents via
Incremental Multi-Turn Interactions*, and it systematizes this setup across
competencies such as accurate retrieval and long-range understanding
([MemoryAgentBench](https://arxiv.org/abs/2507.05257)). The methodological
common denominator is decisive for the present work: each benchmark either forces
the relevant memory into context or defines success relative to a gold memory that
is known to be available. That design makes them well suited to measuring
retrieval and use quality, and structurally unable to observe the prior event —
whether, in an uninstrumented production run, the memory is returned to the model
in the first place. A benchmark that guarantees return cannot estimate the rate at
which return fails.

## Provenance ledgers frame logging as compliance, not measurement

A separate line of work builds tamper-evident records of what an agent did, which
is adjacent to this study's instrument but aimed at a different target. PROV-AGENT
provides a unified provenance model for tracking agent interactions across agentic
workflows, oriented toward reproducibility and trust in multi-agent pipelines
([PROV-AGENT](https://arxiv.org/abs/2508.02866)). More recent work introduces the
Agent Execution Record, a schema-level "reasoning provenance" primitive that
captures intent, observation, and inference as first-class queryable fields so
that an agent's reasoning can be analyzed across populations of runs
([Reasoning Provenance for Autonomous AI Agents](https://arxiv.org/abs/2603.21692)).
These systems make an agent's history auditable and queryable, and the second is
close in spirit to using a ledger analytically. Their framing, however, is
compliance, debugging, and tamper-evidence — proving the log was not altered and
explaining individual failures — rather than treating the ledger as a measurement
instrument for epistemic dynamics such as the return base rate. The commercial
"ChainProof" offering occupies the same tamper-evident-audit niche but is a
product website rather than a peer-reviewed or preprint contribution *(unverified —
no scholarly identifier found; https://chainproof.ai/ is a vendor page, not a
primary record)*, and is noted here only to disambiguate it from the citable
provenance work above.

## Preregistered and real-world-evidence AI measurement

The methodological home for this study is the emerging practice of preregistered,
observational, real-world-evidence evaluation of AI systems, which is distinct from
the benchmark tradition and increasingly treated as rigorous. A recent benchmark
asks whether LLM agents can generate real-world evidence by conducting
observational studies over medical databases, importing epidemiological standards
of evidence into agent evaluation
([Can LLM Agents Generate Real-World Evidence?](https://arxiv.org/abs/2603.22767)).
On the longitudinal side, a preregistered PLOS ONE study tracks three model
families over ten weekly waves with a frozen prompt bank and change-point
detection, using blinded human raters anchored by a bias-calibrated
LLM-as-judge, explicitly to make service drift measurable without selective
reporting ([Wiese 2026](https://doi.org/10.1371/journal.pone.0339920)); this
single paper accounts for both the "PLOS ONE" and the "PMC LLM-as-judge" studies
that earlier recall had listed as separate works. ReplicatorBench extends the
preregistration ethos to agents themselves, benchmarking whether LLM agents can
assess the replicability — not merely the reproducibility — of social and
behavioral science claims, including human-verified non-replicable claims
([ReplicatorBench](https://arxiv.org/abs/2602.11354)). Together these establish
that a frozen-prediction, gated-verdict, kept-negatives discipline has an
established literature to sit within, and that an observational negative result,
delivered with preregistered rigor, is a recognized contribution rather than an
anecdote.

## The upstream gap this study measures

Read across these four bodies of work, the field's center of mass is the quality
of *use given return*: better memory architectures
([MemGPT](https://arxiv.org/abs/2310.08560);
[Mem0](https://arxiv.org/abs/2504.19413);
[Zep](https://arxiv.org/abs/2501.13956);
[A-MEM](https://arxiv.org/abs/2502.12110)) evaluated on benchmarks that guarantee
the relevant memory is present
([LongMemEval](https://arxiv.org/abs/2410.10813);
[LoCoMo](https://arxiv.org/abs/2402.17753);
[MemoryAgentBench](https://arxiv.org/abs/2507.05257)). Provenance systems can
record what happened but are framed for audit rather than for measuring epistemic
dynamics ([PROV-AGENT](https://arxiv.org/abs/2508.02866);
[Reasoning Provenance for Autonomous AI Agents](https://arxiv.org/abs/2603.21692)).
The upstream quantity — the base rate at which captured knowledge is returned to
the model at all, in production, over time — falls in the blind spot common to all
of them, because their designs assume it away. This study measures that base rate
directly with a preregistered, ledger-backed, real-world-evidence protocol, adopting
the observational and preregistration standards of the AI-measurement literature
([Can LLM Agents Generate Real-World Evidence?](https://arxiv.org/abs/2603.22767);
[Wiese 2026](https://doi.org/10.1371/journal.pone.0339920);
[ReplicatorBench](https://arxiv.org/abs/2602.11354)) and turning a provenance ledger
from a compliance record into a measurement instrument. Its headline is a negative
result — capture greatly exceeds return — which is legible precisely because the
surrounding literature has, without measuring it, assumed the opposite.
