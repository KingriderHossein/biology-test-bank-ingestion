# Workflow Reference

## Contents

- 1. Workspace model
- 2. Year-by-year state machine
- 3. Source audit
- 4. Text-vs-image decision
- 5. Segmentation strategy order
- 6. OCR strategy
- 7. Figures
- 8. Shared contexts
- 9. Markdown review package
- 10. Final package QA
- 11. Human review publication
- 12. Completion

## 1. Workspace model

Use one workspace per bank and one subdirectory per year:

```text
bank_<id>/
  sources/
  year_<year>/
    data/
    pages_300/
    question_crops/
    figures/
    shared_contexts/
    ocr_raw/
    review/
```

In Google Drive, use:

```text
<bank>/<year>/
  01_sources/
  02_working/
  03_validated/
  04_reports/
  05_human_review/
```

Original sources remain immutable.

## 2. Year-by-year state machine

```text
DISCOVERED
  -> SOURCE_LOCKED
  -> ANSWER_KEY_COMPLETE
  -> QUESTION_BLOCKS_EXTRACTED
  -> STRUCTURED_TRANSCRIPTION_COMPLETE
  -> FIGURE_CONTEXT_REVIEW_COMPLETE
  -> INTERNAL_SOURCE_REVIEW_COMPLETE
  -> MARKDOWN_REVIEW_PACKAGE_BUILT
  -> MARKDOWN_PACKAGE_QA_PASSED
  -> HUMAN_REVIEW_PACKAGE_PUBLISHED
  -> HUMAN_REVIEW_CORRECTIONS_RESOLVED
  -> YEAR_COMPLETE
```

Do not advance a second year in parallel.

## 3. Source audit

Record filename/role, SHA-256, file type, page count, native text quality, OCR requirement, and unusual layout notes.

## 4. Text-vs-image decision

A PDF text layer can be useless. Compare extracted text with visible exam content; if it is mainly watermark, headers, gibberish, or incomplete, treat the page as image-based.

## 5. Segmentation strategy order

Prefer:

1. explicit PDF structure/coordinates;
2. stable geometric question marker or separator;
3. OCR layout boxes plus numbering pattern;
4. page-level OCR plus parser;
5. manual bounding boxes for exceptions.

Count equality is necessary but not sufficient. Visually sample beginning, middle, end, and complex figure questions.

## 6. OCR strategy

Do not run full-page OCR and directly publish its text.

Preferred sequence:

1. render authoritative page;
2. segment question/context block;
3. OCR each block with relevant language models;
4. retain raw OCR;
5. normalize only safe typography/digits;
6. parse stem/options;
7. flag uncertainty;
8. compare with image source during internal review.

## 7. Figures

Always preserve the question source crop. Before publication, identify every question that contains a required visual element.

For each image-bearing question:

1. locate the figure/graph/pedigree/diagram/structure/table inside the source question/page;
2. crop only the required visual when separation is reliable;
3. preserve it without redrawing or reinterpretation;
4. save it under the review package `images/` directory with a deterministic filename;
5. visually open the saved crop and verify clipping and question association.

If multiple visuals exist, number them `_01`, `_02`, and so on.

## 8. Shared contexts

Represent passages/tables/diagrams used by multiple questions as separate records. Each question references `context_id`. Render shared text once in the Markdown package before the relevant questions.

## 9. Markdown review package

After internal extraction checks, create the canonical human-review package under `05_human_review`:

```text
<bank>_<year>_extracted_questions_review_vX.Y.Z.md
images/
validation_summary_vX.Y.Z.json
<bank>_<year>_review_md_package_vX.Y.Z.zip   # optional
```

The Markdown file must contain all extracted questions in order and use relative links to cropped visual assets.

Read `markdown-review-package.md` for the exact contract.

## 10. Final package QA

Before publishing or handing the package to the reviewer:

1. reopen the generated Markdown file;
2. verify expected question count and numbering;
3. verify every local image link resolves;
4. compare image-reference count with the image-bearing-question manifest;
5. visually open every image crop;
6. inspect first/middle/last questions and every section-boundary question;
7. verify shared contexts and image labels;
8. run `scripts/validate_markdown_review_v0.3.0.py`.

If QA fails, return to extraction/figure handling and regenerate the package. Do not publish a failed package.

## 11. Human review publication

Upload the Markdown package to `05_human_review` in Google Drive.

The reviewer has one task only: compare the extracted content with the original booklet and highlight incorrect parts. Prefer `==incorrect text==` as the machine-readable Markdown highlight convention.

If an image crop is incomplete or wrong, the reviewer highlights the nearby visible image label.

Do not require a Google Doc, Google Sheet, per-question approval, status fields, issue codes, reviewer names, dates, or notes.

Read `human-review-protocol.md` for the correction loop.

## 12. Completion

After the reviewer finishes:

1. inspect highlighted portions;
2. verify each against the authoritative source;
3. correct structured data or affected image crops;
4. regenerate the Markdown package;
5. rerun final package QA;
6. republish if needed.

A year becomes complete only when review is finished and all highlighted extraction errors are resolved. Only then unlock the next year.

For the full process diagram, read `pipeline-mermaid.md`.

If explanations are added later, keep them as a downstream feature unless the user changes the policy.
