---
name: biology-test-bank-ingestion
description: Build reliable structured question banks from exam PDFs, scanned booklets, answer keys, archives, and mixed text/image questions. Use when the user wants to ingest, audit, OCR, segment, validate, resume, or extend a test bank; convert exam booklets into structured question records; preserve figures and shared passages; map official answer keys; or continue a multi-year question-bank project. Enforce strict year-by-year processing with quality gates and persistent checkpoints before advancing to the next year.
---

# Biology Test Bank Ingestion

Process question-bank sources as a provenance-preserving data pipeline. Treat verified structured data as the primary product. Do not start product UI work unless the user explicitly asks for it.

## Core rule: one year at a time

For a multi-year bank, process exactly one exam year at a time.

1. Select the active year.
2. Complete all required gates for that year.
3. Persist the checkpoint.
4. Do not process, OCR, segment, or modify the next year until the active year has passed the completion gate.

If a user asks to resume an existing project, first load its persisted checkpoint from `project/<bank-id>/current_checkpoint.json` or the corresponding GitHub repository. Do not reconstruct status from memory when a checkpoint exists.

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
- Never treat the presence of a PDF text layer as proof that OCR is unnecessary. Assess whether the extracted text contains the actual exam content.
- Keep original files immutable.

### Gate 1 - Official answer mapping

- Prefer the official answer key over model inference.
- Normalize Persian/Arabic digits when parsing.
- Validate that all expected question numbers have exactly one option in the allowed range.
- If the key is image-only, OCR or transcribe it and mark the source method.
- Never silently invent a missing answer.

Use `scripts/parse_answer_key_pairs_v0.1.0.py` when the answer key is machine-readable or has been converted to text.

### Gate 2 - Question segmentation

- Render scanned/image-based pages at high resolution, normally 300 DPI.
- Detect stable layout cues before relying on OCR for question numbering.
- Prefer deterministic geometric cues when available: printed dashes, number-label locations, separators, column boundaries, or consistent blocks.
- Calibrate detector thresholds per year. Do not assume one year's coordinates work for another year.
- Require detected question count to match the expected count before accepting segmentation.
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

### Gate 5 - Human/source verification

- Compare extracted text with the source crop/page.
- Resolve OCR errors before marking text as verified.
- Verify option ordering and figure association.
- Keep raw extraction and cleaned text separately.

### Gate 6 - Year completion

Run `scripts/validate_year_v0.1.0.py`.

A year can be `COMPLETE` only when required fields and counts pass the project's completion policy. Persist the final year checkpoint before moving to the next year.

## Data contract

Read `references/data-contract.md` when creating or modifying JSON records.

Never overwrite provenance fields with cleaned values. Preserve:

- source file hashes;
- source page;
- crop coordinates;
- raw OCR/transcription;
- cleaned text;
- official-answer provenance;
- review states;
- pipeline/script version.

## Persistent checkpoints

After every completed gate, update the project's checkpoint file. Read `references/checkpoint-protocol.md`.

For the current MSc Biology 1206 project, the seed checkpoint is stored at:

`project/1206/current_checkpoint.json`

Do not store copyrighted exam PDFs, full question crops, or large generated page images in the reusable skill repository unless the user explicitly owns the distribution rights and asks to publish them. Store code, schemas, hashes, counts, non-content metadata, and checkpoint state instead.

## Reuse for another question bank

When the user provides a different bank:

1. Create a new bank ID.
2. Inventory its available years.
3. Select one active year only.
4. Calibrate source extraction and segmentation for that year.
5. Apply the same gates and data contract.
6. Persist a new checkpoint under `project/<bank-id>/`.

Do not assume the 1206 layout, subject ranges, 190-question count, or 1404 marker geometry applies to a new bank.

## Output expectations

At the end of each working session report only verifiable state:

- active bank and year;
- completed gates;
- counts detected/expected;
- unresolved exceptions;
- exact next gate;
- checkpoint version/path.

Never claim a year is complete when only segmentation or answer mapping is complete.
