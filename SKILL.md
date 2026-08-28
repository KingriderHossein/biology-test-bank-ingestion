---
name: biology-test-bank-ingestion
description: Build reliable structured question banks from exam PDFs, scanned booklets, answer keys, archives, and mixed text/image questions. Use when the user wants to ingest, audit, OCR, segment, validate, resume, or extend a test bank; convert exam booklets into structured question records; preserve figures and shared passages; map official answer keys; or continue a multi-year question-bank project. Enforce strict year-by-year processing with quality gates, persistent checkpoints, Google Drive as the data plane, and a simple Google Doc human-review step before a year is completed.
---

# Biology Test Bank Ingestion

Process question-bank sources as a provenance-preserving data pipeline. Treat verified structured data as the primary product.

## Core rule: one year at a time

For a multi-year bank, process exactly one exam year at a time.

1. Select the active year.
2. Complete extraction and internal source verification for that year.
3. Publish all extracted questions for that year into one Google Doc in Drive.
4. Let the human reviewer highlight only the incorrect text/part in that Doc.
5. Read the highlighted portions, correct the extracted dataset, and update the Doc if needed.
6. Persist the final checkpoint.
7. Do not start the next year until the current year has passed the human-review gate.

If a user asks to resume an existing project, first load `project/<bank-id>/current_checkpoint.json` from the corresponding GitHub repository. Do not reconstruct status from memory when a checkpoint exists.

## Storage model

Read `references/storage-policy.md` before writing persistent project data.

Use:

- GitHub as the control plane for code, schemas, configs, hashes, quality gates, checkpoints, and non-content metadata.
- Google Drive as the data plane for source archives/PDFs, rendered pages, question crops, figures, OCR/raw transcription, structured datasets, validated exports, and review artifacts.
- One Google Doc per completed extraction year as the human-review surface. Do not use a review spreadsheet unless the user explicitly asks for one.

When the GitHub repository is public, do not persist private Drive folder IDs or private Drive URLs unless the user explicitly requests it. Persist logical Drive names/paths and resolve them through connected Drive when resuming.

## Workflow

Read `references/workflow.md` before running a new ingestion or resuming after a long gap.

### Gate 0 - Source audit and lock

- Inventory source files.
- Identify question booklet and answer key for the active year.
- Record SHA-256 hashes and page count.
- Check whether native PDF text is actually usable.
- Keep original files immutable.

### Gate 1 - Official answer mapping

- Prefer the official answer key over model inference.
- Normalize Persian/Arabic digits when parsing.
- Validate that all expected question numbers have exactly one allowed answer.
- Never silently invent a missing answer.

Use `scripts/parse_answer_key_pairs_v0.1.0.py` when applicable.

### Gate 2 - Question segmentation

- Render image-based pages at high resolution, normally 300 DPI.
- Prefer deterministic layout cues over OCR for question numbering when reliable.
- Calibrate detector thresholds per year.
- Require detected question count to match expected count.
- Preserve a source crop for every question.

Use `scripts/detect_markers_v0.1.0.py` with a year-specific config, then `scripts/build_question_crops_v0.1.0.py`.

### Gate 3 - Structured transcription

For each question create:

- question number and source page;
- `stem_raw` / `stem_clean`;
- four options when applicable;
- official correct option;
- `has_figure` and figure/source asset references;
- optional shared-context ID;
- extraction/review status.

OCR output is a draft, never final verified text. Mixed Persian/English scientific notation, formulas, sequence strings, gene/protein names, Greek letters, subscripts, and question numbers require special review.

### Gate 4 - Figures and shared contexts

- Preserve figures as image assets instead of forcing them into OCR text.
- Crop figures from the authoritative rendered page when needed.
- Keep passages, tables, diagrams, or other shared material as separate context records referenced by multiple questions.

### Gate 5 - Internal source verification

- Compare extracted text with source crop/page.
- Resolve obvious OCR errors before handing the year to the human reviewer.
- Verify option ordering, answer association, and figure/context association.
- Keep raw extraction and cleaned text separately.

### Gate 6 - Publish one review Doc

Read `references/human-review-protocol.md`.

After extraction and internal verification:

1. Create one Google Doc for the active year inside `05_human_review`.
2. Put all extracted questions in order in that Doc, including question number, stem, options, official answer, and visible figure/context when needed for checking.
3. Ask the reviewer only to highlight incorrect text or incorrect extracted parts.
4. Do not require reviewer statuses, issue codes, forms, notes, reviewer identity, dates, or per-question approval rows.
5. Use the highlighted portions as the correction queue.

### Gate 7 - Year completion

A year can be `COMPLETE` only when:

- extraction/data validation passes;
- the yearly review Doc has been published;
- the human reviewer has finished highlighting detected errors;
- highlighted errors have been corrected or explicitly resolved;
- the final checkpoint is persisted.

Then and only then unlock the next year.

## Data contract

Read `references/data-contract.md` when creating or modifying JSON records. Preserve source hashes, source page, crop coordinates, raw OCR/transcription, cleaned text, official-answer provenance, review state, and pipeline/script version.

## Persistent checkpoints

After every completed gate, update the project's checkpoint file. Read `references/checkpoint-protocol.md`.

For the current MSc Biology 1206 project, the seed checkpoint is stored at `project/1206/current_checkpoint.json`.

Do not store copyrighted exam PDFs, full question crops, or large generated page images in the public reusable skill repository. Store large project artifacts in the configured Google Drive data plane.

## Reuse for another question bank

When the user provides a different bank:

1. Create a new bank ID.
2. Inventory its available years.
3. Select one active year only.
4. Create/resolve its Drive bank/year folders, including `05_human_review`.
5. Calibrate extraction and segmentation for that year.
6. Apply the same gates and data contract.
7. Publish one Google Doc containing that year's extracted questions for human highlighting.
8. Persist a new checkpoint under `project/<bank-id>/`.

Do not assume the 1206 layout, subject ranges, question count, or 1404 marker geometry applies to another bank or year.

## Output expectations

At the end of each working session report only verifiable state:

- active bank and year;
- completed gates;
- counts detected/expected;
- whether the yearly review Doc is published;
- whether highlighted human-review errors remain unresolved;
- exact next gate;
- checkpoint version/path.

Never claim a year is complete before the simple human-review Doc gate passes.