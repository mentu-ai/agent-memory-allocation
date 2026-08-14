# BUILD — C31 capability-conditioned resident utility

**Status**: registered design · **Prepared**: 2026-07-26 · **Owner**: Rashid Azarang

## Purpose

C27 measures whether boot-resident skill descriptions are invoked, but explicitly
cannot measure whether resident-but-uninvoked guidance changes task outcomes.
C31 supplies the missing counterfactual: hold guidance content constant, change
only its allocation, and compare mechanically scored work across model regimes.

The object is **marginal resident utility**, represented as a vector rather than
a scalar quality score:

```
MRU_r(g) = (
  delta_task_success,
  delta_input_tokens,
  delta_cost,
  delta_steps,
  delta_rule_violations
)
```

where `g` is one repository-guidance body and
`r = model_id × harness_commit × dataset_revision × task_population`.
No weights combine these quantities. A model or harness change creates a new
allocation regime; results from distinct regimes are never silently pooled.

## Research question

On the same coding tasks, with the same developer-authored repository guidance,
does moving that guidance from boot-resident content to pointer-paged content
preserve task success, and is the effect conditional on model generation?

This program is independent of C26/C27 accrual and uses no Mentu, CIR, LACS,
Claude transcript, or Workspace-P data.

## Pinned substrate

- Harness: `eth-sri/agentbench`, commit
  `da299c4c6b14a9abad2ceef8c751f6c45c543656`.
- Dataset: `eth-sri/agentbench`, revision
  `82c4b95db706965e82736ef5fe8404be3c0f79ba`.
- Models: `claude-opus-4-8` and `claude-opus-5`, each at explicit
  `effort=high`; fallback is disabled.
- Population: all 138 published AGENTBench instances, subject only to mechanical
  setup/evaluator validity. Four are permanently reserved for instrument
  validation; the intended adjudication population is the remaining 134.

The task manifest committed before the first run records every instance id,
repository, base commit, context path, context-body sha256, and evaluator
identity. If the pinned dataset does not yield 138 unique instances, the
instrument reports the mismatch and no pilot runs.

## Arms

The factorial cells are:

| Model | Allocation |
|---|---|
| `claude-opus-4-8` | `full_resident` |
| `claude-opus-4-8` | `pointer_paged` |
| `claude-opus-5` | `full_resident` |
| `claude-opus-5` | `pointer_paged` |

**Full-resident** leaves the developer-provided context file at the path the
harness auto-loads.

**Pointer-paged** moves the complete original body, byte-for-byte, to the
non-auto-loaded repository-relative path `.c31/full-guidance.md`. The original
auto-loaded file is replaced with exactly:

```
# Repository guidance

The complete repository guidance is at `.c31/full-guidance.md`.
Read it when it is relevant to the task.
```

The adapter verifies the moved body's sha256 against the manifest before the
agent starts and after it exits. Both arms otherwise receive the same default
system prompt, task statement, tools, permissions, repository state, evaluator,
effort setting, and execution limits.

## Frozen predictions and adjudication

Predictions are transcribed in the C31 conjecture. In operational form:

- P1: for `claude-opus-5`, `success(pointer_paged) >=
  success(full_resident) - 0.05`.
- P2: `(success(full)-success(paged))_opus4.8 -
  (success(full)-success(paged))_opus5 >= 0.10`.
- P3: the median per-task reduction in boot-resident guidance tokens in the
  pointer arm is at least 80%.

Primary outcome is official AGENTBench task resolution. Secondary outcomes:
paid and uncached input tokens, output tokens, cost, wall time, agent steps,
tool calls, files touched, rule violations where the benchmark supplies a
mechanical check, and whether/when `.c31/full-guidance.md` was read.

The future verdict comes only from a committed analyzer over the future scored
population. The analyzer emits task-level paired records and 95% paired
bootstrap intervals, stratified by repository, but frozen thresholds adjudicate
the point estimates exactly as written; intervals report uncertainty and do not
move thresholds.

## Order proof

Commits occur in this order:

1. this BUILD contract, the C31 conjecture, instrument provenance, and README row;
2. task/context manifest, adapter, analyzer, schemas, selection seeds, and retry
   policy;
3. pilot run artifacts plus a dated instrument-validation report;
4. paper v1.1 and generated publication artifacts.

No agent/model call occurs before step 2 is committed.

## Deterministic pilot selection

Pilot selection seed: `c31-agentbench-pilot-v1`.

1. Group the 138 manifest instances by repository slug.
2. Rank repository slugs by
   `sha256("c31-agentbench-pilot-v1\0" + repository_slug)`.
3. Select the first four repositories in that ordering.
4. Within each selected repository, choose the instance minimizing
   `sha256("c31-agentbench-pilot-v1\0" + instance_id)`.

This selects four tasks across four repositories without outcome inspection.
Those ids are permanently excluded from adjudication. Each runs once in all
four factorial cells: 16 pilot runs.

Future scored run-order seed: `c31-agentbench-adjudication-v1`. Ordering is by
`sha256(seed + "\0" + instance_id + "\0" + model_id + "\0" + arm)`.

## Pilot contract

The pilot validates only:

- repository setup and official test evaluation;
- exact resolved model identity and pinned harness revision;
- byte identity of relocated guidance;
- resident-guidance token measurement;
- detection of whether and when the paged body was read;
- parseable trajectory, token/cost, and evaluation records, plus a saved scored
  patch that exactly matches the pinned evaluator report.

Pilot task success is sealed but never aggregated, compared, or used to amend
the claim, predictions, thresholds, arms, or future population. An
instrument-only report may state counts of parseable records and identity
checks. It may not state per-arm success counts or effect directions.

## Retry and failure rules

- One scored agent attempt per cell. A completed attempt is never re-run.
- Infrastructure retry is allowed once only when no scored patch/evaluation was
  produced. The original failure record remains, and the retry carries
  `retry_of`. The retry must use the identical content-derived instrument
  bundle and prepared-task image, and a committed dated instrument note must
  authorize it before any later cell.
- No fallback model. A resolved model id mismatch invalidates that cell.
- Any task/context hash mismatch stops the run before the model call.
- Future adjudication is `instrument insufficient` if fewer than 100
  non-pilot tasks remain, evaluator coverage is below 95%, model identities
  drift, or content identity cannot be proven.

## Pilot exit gate

Instrument validation passes only if all 16 cells:

- start from the expected repository/base commit;
- resolve to the expected model id;
- preserve the full guidance-body hash;
- produce parseable trajectory, patch, usage, and evaluator records; and
- expose enough trace detail to classify paged-body reads.

Failure is reported in a new dated instrument note. A same-bundle transient
retry cannot repair mechanics. A mechanical repair changes the instrument
bundle and therefore requires a separately registered pilot revision rather
than a cross-regime retry; the estimand and frozen thresholds never change.

### Registered pilot revision 2

Credential-free preparation under adapter commit `33dcc4f` exposed an obsolete
Claude Code layout expectation before task setup, credential access, or any
model call. The dated
`instruments/2026-07-26-c31-pilot-revision-2-runtime-layout.md` note registers
the mechanical repair before preparation is attempted again. Revision 2 pins
the native-package integrity and executable hash and expands runtime
attestation to the actual launcher, package, loader, and shared-library
closure. The claim, predictions, thresholds, arms, tasks, hashes, and frozen
run order are unchanged. Revision 3 below supersedes this runtime mechanics
bundle before any pilot output.

### Registered pilot revision 3

The first formal credential-free preparation attempt under revision 2 stopped
at its pre-setup version probe because the x86-64 Claude executable was routed
through an emulator without AVX on the arm64 host. No task setup, credential
access, model call, or pilot output occurred. The dated
`instruments/2026-07-26-c31-pilot-revision-3-native-arm64-runtime.md` note
registers a mixed-architecture mechanics repair: AGENTBench and all repository
tools stay on the frozen amd64 image, while the identical-version Claude
executable and its pinned dependency closure run as native arm64. Both
architecture closures are attested. Credential-bearing launches also bind
OpenSSL's certificate file to the frozen base bundle and its certificate
directory to an attested-empty root-owned directory. The claim, predictions,
thresholds, arms, tasks, hashes, and frozen run order remain unchanged.
Revision 3 supersedes revision 2 for preparation and all pilot cells.

### Registered pilot revision 4

The first formal credential-free public setup under revision 3 stopped after
the first task had been sealed, when the Git history-sanitation shell returned
status 128 during the second task. The credential-free PDM prepared image was
recorded and removed; the attempt created no runtime manifest, pilot cell,
credential access, or model request. The dated
`instruments/2026-07-26-c31-pilot-revision-4-history-sanitization.md` note
registers a mechanics-only repair before another attempt: automatic Git
maintenance is disabled before ref mutation, configured remotes are removed,
every remaining ref is deleted in one transaction, one foreground prune runs,
and the adapter verifies the absence of remotes, refs, reflogs, and unreachable
future objects. The claim, predictions, thresholds, arms, tasks, hashes, and
frozen run order remain unchanged. Revision 4 supersedes revision 3 for
preparation and all pilot cells.

### Registered pilot revision 5

The first formal credential-free public setup under revision 4 sealed the PDM
task, then stopped when the published OpenAI repository object store failed a
full Git repack. The PDM image was recorded and removed; the attempt created no
runtime manifest, pilot cell, credential access, or model request. The dated
`instruments/2026-07-26-c31-pilot-revision-5-shallow-git-rebuild.md` note
registers a frozen preparation repair: reset the index while preserving setup
content, hash the complete worktree, fetch the exact detached base into a new
depth-1 Git repository, replace the old metadata, and require the same base
`HEAD` and worktree plus no ref, remote, reflog, unreachable object, or
traversable pre-base commit. This deliberately removes model-visible pre-base
Git history. The same prepared image serves every cell for a task, so the
truncation is symmetric and leaves the registered placement contrast,
predictions, thresholds, arms, tasks, hashes, and frozen run order unchanged.
It is nevertheless a revision-5 task-environment boundary and limits external
comparison with stock AGENTBench execution. Revision 5 supersedes revision 4
for preparation and all pilot cells.

### Registered pilot revision 6

The first formal credential-free setup under revision 5 sealed the PDM,
OpenAI, and OpShin tasks, then stopped on Qodo before writing a runtime
manifest. Qodo's frozen Python installation regenerated
`/etc/ld.so.cache`, so the already-injected credential-facing runtime no longer
matched its pre-setup attestation. No credential, model request, pilot cell,
patch, or evaluation resulted; the three source-bound prepared images were
recorded and removed. The dated
`instruments/2026-07-26-c31-pilot-revision-6-setup-before-runtime.md` note
registers the repair before another attempt: freeze public setup directly from
the immutable task image, then inject the pinned runtime from that exact setup
image id, bind the base→setup→runtime→prepared ids and layer prefixes, and
re-attest runtime plus Git state. Required task setup can therefore no longer
mutate an already-installed credential-facing runtime. The claim, estimand,
predictions, thresholds, arms, tasks, hashes, and frozen run order remain
unchanged. Revision 6 supersedes revision 5 for preparation and all pilot
cells.

## Scope boundary

This program does not authorize the future 536 scored runs. It registers the
study and validates its instrument only. It does not change any runtime policy,
existing conjecture, existing verdict, or paper recommendation.
