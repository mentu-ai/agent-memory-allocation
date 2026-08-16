# B2v2 — Field-Positioning Re-Referee (revised paper v1.2)
*Lens: positioning of "The Return Base Rate" against the cited works ONLY.*
*Stance: adversarial agent-memory field expert. Confirming resolution of F1–F7 and hunting regressions.*
*Recency note: three cited items (arXiv:2603.21692, arXiv:2603.22767, Wiese 2026 / DOI 10.1371/journal.pone.0339920) postdate my Jan-2026 cutoff. I judge their characterization against the citation record's own title/notes, not recall; residual exposure is marked NEEDS-VERIFICATION.*

---

## Verdict on prior findings

### F1 — "Inject" mischaracterized the four retrieval-based systems — **RESOLVED**
The blanket verb is gone and the mechanism is now split exactly by class. The verb "inject" no longer appears anywhere in the field characterization (its only surviving uses — "injected arm", "injected runs" in the Abstract/§3 — describe the paper's *own* randomized offer experiment, which is a correct use).

New §7:
> "The *systems* — MemGPT/Letta (arXiv:2310.08560), Mem0 (arXiv:2504.19413), Zep (arXiv:2501.13956), and A-MEM (arXiv:2502.12110) — *retrieve* relevant memory from their own stores; the *benchmarks* — LongMemEval (arXiv:2410.10813), LoCoMo (arXiv:2402.17753), and MemoryAgentBench (arXiv:2507.05257) — *provide* the answer-bearing memory in a curated corpus and score retrieval-and-use quality conditioned on that guarantee (several explicitly test retrieval within the provided history)."

New Abstract:
> "on evaluations that guarantee the answer-bearing memory is present to be found, whether by providing it in a curated corpus or by retrieving it from the system's own store, and then score the downstream answer."

This is the exact fix I proposed (systems retrieve from own stores; benchmarks provide a guaranteed-relevant corpus), and it sharpens rather than weakens the gap. A referee from the Mem0/Zep/Letta teams can no longer read the paper as not understanding that retrieval *is* the systems' contribution.

### F2 — "Assume return has already happened" was factually off for retrieval-testing benchmarks — **RESOLVED**
The phrase "assume return has already happened" is deleted from the Abstract. The framing is now the conditional-vs-unconditional axis I proposed, and the paper explicitly concedes the retrieval-testing settings ("several explicitly test retrieval within the provided history"), which pre-empts the one-sentence rebuttal.

New §7:
> "In every case the evaluation guarantees the relevant knowledge exists to be found. We measure the quantity that guarantee removes by construction: the *unconditional* rate at which captured knowledge is organically surfaced at all across production activity — and find it near zero."

The distinction is now unassailable: conditional retrieval-and-use quality (given a guaranteed-relevant corpus and an active query) versus the unconditional organic-surfacing base rate. No benchmark author can refute it by pointing to a retrieval setting.

### F3 — §1-vs-abstract "retrieved / inject" inconsistency — **RESOLVED**
The abstract and §7 no longer say "inject"; both now use the "provide / retrieve" split, harmonized with §1's original "retrieved into context." The self-contradiction is gone.
*Residual (nit, not a regression):* §1 still states the shared assumption at high altitude as "the relevant prior knowledge is retrieved into context" for the whole set, whereas §7 splits provide-corpus vs retrieve-from-store. This is a defensible intro-level simplification (the precise split lives in §7) and is a far milder version of the old defect — not worth blocking on, but a one-word softening in §1 ("surfaced into context") would close it completely.

### F4 — Unverified "preregistered" attributed to Wiese 2026 — **RESOLVED**
The load-bearing risk is removed. "Preregistered" no longer modifies Wiese 2026, and the freeze-predictions discipline is now claimed as the paper's own rather than inherited.

New §7:
> "longitudinal LLM evaluation with human anchoring is reported by Wiese 2026 (doi:10.1371/journal.pone.0339920). The freeze-predictions-before-results discipline we apply to an in-production instrument is this paper's own methodological commitment rather than one inherited from these works."

The new characterization ("longitudinal LLM evaluation with human anchoring") matches the citation record's title ("Human-anchored longitudinal comparison of generative AI with a bias-calibrated LLM-as-judge") — so the NEEDS-VERIFICATION exposure that made F4 a major has been designed out: nothing now turns on whether Wiese preregistered. The arXiv:2603.22767 clause is also detached from the discipline claim ("asks whether agents can generate real-world evidence from observational databases," matching its recorded title). The paper's own subtitle "Preregistered, ledger-backed real-world evidence" is a claim about *this* paper (C25), which is accurate — not a Wiese attribution.

### F5 — "Track agent interactions" flattened the AER/provenance work — **RESOLVED**
New §7:
> "PROV-AGENT (arXiv:2508.02866) and related work on reasoning provenance for autonomous agents (arXiv:2603.21692) capture provenance and behavioral analytics of agent execution; our hash-chained ledger is used here as a *measurement substrate* for a base-rate study, not as an audit end in itself."

"track agent interactions" → "capture provenance and behavioral analytics of agent execution." "Behavioral analytics" now respects the AER framing (citation record: "Structured Behavioral Analytics Beyond State Checkpoints and Execution Traces"), and "provenance" fits PROV-AGENT (W3C-PROV extension). The substrate-vs-audit differentiator is preserved. NEEDS-VERIFICATION on the 2603.21692 wording (post-cutoff), but the phrasing is now consistent with the recorded title, so exposure is low.

### F6 — Universal quantifiers over-reached the 7-work basis — **RESOLVED**
Both instances scoped to the cited genre:
> Abstract: "the base rate the memory-evaluation literature presupposes." (was "the whole field")
> §9: "The base rate is the quantity retrieval-and-memory evaluations presuppose by construction" (was "every retrieval benchmark").

No longer refutable by naming one counterexample. The two remaining "every"-class phrases are bounded to defined referents: "every such evaluation" (Abstract) means the memory-literature evaluations just characterized, and "In every case" (§7) refers to the seven enumerated works — both are checkable claims about a named set, not open-field universals.

### F7 — Companion cross-citation: standalone-sufficiency risk — **RESOLVED (in substance)**
The self-containment guarantee I proposed is now stated explicitly:
> "The two are readings of one system from the engine side and the science side; the results reported here are self-contained and do not depend on the companion for their validity."

This neutralizes the closed-loop self-citation concern. The unresolved arXiv identifier ("to be inserted at submission") remains — but that is a submission-mechanics action (co-post the pair), not a defect fixable in the manuscript text, and it is already flagged in-line.

---

## Regressions and new issues

No blocking regression. No cited system or benchmark is newly mischaracterized; the revision is uniformly more accurate than v1.1. Two low-severity watches introduced by the new wording:

**W1 (minor — the single most serious surviving item).** The Abstract compresses the retrieve/provide split into a form that makes *retrieval itself* sound like a guarantee:
> "on evaluations that guarantee the answer-bearing memory is present to be found, whether by providing it in a curated corpus or by retrieving it from the system's own store"

Retrieval from a system's own store is precisely *not* a guarantee that the memory will be found — retrieval failure is a central failure mode the retrieval community studies. The accurate claim (correctly made in the §7 body) is that the answer-bearing memory was *captured/available in the pipeline*; whether the system's retrieval surfaces it is what these systems work on. A sharp referee from the retrieval side could seize on the abstract's collapse of "available to be found" with "retrieved from the store." Fix is abstract-only and small: attach the guarantee to the corpus/pipeline, not to the act of retrieval — e.g. "…whether by providing it in a curated corpus or by making it available in the system's own store for retrieval." The §7 body needs no change.

**W2 (nit).** The §1-vs-§7 altitude difference noted under F3 — §1's "retrieved into context" as the umbrella verb vs §7's provide/retrieve split. Cosmetic; a one-word softening in §1 closes it.

Neither W1 nor W2 touches the correctness or novelty of the negative result. The central positioning claim — that no cited work reports the *unconditional, organic return base rate in production*, only retrieval-and-use quality conditioned on a guaranteed-relevant corpus — remains correct and novel against all seven systems/benchmarks, and is now stated in language that survives adversarial reading by the cited community.

## Bottom line
All seven prior findings resolved; the two v1.1 majors (F1 inject-verb, F2 assume-return) and the one substantive risk (F4 Wiese preregistration) are cleanly fixed and, in the F4 case, the fix removes the fact-dependency that made it dangerous. No regressions of consequence. The paper is now clean on field-positioning grounds; only a one-line abstract tightening (W1) would remove the last minor purchase point for a retrieval-community referee.
