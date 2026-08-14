# B2 — Field-Positioning Referee Report
*Lens: positioning of "The Return Base Rate" against the cited works ONLY.*
*Referee stance: adversarial agent-memory field expert. Judgments are from the paper's text plus reliable recall of the named systems; recency-limited items are marked NEEDS-VERIFICATION.*

Scope note: three cited items (arXiv:2603.21692, arXiv:2603.22767, Wiese 2026 / PLoS ONE 10.1371/journal.pone.0339920) postdate my January 2026 knowledge cutoff. Their existence is attested by the citation record, but I cannot independently vouch for the paper's *characterization* of them from recall. Those findings are flagged NEEDS-VERIFICATION rather than asserted.

---

## F1 — "Inject" mischaracterizes the four retrieval-based *systems*

**Claim attacked:** That MemGPT/Letta, Mem0, Zep, and A-MEM "inject the relevant context." They do not inject; each performs its *own* retrieval from its *own* store. That is the entire premise of each system: MemGPT self-pages memory in/out via function calls; Mem0 extracts/stores/semantic-retrieves; Zep retrieves over a temporal knowledge graph (Graphiti); A-MEM retrieves with dynamic Zettelkasten-style linking. "Inject" describes an oracle/full-context feed, which is exactly what these systems are built to avoid.

**Severity:** major

**Exact quoted line:**
> "MemGPT/Letta (arXiv:2310.08560), Mem0 (arXiv:2504.19413), Zep (arXiv:2501.13956), and A-MEM (arXiv:2502.12110) build agent memory systems; ... All inject the relevant context and score the downstream answer." (§7)

and, in the abstract:
> "on benchmarks that inject gold memory into the prompt and assume return has already happened." (Abstract)

**Why it matters (field-positioning):** A referee drawn from the Mem0, Zep, or Letta teams — plausible at any memory-focused venue — will read "All inject the relevant context" as evidence the authors did not understand the systems they are positioning against. The systems' contribution *is* the retrieval step the paper implies the field skips. This is the single mischaracterization most likely to trigger a harsh or reject review from exactly the cited community, even though it does not touch the correctness of the negative result.

**Proposed fix:** Split the verb by class. E.g.: "The benchmarks *provide* the answer-bearing memory in a curated corpus; the systems *retrieve* it from their own stores. In both cases the evaluation guarantees the relevant knowledge is present to be found, and scores the downstream answer." This preserves — and actually sharpens — the gap while being accurate about mechanism.

---

## F2 — "Assume return has already happened" is factually off for benchmarks that test retrieval

**Claim attacked:** That the benchmarks "assume return has already happened" / merely "inject gold memory." LongMemEval, LoCoMo, and MemoryAgentBench each include retrieval-based evaluation settings where locating the right session/turn within a long provided history *is* part of the scored task (MemoryAgentBench names "accurate retrieval" as an explicit competency; LongMemEval and LoCoMo both report retrieval-augmented as well as full-context conditions). So these benchmarks do not assume return; several *measure* a form of it. What they actually presuppose is narrower: the answer-bearing memory is *guaranteed to exist in the curated corpus*.

**Severity:** major

**Exact quoted line:**
> "LongMemEval (arXiv:2410.10813), LoCoMo (arXiv:2402.17753), and MemoryAgentBench (arXiv:2507.05257) evaluate how well agents use provided memory. All inject the relevant context and score the downstream answer." (§7)
> "on benchmarks that inject gold memory into the prompt and assume return has already happened." (Abstract)

**Why it matters:** This is the load-bearing framing of the whole gap. Stated as "they assume return happened," it is refutable in one sentence by a benchmark author ("we evaluate retrieval explicitly"). Stated correctly, it is unassailable and stronger: the honest distinction is between *conditional retrieval quality* (given a guaranteed-relevant corpus and an active query) versus the *unconditional organic-surfacing base rate across all production activity* — which is what this paper uniquely measures. Reframing on that axis defends the novelty and neutralizes the obvious rebuttal.

**Proposed fix:** Replace "assume return has already happened" with the conditional-vs-unconditional framing: "These benchmarks guarantee the answer-bearing memory is present in the provided corpus and measure retrieval-and-use quality conditioned on that guarantee. We measure the unconditional rate at which such memory is organically surfaced at all in production — the quantity their guarantee removes by construction."

---

## F3 — Internal inconsistency: §1 says "retrieved," abstract/§7 say "inject"

**Claim attacked:** The paper describes the same mechanism two incompatible ways. §1 correctly says knowledge is "retrieved into context"; the abstract and §7 say the field "injects." The correct verb already appears in the paper, which makes the "inject" usage look like loose drafting rather than a considered position.

**Severity:** minor

**Exact quoted line:**
> "the relevant prior knowledge is retrieved into context, and the question is how well the agent uses it." (§1)
versus the abstract/§7 "inject" lines quoted in F1.

**Proposed fix:** Harmonize on the precise, class-split language from F1/F2 throughout. Since §1 already has the right frame, propagate it to the abstract and §7.

---

## F4 — "Preregistered" attributed to Wiese 2026 is the load-bearing methodological hook and is unverified

**Claim attacked:** That Wiese 2026 (PLoS ONE, 10.1371/journal.pone.0339920) "reports preregistered longitudinal LLM evaluations," and that this paper therefore "adopt[s] the same freeze-predictions-before-results discipline." The citation record's own note describes that paper as "Human-anchored longitudinal comparison of generative AI with a bias-calibrated LLM-as-judge" and does **not** mention preregistration. The methodological alliance the paper claims (shared preregistration discipline) rests entirely on Wiese 2026 actually being preregistered. Separately, arXiv:2603.22767 is about agents *conducting* observational RWE studies, whereas this paper *is* an RWE study *of* an agent; bundling it under "the same discipline" is a looser fit than the sentence implies.

**Severity:** major — but NEEDS-VERIFICATION (paper postdates my cutoff; cannot confirm or deny preregistration from recall)

**Exact quoted line:**
> "recent work asks whether agents can generate real-world evidence from observational databases (arXiv:2603.22767) and reports preregistered longitudinal LLM evaluations (Wiese 2026, doi:10.1371/journal.pone.0339920); we adopt the same freeze-predictions-before-results discipline for an in-production instrument." (§7)

**Proposed fix:** Verify against the Wiese 2026 paper that it is in fact preregistered (registry link / OSF id). If yes, cite the registration to make the alliance checkable. If not, drop "preregistered" and re-anchor the freeze-predictions discipline to a source that genuinely preregisters (or present it as this paper's own contribution rather than a shared one). Also tighten the 2603.22767 clause so it is not read as claiming that paper shares the preregistration discipline.

---

## F5 — "Track agent interactions" undersells the reasoning-provenance work; provenance positioning otherwise fair

**Claim attacked:** That PROV-AGENT (2508.02866) and arXiv:2603.21692 both merely "track agent interactions." Per the citation record, 2603.21692 introduces the Agent Execution Record (AER) — "structured behavioral analytics beyond state checkpoints and execution traces," i.e. explicitly *more* than interaction tracking. The verb flattens that distinction. The core positioning move, however — "our hash-chained ledger is used here as a *measurement substrate* for a base-rate study, not as an audit end in itself" — is accurate and appropriately modest for PROV-AGENT (a W3C-PROV extension for agentic workflows aimed at debugging/reproducibility/trust).

**Severity:** nit — NEEDS-VERIFICATION for 2603.21692 (postdates cutoff; AER description taken from the citation note, not recall)

**Exact quoted line:**
> "PROV-AGENT (arXiv:2508.02866) and related work on reasoning provenance for autonomous agents (arXiv:2603.21692) track agent interactions; our hash-chained ledger is used here as a *measurement substrate* for a base-rate study, not as an audit end in itself." (§7)

**Proposed fix:** Change "track agent interactions" to something that respects the AER framing, e.g. "capture provenance and behavioral analytics of agent execution." Keep the substrate-vs-audit differentiation as is; it is the right distinction and defends against a "this is just another provenance/audit-trail system" objection.

---

## F6 — Universal quantifiers: "the whole field" / "every retrieval benchmark" overreach the 7-work basis

**Claim attacked:** The paper generalizes from seven cited works to the entire field twice. "The whole field" and "every retrieval benchmark" are stronger than the evidence base (a curated set of memory systems and benchmarks) supports, and invite a referee to name one counterexample and puncture the claim.

**Severity:** minor

**Exact quoted line:**
> "The headline is a negative result about the base rate the whole field assumes." (Abstract)
> "The base rate is the quantity every retrieval benchmark assumes ..." (§9)

**Proposed fix:** Scope the quantifier to the cited genre: "the base rate the memory-evaluation literature presupposes" / "the quantity retrieval-and-memory benchmarks presuppose by construction." Narrower, still striking, and no longer refutable by a single counterexample.

---

## F7 — Companion-paper cross-citation: unresolved identifier and standalone-sufficiency risk

**Claim attacked:** The cross-reference to *Evidence-Carrying Execution* (Azarang, 2026; "arXiv identifier to be inserted at submission") frames the two papers as "readings of one system from the engine side and the science side respectively." Two field-positioning risks: (a) the identifier is unresolved, so a referee cannot verify the companion exists or says what is claimed; (b) the complementarity framing implies this paper's measurement validity may lean on the companion's evidence/trust semantics, raising a closed-loop self-citation concern if neither paper is independently grounded. This is a self-citation matter rather than positioning against the external cited works, but it lives in the same Related Work section and a referee will treat it as such.

**Severity:** minor

**Exact quoted line:**
> "A companion paper, *Evidence-Carrying Execution* (Azarang, 2026; arXiv identifier to be inserted at submission), describes the engine side of the same instrument ... the two are readings of one system from the engine side and the science side respectively." (§7)

**Proposed fix:** Ensure the arXiv id is populated before/at submission (co-post the pair). State explicitly that this paper's claims are self-contained and do not depend on the companion for their validity, so the pair reads as complementary rather than mutually load-bearing.

---

## Overall verdict

The paper's central gap — that no cited work measures the *unconditional, organic return base rate in production*, only retrieval-and-use quality conditioned on a guaranteed-relevant corpus — is, as far as I can judge, correct and genuinely novel against the seven cited systems and benchmarks. None of MemGPT/Letta, Mem0, Zep, A-MEM (systems), nor LongMemEval, LoCoMo, MemoryAgentBench (benchmarks) reports an organic-surfacing base rate; they measure retrieval/use accuracy where a relevant memory is guaranteed to exist. The contribution survives adversarial reading. The problem is entirely in the *characterization* of how the cited works differ: the repeated verb "inject" is wrong for the four retrieval-based systems (F1) and the phrase "assume return has already happened" is factually wrong for the benchmarks that explicitly test retrieval (F2). Both are the kind of imprecision a referee from the cited teams will seize on, and both are fixable — indeed, fixing them (conditional retrieval quality vs unconditional organic base rate) makes the positioning sharper and harder to rebut. The provenance positioning is sound modulo one flattening verb (F5); the preregistration alliance is the one substantive risk that turns on a fact I cannot verify (F4 — whether Wiese 2026 is actually preregistered), and the paper's methodological framing depends on it. The universal quantifiers (F6) and companion cross-citation (F7) are cosmetic. Recommendation: not a reject on positioning grounds, but the two "inject/assume-return" majors must be corrected before this goes in front of the memory community, and the Wiese preregistration claim must be verified or removed.
