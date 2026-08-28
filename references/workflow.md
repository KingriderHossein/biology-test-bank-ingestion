# Workflow Reference

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
  -> HUMAN_REVIEW_DOC_PUBLISHED
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

Always preserve the question source crop. Track whether a figure is present and whether it has been isolated/verified.

## 8. Shared contexts

Represent passages/tables/diagrams used by multiple questions as separate records. Each question references `context_id`.

## 9. Human review publication

After the extracted year passes internal source checks, create one Google Doc under `05_human_review` containing all extracted questions in order.

Each question should show the extracted content needed for checking: number, stem, options, official answer, and figure/context when relevant.

The reviewer has one task only: compare with the original booklet and highlight incorrect extracted text or parts.

Do not require a Google Sheet, per-question approval, status fields, issue codes, reviewer names, dates, or notes.

Read `human-review-protocol.md` for the simple correction loop.

## 10. Completion

After the reviewer finishes, inspect highlighted portions, verify them against the source, correct the structured dataset, and update the review Doc if needed.

A year becomes complete when the review is finished and all highlighted extraction errors are resolved. Only then unlock the next year.

If explanations are added later, keep them as a downstream feature unless the user changes the policy.