---
name: biology-test-bank-ingestion
description: Build reliable structured question banks from exam PDFs, scanned booklets, answer keys, archives, and mixed text/image questions. Use when the user wants to ingest, audit, OCR/transcribe, segment, validate, resume, or extend a test bank; convert exam booklets into structured question records; preserve figures and shared passages; map official answer keys; or continue a multi-year question-bank project. Enforce year-by-year processing, provenance, deterministic validation, persistent checkpoints, and a Markdown-plus-images human-review package before a year can be completed.
---

# Biology Test Bank Ingestion

Protocol version: 0.4.0

Treat verified structured data and provenance as the primary product. Keep reusable pipeline rules separate from project-specific state.

## Core invariants

1. **One active year at a time.** Do not start the next year until the current year passes machine validation, review-package validation, human review, correction, and checkpoint completion.
2. **Source provenance is immutable.** Lock source identity and hashes before extraction. Do not overwrite or silently replace original source files.
3. **Official answers outrank inference.** Never invent a missing official answer or silently substitute a model guess.
4. **OCR/transcription is draft evidence.** Preserve raw extraction separately from cleaned text and verify against authoritative source pages/crops.
5. **Visual evidence must be preserved faithfully.** Detect image-bearing questions and crop required figures from the authoritative source. Do not redraw or model-regenerate source figures.
6. **Human review is a release gate, not optional polish.** A year is not complete until highlighted extraction errors are resolved or explicitly dispositioned.
7. **Checkpoint state is authoritative for continuation.** Do not reconstruct progress from conversation memory, README text, or assumptions when a project checkpoint exists.
8. **Do not claim persistence that did not occur.** If the configured Drive/repository write is unavailable, report the blocker and keep the year incomplete.

## Project-state routing

For an existing bank, resolve the project ID and load:

`project/<bank-id>/current_checkpoint.json`

before deciding what to do next.

Use the checkpoint to determine the active year, completed gates, artifact locations, versions, unresolved review state, and next gate. Project-specific facts belong in `project/`, not in this reusable `SKILL.md`.

For a new bank, create a project ID and initialize its checkpoint according to `references/checkpoint-protocol.md` before multi-session work begins.

## Reference routing

Load detailed references only when their stage is reached.

- `references/storage-policy.md` — read before writing persistent project data or resolving repository/Drive responsibilities.
- `references/workflow.md` — read for a new ingestion, a long-gap resume, or when gate order is unclear.
- `references/quality-gates.md` — read before declaring any gate or year complete.
- `references/data-contract.md` — read when creating or changing structured question/context/figure records.
- `references/checkpoint-protocol.md` — read when initializing, resuming, or persisting project state.
- `references/markdown-review-package.md` — read when building, validating, or correcting the canonical human-review package.
- `references/human-review-protocol.md` — read when publishing for human review or applying reviewer highlights.
- `references/pipeline-mermaid.md` — read only when the user asks for a workflow map/diagram or when a human-facing overview is useful; it is not required for normal execution.

Do not load every reference by default and do not duplicate its full schema in this entrypoint.

## Storage boundary

Follow `references/storage-policy.md`.

Default architecture:

- **GitHub/control repository:** reusable code, schemas, configs, hashes, validation rules, checkpoints, and small non-content metadata.
- **Google Drive/data plane when configured:** source archives/PDFs, rendered pages, source/question crops, figures, OCR/raw transcription, structured datasets, validated exports, and human-review packages.
- **Markdown plus relative image assets:** canonical human-review surface unless the user explicitly requests another surface.

Do not store copyrighted exam PDFs, full question-image corpora, or large generated page assets in a public reusable Skill repository by default. Do not persist private Drive IDs/URLs in a public repository unless the user explicitly requests it; prefer logical paths that can be resolved through the connected data plane.

## Pipeline

Use the gate order defined in `references/workflow.md`. The control flow is:

`source lock -> official answer mapping -> segmentation/crops -> structured transcription -> figures/contexts -> internal QA -> review-package validation -> human review/correction -> year completion`

### 0. Source lock

Inventory authoritative source files, identify the question booklet and official answer key, record hashes/page counts, assess whether native PDF text is usable, and keep originals immutable.

### 1. Official answer mapping

Parse the official answer key, normalize digits when needed, require one valid answer per expected question, and surface missing/ambiguous answers instead of guessing.

Use `scripts/parse_answer_key_pairs_v0.1.0.py` when the source format matches its contract.

### 2. Segmentation and authoritative crops

Render source pages at sufficient resolution, use deterministic layout cues where reliable, calibrate detector parameters per year, require the detected question count to match the expected count, and preserve an authoritative source crop for every question.

Use `scripts/detect_markers_v0.1.0.py` and `scripts/build_question_crops_v0.1.0.py` when applicable. Do not assume one year's geometry or thresholds apply to another year.

### 3. Structured transcription

Create records that preserve question identity, source page/crop provenance, raw extraction, cleaned text, option/type structure, official answer provenance, context/figure links, and extraction/review state according to `references/data-contract.md`.

Apply extra review to mixed Persian/English scientific notation, formulas, sequences, gene/protein names, Greek letters, subscripts, and option numbering.

### 4. Figures and shared contexts

Detect every question requiring visual evidence. Crop the required visual from the authoritative source and name assets deterministically. Store shared passages/contexts as separate records so they are not duplicated or associated with the wrong questions.

### 5. Internal QA

Compare cleaned extraction against authoritative crops/pages. Verify boundaries, numbering, option order, answer association, context association, figure association, and raw-versus-clean separation.

### 6. Build and validate the Markdown review package

Follow `references/markdown-review-package.md`. Build one ordered yearly Markdown package plus relative `images/` assets and a validation summary. Before publication, reopen the package and verify expected question count, unique/complete numbering, local image links, image-bearing-question coverage, visual crop correctness, shared contexts, and section boundaries.

Run `scripts/validate_markdown_review_v0.3.0.py` for deterministic structural validation. Do not publish a package that fails validation.

### 7. Human review and correction

Follow `references/human-review-protocol.md`. The human reviewer should identify incorrect extraction with the minimal supported convention, for example `==incorrect extracted text==`. Verify each marked issue against the authoritative source, correct the structured data or crop, regenerate the review package, rerun QA, and repeat until unresolved extraction errors are cleared or explicitly resolved.

### 8. Complete the year

Read `references/quality-gates.md` before setting `COMPLETE`. Persist the final checkpoint only after all required machine, package, and human-review gates pass. Then unlock the next year.

## Resume behavior

When the user asks to continue or resume:

1. load the current project checkpoint;
2. verify referenced persistent artifacts still exist when that affects the next action;
3. resume from the first incomplete or failed gate;
4. do not redo completed work unless validation evidence is missing, stale, or invalidated by a changed source/config/script;
5. persist a new checkpoint after each completed gate.

## New-bank behavior

For a different question bank:

1. create a new bank ID and checkpoint;
2. inventory available years;
3. select one active year;
4. resolve configured storage paths;
5. calibrate extraction/segmentation for that year;
6. run the same gate sequence and data contract;
7. build and validate one canonical Markdown review package;
8. complete the human correction loop;
9. persist the checkpoint before moving to the next year.

Never assume a prior bank's layout, subject ranges, question count, marker geometry, or answer-key format applies to another bank or year.

## Session output

At the end of a substantive working session, report only verifiable state that is useful for continuation:

- active bank and year;
- completed and failed/incomplete gates;
- detected versus expected question count when measured;
- image-bearing question count and packaged image count when measured;
- Markdown validation result;
- review-package persistence/publication state;
- unresolved human-review state;
- exact next gate;
- checkpoint version/path.

Never claim a year is complete before the required validation and human-review gates pass.
