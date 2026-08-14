---
id: c18
name: intent-density-capture-advantage
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/epistemic-computer/building-the-epistemic-computer.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/epistemic-computer/building-the-epistemic-computer-2.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/epistemic-computer/epistemic-computer-simulation.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/epistemic-computer/epistemic-handler-light-weight-coordinator.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/epistemic-computer/epistemic-computer-software-enhacements.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/epistemic-computer/introducing-agent-marketplace-and-pipelines.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/epistemic-computer/introduction-to-the-epistemic-hardware.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/epistemic-computer/epistemic-handle-physical-product-design.md.txt
verdict: null
---

# C18 - Intent-density capture advantage

## Claim

Capture channels with higher human intent-density should produce more returnable and
useful epistemic records than broad passive capture channels at the same processing
budget and privacy burden. Intent-density means the source has already passed through
human attention: written notes, drafts, highlights, explicit imports, emails, meeting
minutes, or deliberate voice notes. Passive channels include ambient audio, room
recording, camera streams, wearable sensors, and always-on device coordination.

This is the testable residue of the epistemic-computer material. It does not admit the
hardware product vision, ambient coordinator, or "feeling understood" as established.
It tests the folder's own strongest constraint insight: prove the return loop with the
lightest high-signal input before expanding into lower-signal ambient capture.

## Origin

The audited docs pull in two directions. Some propose purpose-built hardware: a
Coordinator, Anima, Locus, Well, and ambient software ecosystem that turns lived
experience into memory. The most disciplined passage argues the opposite sequencing:
when resources are constrained, start with the written word because it has the highest
ratio of intent to noise and avoids premature sensor/privacy complexity.

C18 keeps that measurable tension. It asks whether explicit, intentional capture
actually outperforms passive capture in downstream return, not whether either product
story feels beautiful.

## Operationalization

**Datasets**:

- Capture event logs, future:
  - `capture_id`, `modality`, `source_app_or_device`, `capture_mode`;
  - `intent_level` (`explicit`, `curated`, `semi_passive`, `passive`, `ambient`);
  - consent scope, privacy level, retention policy;
  - raw byte count or duration;
  - quality/fidelity metrics (`transcription_confidence`, `speaker_confidence`,
    `ocr_confidence`, `noise_score`, `source_position_quality`);
  - extraction status, produced signal ids, handle ids, and processing cost.
- Current partial surfaces:
  - `~/.mentu/cir-pending-archive/*capture*.jsonl` records local capture operations;
  - CIR `file_snapshot` and `document` signals;
  - `~/.mentu/training/cir-run-outcomes.jsonl` selected/injected/read/use aggregates
    and source intent strings;
  - media relevance training files, which prove some media substrate exists but do not
    yet connect media capture to return outcomes.

**Predeclared predictor**:

Intent-density score at capture time:

- `0`: passive ambient capture with no explicit user act;
- `1`: semi-passive capture from an existing integration or device stream;
- `2`: deliberate source selection, but raw or weakly curated;
- `3`: explicit note, draft, import, highlight, or user-submitted artifact;
- `4`: explicit capture plus declared purpose, project, or expected future return.

**Outcomes**:

- extraction success and accepted-record rate;
- downstream selection and injection into run context;
- actual read/use footer or citation;
- verified/proven contribution to later work;
- later correction, deletion, privacy objection, or "irrelevant capture" label;
- cost per accepted and later-used record;
- user review response where available: returned insight saved, acted on, or ignored.

**Controls**:

- modality and source app/device;
- capture size/duration;
- processing method/model;
- workspace and recipe family;
- C7 handle richness;
- C13 semantic redundancy;
- C15 compiler invocation readiness;
- C16 conditional activation selectivity;
- privacy sensitivity/risk class;
- week/cohort.

## Predictions (stated 2026-06-19, before C18 verdict analysis)

- **P1**: Explicit text-like captures will have higher accepted-record and later-use
  rates than passive ambient captures after size, workspace, and processing controls.
- **P2**: Passive audio/video capture will have higher extraction volume but lower
  utility per processed byte and per dollar unless it carries high-quality consent,
  speaker, and context metadata.
- **P3**: Deliberate voice notes should sit between explicit text and ambient audio:
  lower friction than text, but lower precision unless transcription confidence is
  high.
- **P4**: Any benefit from passive capture should be largest for missed-context
  recovery tasks and weakest for precise commitment/decision extraction.
- **P5**: The "hardware captures more life" hypothesis is supported only if ambient
  modalities improve downstream utility without increasing privacy objections,
  correction burden, or cost per later-used record.

## Falsification criteria

- Intent-density has no positive association with accepted records, return/use,
  verified contribution, or lower correction/privacy burden after controls ->
  **refuted**.
- Ambient capture outperforms explicit text on utility per cost and privacy burden ->
  **revised** toward a modality-rich capture claim.
- The apparent advantage is explained by C7/C13/C15/C16 controls -> **revised** as
  handle/redundancy/compiler/activation quality rather than capture intent-density.
- Any verdict that lacks passive-capture denominators, skipped captures, or privacy
  outcomes is invalid.

## Gate

C18 may produce a verdict only when all are true:

- scoring rules are frozen before outcome modeling;
- at least 5,000 capture events exist with modality and intent-level labels;
- at least 1,000 explicit/curated text-like captures and 1,000 passive/semi-passive
  audio/video/sensor captures exist;
- each capture records consent/privacy scope and quality/fidelity metadata;
- produced signal/handle ids are linked to later selection, injection, read/use,
  correction, deletion, or privacy outcomes;
- at least 8 weeks of follow-up exist;
- C7/C13/C15/C16 controls are computable for produced artifacts.

Current data has capture archives, file snapshots, and run aggregates. It does not yet
log per-capture modality, intent-density, quality, consent, or capture-to-return
outcome links. C18 is therefore readiness-gated.

## Known limitations

- Explicit text may look better because it is used by more technical users or higher
  stakes workflows. Control for workspace, user cohort, artifact type, and task class.
- Passive capture may be valuable for recall and accountability even when it is less
  efficient for ordinary return. Outcome classes must be separated.
- Privacy burden is part of the claim, not an externality. A high-utility capture mode
  that creates unacceptable privacy objections does not support C18.
- The product-design language is useful only as lineage. The scientific object is the
  capture channel and its downstream utility.
