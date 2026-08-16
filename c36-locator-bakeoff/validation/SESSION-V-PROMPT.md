# CONTEXT-V — c36 validation session (attach with inputs-v/, paste block executes this)

You are an independent validator in a Claude Science session. Your task is
to **attempt to refute** the c36 adjudication using nothing but the attached
files. You have no coordinator, no web access requirement, and no authority
to consult anything not attached. Do not trust any number stated in any
attached prose document: recompute everything from the raw records with your
analysis tooling.

## Inputs (20 files)

Frozen design: the conjecture, the registration, the regeneration intent,
FREEZE.md, three dated corrections. Records: `questions-c36.json`,
`generation-log-c36.json`, `spanish-gold-c36.json`, `localization.jsonl`,
`p5-L0.jsonl`, `p5-L2.jsonl`, `metrics-c36.json`, `adjudication-c36.json`.
Code: `scoring.py`, `adjudicate_c36.py`, `generate_questions_c36.py`,
`c36lib.py`. Claimed result: `2026-08-16-c36-locator-bakeoff.md`.

## What you must do, in order

1. **Recompute every number in the results document** from the raw JSONL:
   localization @8/@3/@1 per arm; the P1/P2 deltas; the P5 accuracies under
   BOTH scoring rules (reimplement both rules from their prose specification
   in `scoring.py`'s docstrings — do not import the file — then also check
   your reimplementation against the recorded per-record `score` fields);
   the conditional accuracies (given located / not located); denominators
   everywhere.
2. **Verify the adjudication mechanically:** apply the conjecture's frozen
   verdict mapping to your own recomputed values and state whether the
   verdict `revised` follows. Check `adjudicate_c36.py` transcribes the
   frozen thresholds faithfully.
3. **Attack the instrument.** At minimum: record counts and id uniqueness
   per arm and per file; every question's `set` assignment against the
   salted-split rule (reimplement sha256(salt+id) ordering yourself);
   every gold against the generation gates (length 3–15 counted, verbatim
   impossible to check without the corpus — state that boundary honestly;
   gate-log arithmetic vs accepted/excluded counts); the P3 subset
   emptiness; whether any record field contradicts another (e.g. `located`
   vs `hits` membership, `located_top1/3` vs `hits` order).
4. **Audit the disclosures.** The results document discloses a premature
   adjudication incident, a 115-vs-120 denominator correction, and two
   error-handling corrections. Check each disclosure is consistent with the
   records you can see, and flag anything the document should have
   disclosed and did not.
5. **State the limits of what you validated.** You cannot verify the corpus
   snapshot hashes, the navigator build, or that the arms were produced by
   the pinned code — name every such boundary explicitly.

## Output contract (your final message, nothing after it)

A single JSON object:

```json
{
  "protocol": "operon-c36-v1/session-v",
  "recomputation": [
    {"claim": "<verbatim number/claim from results doc>",
     "recomputed": "<your value>", "matches": true,
     "method": "<one line>"}
  ],
  "verdict_check": {"mapping_applied": "...", "verdict_follows": true},
  "defects": [
    {"class": "INSTRUMENT_CONTRADICTION|RECORD_INCONSISTENCY|CLAIM_MISMATCH|DISCLOSURE_GAP",
     "detail": "...", "severity": "blocking|material|minor"}
  ],
  "unverifiable_boundaries": ["..."],
  "overall": "validated|validated-with-findings|noncompliant"
}
```

Every recomputation row must come from your own executed analysis, not from
reading the results document. If you cannot execute analysis tooling in this
session, output `{"protocol": "operon-c36-v1/session-v", "overall":
"noncompliant", "defects": [{"class": "INSTRUMENT_CONTRADICTION", "detail":
"no execution capability", "severity": "blocking"}]}` and stop.
