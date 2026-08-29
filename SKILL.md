---
name: biology-test-bank-ingestion
description: Build reliable structured question banks from exam PDFs, scanned booklets, answer keys, archives, and mixed text/image questions. Use when the user wants to ingest, audit, OCR, segment, validate, resume, or extend a test bank; convert exam booklets into structured question records; preserve figures and shared passages; map official answer keys; or continue a multi-year question-bank project. Enforce strict year-by-year processing with quality gates, persistent checkpoints, Google Drive as the data plane, and a Markdown-plus-images human-review package before a year is completed.
---

# Biology Test Bank Ingestion

Process question-bank sources as a provenance-preserving data pipeline. Treat verified structured data as the primary product.

## Core rule: one year at a time

For a multi-year bank, process exactly one exam year at a time.

1. Select the active year.
2. Complete source audit, answer mapping, segmentation, transcription, context handling, image handling, and internal QA for that year.
3. Detect every question that requires a visual source and crop the required visual from the authoritative source.
4. Build one Markdown review package containing all questions in order plus relative `images/` assets.
5. Reopen and validate the generated Markdown package before publication.
6. Publish the package under the year folder in Google Drive.
7. Let the human reviewer highlight only incorrect extracted parts.
8. Resolve highlighted errors, regenerate/revalidate the package, and repeat if needed.
9. Persist the final checkpoint.
10. Do not start the next year until the active year has passed the human-review completion gate.

If a user asks to resume an existing project, first load `project/<bank-id>/current_checkpoint.json` from the corresponding GitHub repository. Do not reconstruct status from memory when a checkpoint exists.

## Storage model

Read `references/storage-policy.md` before writing persistent project data.

Use:

- GitHub as the control plane for code, schemas, configs, hashes, quality gates, checkpoints, and non-content metadata.
- Google Drive as the data plane for source archives/PDFs, rendered pages, question crops, figures, OCR/raw transcription, structured datasets, validated exports, and human-review packages.
- Markdown plus relative image assets as the canonical human-review surface. Do not create a Google Doc or Google Sheet for human review unless the user explicitly asks for one.

When the GitHub repository is public, do not persist private Drive folder IDs or private Drive URLs unless the user explicitly requests it. Persist logical Drive names/paths and resolve them through connected Drive when resuming.

## Workflow

Read `references/workflow.md` and `references/pipeline-mermaid.md` before running a new ingestion or resuming after a long gap.

### Gate 0 - Source audit and lock

- Inventory source files.
- Identify question booklet and official answer key for the active year.
- Record SHA-256 hashes and page count.
- Check whether native PDF text is actually useful.
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
- Preserve one authoritative source crop for every question.

Use `scripts/detect_markers_v0.1.0.py` with a year-specific config, then `scripts/build_question_crops_v0.1.0.py`.

### Gate 3 - Structured transcription

For each question create:

- question number and source page;
- `stem_raw` / `stem_clean`;
- expected options or type-specific structure;
- official correct option;
- context/figure references;
- extraction and review status.

OCR output is a draft, never verified truth. Mixed Persian/English scientific notation, formulas, sequences, gene/protein names, Greek letters, subscripts, and option numbering require special review.

### Gate 4 - Figures and shared contexts

- Detect every image-bearing question before publication.
- Crop the visual itself from the authoritative page/question crop; do not redraw it.
- Include graphs, pedigrees, diagrams, chemical structures, image-based tables, maps, and other essential visual evidence.
- Name assets deterministically, for example `images/q066_figure_01.png`.
- Keep shared passages/contexts as separate records and render them once in the review output.

Read `references/markdown-review-package.md` for the image/output contract.

### Gate 5 - Internal extraction QA

- Compare extracted text with source crops/pages.
- Resolve obvious OCR and boundary errors before publication.
- Verify option order, answer association, context association, and figure-question association.
- Keep raw OCR and cleaned text separately.

### Gate 6 - Build and validate Markdown review package

Read `references/markdown-review-package.md`.

Create under `05_human_review/`:

```text
<bank>_<year>_extracted_questions_review_vX.Y.Z.md
images/
validation_summary_vX.Y.Z.json
<bank>_<year>_review_md_package_vX.Y.Z.zip   # optional convenience bundle
```

Before upload, reopen the Markdown and verify:

- expected question count;
- complete/unique numbering;
- all local image links resolve;
- image count matches the image-bearing-question manifest;
- every image crop is visually opened and checked for clipping or wrong association;
- shared contexts and section boundaries are correct.

Run `scripts/validate_markdown_review_v0.3.0.py` for deterministic structural validation. Do not publish a package that fails validation.

### Gate 7 - Human review and correction loop

Read `references/human-review-protocol.md`.

The reviewer has one task only: compare the Markdown package with the original booklet and highlight incorrect extracted parts. Prefer the machine-readable Markdown convention:

```markdown
==incorrect extracted text==
```

No status table, issue code, reviewer name, date, or written explanation is required.

For an incorrect image crop, highlight the visible image label near that image.

After review:

1. verify each highlight against the authoritative source;
2. correct the structured dataset or image crop;
3. regenerate the Markdown package;
4. rerun final package QA;
5. republish and repeat until no unresolved highlighted errors remain.

### Gate 8 - Year completion

A year can be `COMPLETE` only when:

- machine/data validation passes;
- the canonical Markdown review package is published;
- final package QA has passed;
- the human reviewer has finished;
- all highlighted extraction errors are corrected or explicitly resolved;
- the final checkpoint is persisted.

Then and only then unlock the next year.

## Data contract

Read `references/data-contract.md` when creating or modifying JSON records. Preserve source hashes, source page, crop coordinates, raw OCR/transcription, cleaned text, official-answer provenance, context/figure provenance, review state, and pipeline/script version.

## Persistent checkpoints

After every completed gate, update the project's checkpoint file. Read `references/checkpoint-protocol.md`.

For the current MSc Biology 1206 project, the checkpoint is stored at `project/1206/current_checkpoint.json`.

Do not store copyrighted exam PDFs, full question crops, or large generated page images in the public reusable skill repository. Store project artifacts in the configured Google Drive data plane.

## Reuse for another question bank

When the user provides a different bank:

1. Create a new bank ID.
2. Inventory its available years.
3. Select one active year only.
4. Create/resolve its Drive bank/year folders.
5. Calibrate extraction and segmentation for that year.
6. Apply the same gates and data contract.
7. Detect and crop all required visuals.
8. Build, reopen, validate, and publish one Markdown review package for that year.
9. Complete the minimal human-highlight correction loop.
10. Persist a new checkpoint under `project/<bank-id>/`.

Do not assume the 1206 layout, subject ranges, question count, or 1404 marker geometry applies to another bank or year.

## Output expectations

At the end of each working session report only verifiable state:

- active bank and year;
- completed gates;
- detected/expected question counts;
- image-bearing question count and package image count;
- Markdown validation result;
- whether the review package is published;
- whether human-review highlights remain unresolved;
- exact next gate;
- checkpoint version/path.

Never claim a year is complete before the Markdown review and correction gate passes.