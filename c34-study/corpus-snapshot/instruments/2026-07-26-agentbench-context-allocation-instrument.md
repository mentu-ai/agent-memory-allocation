# Instrument note — AGENTBench context-allocation experiment

**Date**: 2026-07-26 · **Serves**: C31 · **Mode**: public, isolated,
counterfactual agent evaluation

## Measurement surface

C31 uses the public AGENTBench coding-task harness and dataset:

- harness commit:
  `da299c4c6b14a9abad2ceef8c751f6c45c543656`;
- dataset revision:
  `82c4b95db706965e82736ef5fe8404be3c0f79ba`.

AGENTBench supplies real GitHub issue tasks, repository setup, developer-written
repository context, agent trajectories/patches, and official per-instance test
evaluation. The instrument consumes only this public substrate.

## Experimental intervention

The content of repository guidance is held constant while its allocation
changes:

- `full_resident`: original developer guidance remains at its auto-loaded path;
- `pointer_paged`: that same byte sequence moves to
  `.c31/full-guidance.md`, while the auto-loaded path contains one frozen
  pointer to it.

Body identity is established by sha256 before and after each run. The pointer
text and relocation path are frozen in
`docs/BUILD-c31-capability-conditioned-resident-utility-v1.md`.

## Recorded fields

The committed manifest and adapter record:

- instance id, repository slug, base commit, task statement hash;
- original context path, body byte count, token count, and sha256;
- harness commit, dataset revision, adapter commit, immutable task-image
  identity, and derived generation-image id;
- requested and resolved model id, effort, arm, run-order key;
- trajectory/patch/evaluator artifact paths and sha256 values;
- input/output/cache token fields, cost, wall time, steps, tool calls, files
  touched;
- paged-body Read occurrence and first-read step;
- official resolved/pass-fail outcome;
- infrastructure status and declared retry lineage.

No composite quality or integration score is computed.

## Observer-effect and isolation boundary

Generation runs inside a derived image based on the manifest's immutable
AGENTBench task image; official evaluation runs separately in a fresh copy of
the untouched base image. Dataset setup commands execute before the
intervention, and no host worktree, home directory, keychain, socket, or
ambient environment is mounted into either container. A dedicated Claude
authorization credential enters through a finite anonymous fd-0 pipe for one
auth preflight and again for one direct generation launch; it is never copied
into the container filesystem or placed in the task process environment or
command line, and is absent from saved artifacts. Before authentication, the
adapter attests every persistent directory or regular file writable—or
chmod-able by ownership—by model uid `31310`, rejecting unmodeled POSIX ACLs.
It excludes non-persistent `/proc`, `/sys`, and `/dev` while checking
`/dev/shm` separately. After auth preflight, after generation, and at final
containment, all attested surfaces (including `/testbed`, `/tmp`, and runner
home) are streamed through a host-side exact-token/token-shape scan via the
Docker daemon; the raw secret is not resent to an in-container scanner or
placed in a scanner command. Every saved scan record must reproduce the full
frozen surface path list and count; capture, continuation, and pilot validation
reject a truncated or substituted proof.

The generation derivation verifies the exact npm integrity of both the Claude
Code wrapper and its linux-arm64 native package and pins the native executable
hash. The AGENTBench task image and repository tools remain linux/amd64: a
digest-pinned amd64 builder supplies Node, while a digest-pinned arm64 builder
supplies the same-version Claude executable and its exact
loader/shared-library closure so the model process runs natively on the arm64
host. The derivation materializes one exact launcher symlink and retains the
identical frozen CA bundle supplied by each immutable pilot base. Every
credential-bearing launch pins `SSL_CERT_FILE` to that bundle and
`SSL_CERT_DIR` to a root-owned directory whose emptiness is attested before
credential access and after execution. The runtime
attestation covers both builder and architecture identities, both native
executable locations and their byte identity, both package manifests, the
launcher target, both architecture closures, and the TLS trust-source
invariant. It does not run a mutable
package manager after the build. For each task, dataset setup runs exactly once
in a credential-free container. The adapter records the published image's
initial Git HEAD, proves
the frozen base commit is present, checks it out detached, and verifies exact
HEAD before setup. The setup container is stopped and frozen before the pinned
credential-facing runtime is injected. Exact base, public-setup, runtime, and
prepared-image ids and layer prefixes are bound into the manifest; the runtime
and sealed Git state are then attested before the exact prepared-task image is
reused for all four cells. The pinned public task images and exact hashed
public setup commands are the explicit setup trusted-computing base and never
receive the credential. Model calls start in fresh containers with
`no-new-privileges`, a reduced root-harness capability set, and a dedicated
unprivileged user without `sudo`. The adapter opens the dedicated credential
only after all four prepared-task images and frozen-order checks pass.

Resident guidance tokens are remeasured from the bytes actually materialized
in the container. Reserved relocation paths are checked with `lstat`; symlink
or collision cases are instrument failures. The adapter quiesces each model
container before hashing, restores its sealed Git configuration, and extracts
the candidate patch against the frozen preparation commit. The exact cleaner
imported from the pinned AGENTBench harness derives the UTF-8 patch that the
official evaluator scores; those bytes are saved as `patch.diff` and must equal
the evaluator report's `model_patch`. The adapter captures and retains the raw
official instance- and repository-test result maps in a separately hashed
evidence artifact. It binds those maps to the report booleans, returned
outcome, frozen pre-patch repository baseline, and saved scored-patch bytes; an
empty repository result map is valid only when the frozen task declares no
repository-test command.

The isolated environments do not read or write:

- `~/.mentu`, CIR, LACS, or any Mentu service;
- `~/.claude/projects` transcript corpora used by C26–C28;
- Workspace-P or any third-party client material;
- the live `epistemics` worktree as a task repository.

The `mentu` CLI and MCP CIR paths are forbidden. Model calls use no session
persistence and no fallback. Pilot and future scored artifacts live only under
the C31 analysis directory.

## Regime identity

One regime is the exact tuple:

```
model_id × effort × harness_commit × dataset_revision ×
instrument_bundle_sha256 × adapter_commit × task_manifest_sha256 ×
pointer_text_sha256 ×
runtime_manifest_sha256 × prepared_task_image_id
```

A change in any tuple member creates a new regime. Results from different
regimes are not pooled. Provider-side refusal or unavailability is recorded as
infrastructure state, never silently served by another model.

The content-derived instrument bundle covers the adapter, analyzer, pilot
validator, schemas, tests, manifests, guidance bodies, and registered C31
contracts. A continuation revalidates the schema, hashes, identity, evaluator
evidence, and retry lineage of every earlier terminal cell before credential
access. It reuses the capture-time evaluator procedure to rederive raw
instance/repository maps, report booleans, the frozen pre-patch baseline,
coverage counts, and evaluation-detail hashes from the saved bytes and pinned
dataset row. Only an unchanged-bundle transient failure with no patch or
evaluation artifact may receive one immediate retry, and only after a
committed dated instrument note. A mechanics change is a new pilot revision,
not a retry.

## Pilot instrument revision

Revision 2 was registered by
`instruments/2026-07-26-c31-pilot-revision-2-runtime-layout.md` after
credential-free preparation exposed an obsolete Claude Code entry-point path.
Its formal pre-setup probe then exposed an x86-64 emulator/AVX failure.
Revision 3 is registered by
`instruments/2026-07-26-c31-pilot-revision-3-native-arm64-runtime.md` and moves
only the same-version Claude executable and sealed dependency closure to native
arm64 while keeping the frozen task substrate amd64. Both repairs predate any
credential access or model call and change runtime mechanics only. The
estimand, predictions, thresholds, arms, pilot tasks, manifests, and run order
remain frozen.

Revision 4 is registered by
`instruments/2026-07-26-c31-pilot-revision-4-history-sanitization.md` after
revision 3's first formal public setup stopped on a status-128 Git
history-sanitation failure. It serializes ref deletion and foreground pruning
and verifies that no remote, ref, reflog, or unreachable future object remains.
The first credential-free PDM task had already been sealed; its revision-3
source-bound image was recorded and removed. The attempt produced no runtime
manifest, pilot cell, credential access, or model request. Revision 4 changes
mechanics only; the estimand, predictions, thresholds, arms, pilot tasks,
manifests, and run order remain frozen.

Revision 5 is registered by
`instruments/2026-07-26-c31-pilot-revision-5-shallow-git-rebuild.md` after the
published OpenAI repository object store failed revision 4's full repack. It
reconstructs Git metadata from a local depth-1 fetch of the exact detached base
commit, proves the non-Git worktree unchanged, and requires that no ref,
remote, reflog, unreachable object, or traversable pre-base commit remains.
The stopped attempt had sealed one credential-free PDM image; that
revision-4 source-bound image was recorded and removed. It produced no runtime
manifest, pilot cell, credential access, or model request. Revision 5 changes
the task environment only as disclosed below; the estimand, predictions,
thresholds, arms, pilot tasks, manifests, and run order remain frozen. The
depth-1 rebuild intentionally
removes model-visible pre-base Git history. The same prepared image is used by
all four cells for each task, so this is symmetric and does not confound the
registered placement contrast; it is a revision-5 task-environment boundary
that limits external comparison with stock AGENTBench execution.

Revision 6 is registered by
`instruments/2026-07-26-c31-pilot-revision-6-setup-before-runtime.md` after
revision 5's formal credential-free preparation sealed three tasks and stopped
on Qodo. Qodo's frozen Python package installation regenerated
`/etc/ld.so.cache`, correctly failing the equality check for a runtime that had
already been injected. The stopped attempt wrote no runtime manifest, opened
no credential, started no model, and created no pilot artifact; its three
source-bound prepared images were recorded and removed. Revision 6 freezes the
public setup image first, then injects and attests the pinned runtime, binding
the exact base→setup→runtime→prepared image and root-filesystem layer lineage.
The estimand, predictions, thresholds, arms, pilot tasks, manifests, and run
order remain frozen.

## Known limits

1. AGENTBench is Python/repository-task evidence, not a universal task
   distribution.
2. Developer context may be useful for compliance even when it does not change
   official test resolution; mechanical rule-violation measures are secondary
   and available only where the benchmark exposes them.
3. A paged-body Read proves exposure, not causal use. The randomized allocation
   contrast carries the outcome estimand; Read classification is mechanism
   context only.
4. Model generation and capability are bundled in the model-id contrast. C31
   does not isolate which internal capability causes any interaction.
5. Pilot outcomes are hypothesis-contaminated by construction and permanently
   barred from adjudication.
6. File-based ancestor, user, project, and Linux managed controls are removed
   or isolated. Server-managed settings attached to the authorization account
   remain an explicit account trust boundary and must not vary across cells.
7. Revision 5 preserves the frozen base commit and complete post-setup
   worktree, but intentionally truncates model-visible pre-base Git history.
   This is identical across all four cells for a task and therefore preserves
   the factorial placement contrast, while limiting external validity relative
   to stock AGENTBench repository execution.
