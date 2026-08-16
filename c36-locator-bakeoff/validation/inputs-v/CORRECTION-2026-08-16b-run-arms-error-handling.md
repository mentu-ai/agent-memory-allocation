# Correction (2026-08-16, pre-P5-record): run_arms Phase B error handling

Same defect class as CORRECTION-2026-08-16-generator-error-handling, in
`run_arms.py` `phase_b`, which the first correction did not touch: it read
`rec["result"]` (the field is `result_text`) and did not handle
`run_claude`'s error records. Phase B crashed on its first call, before any
P5 record was appended — `runs-c36/p5-*.jsonl` did not exist at fix time.

Fix mirrors the generator's: `result_text` on success, provider errors
printed and skipped without a record (the per-id resume gate makes the
question retryable on rerun). Phase A records, the question set, and all
localization results are untouched; no threshold, policy, prompt, or model
changed.
