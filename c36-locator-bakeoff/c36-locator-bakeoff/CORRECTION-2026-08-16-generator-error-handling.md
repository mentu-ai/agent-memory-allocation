# Correction (2026-08-16, pre-generation): generator provider-error handling

Found after the freeze commit (`706ccc6`) and before any question existed.

**Defect.** `run_claude` returns error records (`{"error": ...}`) rather than
raising, and its success field is `result_text`, not `result`. The frozen
generator would have (a) read a missing key, and (b) cached an empty
candidate on a provider error, permanently poisoning that attempt slot and
mislabeling a provider failure as a gate exclusion.

**Fix.** Provider errors are counted separately (`provider_errors` in the
generation log), never cached, and leave the attempt retryable on rerun;
the success path reads `result_text` and tolerates unparseable JSON as an
empty candidate (a genuine gate rejection).

**Scope.** No question existed at fix time; no gate, threshold, salt,
prompt, model, or prediction changed. The generation that produces
`questions-c36.json` runs only the corrected generator.
