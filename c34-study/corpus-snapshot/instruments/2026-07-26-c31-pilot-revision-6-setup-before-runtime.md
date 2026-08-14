# Instrument note — C31 pilot revision 6 seals setup before runtime injection

**Date:** 2026-07-26

**Failure observed:** 2026-07-26, during the first formal credential-free
preparation attempt under pilot revision 5

**Predecessor adapter commit:**
`37382c26ed4f83f3a3917c05e7585103123dfce2`

**Predecessor instrument bundle:**
`bf8c50c12ece51994abd7163bbbb9785d57ea9d4fbbea47a177f764de56d1e80`

**Disposition:** public-setup/runtime-order instrument failure; no pilot cell
started

## What failed

Revision 5 completed and sealed the first three credential-free task
environments:

| Task | Prepared build key | Prepared image id | Setup commit |
|---|---|---|---|
| `pdm-project_pdm-3281` | `ed258a24577e0573f63686e1097d620bcf87d64f8a61f8877d4e7e90f81fdefb` | `sha256:8ab9926d59663bdb508f5311c946b5d9afd37b89646d303dff66e9f3a0181906` | `b90bb18a209881f9147df3347c937b65a8a9d044` |
| `openai_openai-agents-python-1843` | `57256c4cbd3ecb0d7be0651f66a36ae0dfb79b9930f18048d296dbab7780bbb6` | `sha256:10bc9549d39292a9be4c7eba5094409348fef646a19aebe76331056a91a638b0` | `f2ebef4b5faf69d8285b10e890cebec86213a5a4` |
| `opshin_opshin-439` | `ea2485db3b1adda8f6f095faf360284854d511f55b80838da6c7496192814542` | `sha256:e223692c42b4fd2e115f8efcb145f413e4626089aff2a5fe96de076ac76134af` | `20c3a3c74a6c2d08c6324229cf6f4b18116a89aa` |

During the fourth task, `qodo-ai_pr-agent-1412`, the frozen public setup
completed but the adapter stopped before image commit because the
credential-facing runtime attestation no longer equaled its pre-setup value:

```text
RuntimeError: Credential-free task setup changed the credential-facing runtime
```

The failed four-task set wrote no runtime manifest. It opened no credential,
started no model request, created no pilot-run directory, and produced no
trajectory, patch, evaluation, or pilot result. The three source-bound
revision-5 prepared images listed above were removed after their provenance
was recorded.

## Diagnostic result

A separate credential-free reproduction under the committed revision-5
adapter found exactly one attestation delta. Qodo's frozen
`apt-get install -y python3 python3-pip python3-venv` command installed the
declared Python libraries and regenerated `/etc/ld.so.cache`:

- before sha256:
  `6f3a2eb8827e3085b3e411ecccd403d658134521be2c423bf9e1415d3900752e`;
- after sha256:
  `49dec7f0dc512428a50a9e0f36edbadb781a5c28d2c04e0e45b5c005879400cc`;
- kind, mode, owner:
  `file`, `0644`, `uid=0`, `gid=0` before and after; and
- cache entries:
  288 before and 293 after, adding the frozen Python, Expat, and zlib
  libraries.

Every other attested path and top-level runtime field was identical, including
the Claude package tree, native executable bytes, ELF identity, loader
topology, CA bundle, empty certificate directory, and unsafe-package list.
The reproduction used frozen base
`93e64367d20f175ee6843d6bd72f588b5f01dde6`, image head
`d9d4dc8e4dd30fb56e7ebcf32af300f8af66429d`, setup-command hash
`6436e83ad0cf5fc80dce7cdbfa19a438655f6f0afcd9110f510c3ee0f7e92296`,
setup commit `11ff1e6dcb9f899bd0de1e3797068c99c2c0ce84`, and worktree hash
`85c7431b7c1e3adff1dc56263a33c81692b46a9fc86a591fcd95f27806df439e`.
Both diagnostic containers were removed. No image, manifest, credential, model
request, or pilot artifact was retained.

## Registered repair

This note registers **C31 pilot instrument revision 6** before another formal
preparation attempt. Revision 6 changes the construction order rather than
weakening the attestation:

1. Start the exact immutable AGENTBench task image with no Claude credential or
   Claude runtime present.
2. Run the frozen public setup, remove control surfaces, rebuild the shallow
   frozen-base Git metadata, seal the setup commit, and freeze an exact
   source-bound public-setup image.
3. Build the pinned Claude/Node/native-loader overlay from that exact
   public-setup image id, restoring the pinned CA bundle from the original
   immutable task image and performing no mutable task setup afterward.
4. Bind original-base, public-setup, injected-runtime, and final prepared-image
   ids, build keys, labels, platforms, and root-filesystem layer chains into
   the runtime manifest. Each descendant layer chain must have its parent
   chain as an exact prefix.
5. Re-attest the injected runtime and sealed Git state before and after the
   final prepared-image commit. The same final image id remains shared across
   all four factorial cells for a task.
6. Write no runtime manifest unless all four public-setup, runtime-injection,
   final-image, and live-validation records pass. A failed preparation removes
   only the partial images created by that invocation.

The public task image and frozen setup commands remain the explicit
credential-free setup trusted-computing base. Runtime injection occurs only
after setup, so required task package installation cannot mutate an already
attested credential-facing runtime. This changes preparation mechanics and
the content-derived instrument bundle, not the allocation arms or estimand.

## Frozen design remains unchanged

- `estimand_unchanged: true`
- `claim_unchanged: true`
- `predictions_unchanged: true`
- `thresholds_unchanged: true`
- `arms_unchanged: true`
- `task_population_unchanged: true`
- `pilot_tasks_unchanged: true`
- `run_order_unchanged: true`
- `model_ids_unchanged: true`
- `effort_and_fallback_unchanged: true`

Pilot outputs remain non-verdict-bearing and may validate only the registered
instrument mechanics.
