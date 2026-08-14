# Diagnosis — why the return loop reads empty

**Date**: 2026-06-10 (same day as the C1 result)
**Follows**: `results/2026-06-10-c1-return-as-intelligence.md`, recommendation 1
("verify the brief→prompt→footer→used_signal_ids chain end-to-end").
**Method**: read-only inspection of `mentu-engine` source
(`Sources/MentuEngine/CIRContextBrief.swift`, `CIRRunOutcomeRecorder.swift`) and
`~/.mentu/cir.db` signal contents.

## Summary

The C1 result left two live explanations: agents ignore the briefs, or attribution
fails silently. **Both were wrong.** The attribution chain is mechanically sound and
agents comply with it — they read the briefs and answer `CIR_USED: none`, honestly.
The failure is one level deeper: **the substrate content**. What Mentu's CIR returns
into runs is operational exhaust, not knowledge, and the agents correctly report
that it changed nothing.

## Findings

### F1 — The attribution chain is sound (initial hypothesis refuted)

My first hypothesis was an ID-format mismatch (engine tracks `cir_<recipe>_<HEX>`,
interactive agents cite `digest_*`). The code refutes it:

- `CIRContextBrief.usageContract` lists the exact injectable IDs in the prompt
  ("Available evidence IDs: …") and requires `CIR_USED: <ids|none>` as the
  penultimate output line.
- `CIRContextBrief.parseUsage` scans output for the footer, classifies cited IDs
  against the injected set; non-matching citations are recorded as
  `invalid_used_ids`.
- Across all 54 injected runs, `invalid_used_count = 0`. If agents had cited
  wrong-format IDs, that counter would be nonzero. With footers present in ~91%
  of reads and zero valid or invalid citations, agents wrote `CIR_USED: none`.
- (`digest_*` footers belong to a different surface — the interactive Claude Code
  hook — which the run-outcomes instrument does not measure. Cross-surface caveat
  recorded for the instrument map.)

### F2 — The substrate content is operational exhaust

What the selector has to choose from (`cir.db` `signals`, 2026-06-10):

- **Kind distribution is machine telemetry**: `temporal_result` 153,836;
  `temporal_executor_poll` 13,251; `claim` 8,638; `commitment` 7,802;
  `sentinel_triggered` 6,720; `step_result` 6,269 … Distilled, reusable knowledge
  is a rounding error in this pool.
- **Confidence is not assessed, it is banded by kind**: 99,161 signals at exactly
  0.8; 54,560 at 0.3; 26,116 at 0.4; all `embedding` at 0.5; all `recipe_version`
  at 1.0; the injected `step_result` signals uniformly 0.75. The `asserted_confidence`
  field carries kind defaults, not epistemic judgment — so trust-weighted selection
  is selection by kind, in disguise.
- **What actually got injected** (sampled from the 54 runs): truncated output
  tails of prior steps, clipped mid-word at 260 chars by the brief formatter —
  e.g. `cir_sc-np-verify_AF386666` begins "d` (22 KB, 11 H2 sections)…". One
  injected signal, `cir_openai-ping_88BFD33E`, has the body
  **"CIR_USED: none OPENAI_SMOKE_COMPLETE"** — a previous agent's own
  *nothing-was-useful declaration*, stored as evidence and re-served to the next
  agent.

An agent told to report what "materially influenced your plan" and handed
mid-word fragments of prior stdout is giving the correct answer: `none`.

### F3 — The one distilled channel is invisible to measurement

The brief format includes "Recent run reflections (prior runs' distilled lessons)"
— exactly the right content type — but marks them **"not citeable in CIR_USED"**
(`CIRContextBrief.swift:603`). If return-as-intelligence is happening through
reflections, the outcome instrument cannot see it. The only channel that *can* be
measured is the one filled with exhaust.

## Interpretation for the corpus

This sharpens the C1 verdict's locus. Refuted: "Mentu's current injection
implements return-as-intelligence." Untested: the theory itself. And the diagnosis
adds a refinement that descends directly from the 2025 substrate thesis:
**return presupposes that what is stored is knowledge.** A return loop over
exhaust is correctly worthless — the failure isn't in returning, it's in what was
kept. Distillation is a precondition of return.

## Engineering proposal (for Mentu; not applied — engine is production)

1. **Distill at capture**: gate `step_result`-class signals out of the injectable
   pool; admit only signals that pass a distillation step (self-contained lesson,
   complete sentences, body survives truncation) — the dream/reflection machinery
   already in the engine is the natural home.
2. **Make reflections citeable**: give reflections stable IDs valid in `CIR_USED`
   (or a parallel `REFLECTIONS_USED` footer) so the distilled channel becomes
   measurable.
3. **Assess confidence at write time** instead of kind-banding, or rename the
   field; selection currently launders kind defaults as trust.
4. **Randomize injection within-recipe** (coin-flip per eligible run) to give C1b
   common support.

## What this unblocks

`corpus/conjectures/c1b-return-as-intelligence-randomized.md` — the designed fair
test. Prerequisites: items 1, 2, 4 above. Until they land, no observational
reading of `cir-run-outcomes.jsonl` can either prove or disprove
return-as-intelligence; it can only re-measure the exhaust problem.
