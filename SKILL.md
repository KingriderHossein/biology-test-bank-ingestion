---
name: biology-test-bank-ingestion
description: Build reliable structured question banks from exam PDFs, scanned booklets, answer keys, archives, and mixed text/image questions. Use when the user wants to ingest, audit, OCR, segment, validate, resume, or extend a test bank; convert exam booklets into structured question records; preserve figures and shared passages; map official answer keys; or continue a multi-year question-bank project. Enforce strict year-by-year processing with quality gates, persistent checkpoints, Google Drive as the default data plane, and mandatory human review before a year is completed.
---

# Biology Test Bank Ingestion

Process question-bank sources as a provenance-preserving data pipeline. Treat verified structured data as the primary product. Do not start product UI work unless the user explicitly asks for it.

## Core rule: one year at a time

For a multi-year bank, process exactly one exam year at a time.

1. Select the active year.
2. Complete machine extraction and source verification for that year.
3. Publish the complete review package for that year to Google Drive.
4. Require human review of every expected question.
5. Resolve all blocking reviewer findings.
6. Persist the final checkpoint.
7. Do not process, OCR, segment, or modify the next year until the active year has passed the human-review completion gate.

If a user asks to resume an existing project, first load its persisted checkpoint from `project/<bank-id>/current_checkpoint.json` or the corresponding GitHub repository. Do not reconstruct status from memory when a checkpoint exists.

## Storage model

Read `references/storage-policy.md` before writing persistent project data.

Use:

- GitHub as the control plane for code, schemas, configs, hashes, quality gates, checkpoints, and non-content metadata.
- Google Drive as the default data plane for source archives/PDFs, rendered pages, question crops, figures, OCR/raw transcription, structured datasets, validated exports, reports, and human-review packages.
- Google Sheets as the default human-review surface for question-level approval, issue classification, reviewer notes, reviewer identity, and review date.
- Google Docs for human-readable logs, audit summaries, narrative review notes, and completion reports; do not use Google Docs as binary/object storage.

When the GitHub repository is public, do not persist private Drive folder IDs or private Drive URLs unless the user explicitly requests it. Persist logical Drive names/paths and resolve them through the connected Drive when resuming.

## Intake

Accept one or more of:

- archive (`.zip`, `.rar`, `.7z`) containing question booklets and answer keys;
- question PDF/image set;
- official answer-key PDF/image/text;
- an existing year workspace/checkpoint;
- a new test bank from another subject or exam.

Before processing, inventory files and identify the active year. Preserve original sources unchanged.

## Workflow

Read `references/workflow.md` before running a new ingestion or resuming after a long gap.

### Gate 0 - Source audit and lock

- Inventory source files.
- Identify question booklet and answer key for the active year.
- Record SHA-256 hashes.
- Record page count and whether useful native text exists.
- Never treat the presence of a PDF text layer as proof that OCR is unnecessary.
- Keep original files immutable.

### Gate 1 - Official answer mapping

- Prefer the official answer key over model inference.
- Normalize Persian/Arabic digits when parsing.
- Validate that all expected question numbers have exactly one option in the allowed range.
- If the key is image-only, OCR or transcribe it and mark the source method.
- Never silently invent a missing answer.

Use `scripts/parse_answer_key_pairs_v0.1.0.py` when applicable.

### Gate 2 - Question segmentation

- Render scanned/image-based pages at high resolution, normally 300 DPI.
- Detect stable layout cues before relying on OCR for question numbering.
- Prefer deterministic geometric cues when available.
- Calibrate detector thresholds per year.
- Require detected question count to match expected count before accepting segmentation.
- Preserve a source crop for every question.

Use `scripts/detect_markers_v0.1.0.py` with a year-specific config, then `scripts/build_question_crops_v0.1.0.py`.

### Gate 3 - Structured transcription

For each question create:

- `stem_raw` / `stem_clean`;
- four options when applicable;
- question number and source page;
- official correct option;
- `has_figure` and figure/source asset references;
- optional shared-context ID;
- extraction and review status.

OCR output is a draft, never final verified text. Mixed Persian/English scientific notation, formulas, sequence strings, gene/protein names, Greek letters, subscripts, and question numbers require special review.

### Gate 4 - Figures and shared contexts

- Preserve figures as image assets instead of forcing them into OCR text.
- When a figure is embedded in a full-page scan, crop from the authoritative rendered page.
- Keep reading passages, cloze passages, tables, diagrams, or other shared material as separate context records referenced by multiple questions.
- Do not duplicate the same passage into every question.

### Gate 5 - Internal source verification

- Compare extracted text with the source crop/page.
- Resolve obvious OCR errors before publication for external review.
- Verify option ordering, answer-key association, and figure/context association.
- Keep raw extraction and cleaned text separately.

### Gate 6 - Publish and complete human review

Read `references/human-review-protocol.md`.

For every active year:

1. Publish the year review package under the Drive year path in `05_human_review`.
2. Include source-reference access, structured question fields, official answer, figure/context flags, and one review row per expected question.
3. Use reviewer states: `PENDING`, `APPROVED`, `NEEDS_CORRECTION`, `UNCLEAR`.
4. Preserve reviewer findings; never overwrite them when applying corrections.
5. Apply required corrections to the structured dataset, then return affected questions to review when needed.
6. Require all expected questions to be `APPROVED` and zero unresolved blocking findings before passing this gate.

Human review is mandatory. Internal/model verification alone cannot make a year `COMPLETE`.

### Gate 7 - Year completion

Run `scripts/validate_year_v0.1.0.py` plus human-review gate checks.

A year can be `COMPLETE` only when machine/data validation passes, the review package is published, all expected questions are human-approved, and unresolved blocking findings equal zero. Persist the final year checkpoint before moving to the next year.

## Data contract

Read `references/data-contract.md` when creating or modifying JSON records.

Never overwrite provenance fields with cleaned values. Preserve source hashes, pages, crop coordinates, raw OCR/transcription, cleaned text, official-answer provenance, review states, reviewer findings, correction history, and pipeline/script version.

## Persistent checkpoints

After every completed gate, update the project's checkpoint file. Read `references/checkpoint-protocol.md`.

For the current MSc Biology 1206 project, the seed checkpoint is stored at `project/1206/current_checkpoint.json`.

Do not store copyrighted exam PDFs, full question crops, or large generated page images in the reusable skill repository unless the user explicitly owns the distribution rights and asks to publish them. Store large project artifacts in the configured Google Drive data plane.

## Reuse for another question bank

When the user provides a different bank:

1. Create a new bank ID.
2. Inventory its available years.
3. Select one active year only.
4. Create/resolve the corresponding Google Drive bank/year folders, including `05_human_review`.
5. Calibrate source extraction and segmentation for that year.
6. Apply the same gates and data contract.
7. Publish that year for human review before completion.
8. Persist a new checkpoint under `project/<bank-id>/`.

Do not assume the 1206 layout, subject ranges, 190-question count, or 1404 marker geometry applies to a new bank.

## Output expectations

At the end of each working session report only verifiable state:

- active bank and year;
- completed gates;
- counts detected/expected;
- human review counts (`approved`, `needs_correction`, `unclear`, `pending`);
- unresolved exceptions;
- exact next gate;
- checkpoint version/path;
- persistent data location by logical Drive path when used.

Never claim a year is complete before human review passes.