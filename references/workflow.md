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

Original sources remain immutable. Generated outputs can be reproduced from source hashes plus config/script versions.

## 2. Year-by-year state machine

```text
DISCOVERED
  -> SOURCE_LOCKED
  -> ANSWER_KEY_COMPLETE
  -> QUESTION_BLOCKS_EXTRACTED
  -> STRUCTURED_TRANSCRIPTION_COMPLETE
  -> FIGURE_CONTEXT_REVIEW_COMPLETE
  -> HUMAN_TEXT_REVIEW_COMPLETE
  -> YEAR_COMPLETE
```

Do not advance a second year in parallel.

## 3. Source audit

For each source record:

- filename and role;
- SHA-256;
- file type;
- page count if relevant;
- native text quality: `usable`, `partial`, `watermark_only`, `none`, `unknown`;
- OCR required: true/false;
- notes about image quality, skew, columns, or unusual layout.

## 4. Text-vs-image decision

A PDF can contain a text layer that is useless. Sample representative pages and compare extracted text with visible exam content. If extraction yields mostly watermark, headers, gibberish, or incomplete content, treat the page as image-based.

## 5. Segmentation strategy order

Prefer strategies in this order when reliable:

1. explicit PDF structure/coordinates;
2. stable geometric question marker or separator;
3. OCR layout boxes plus numbering pattern;
4. page-level OCR plus parser;
5. manual bounding boxes for exceptions.

Count equality is necessary but not sufficient. Visually sample beginning, middle, end, and complex figure questions.

## 6. OCR strategy

Do not run a single full-page OCR and directly publish its text.

Preferred sequence:

1. render authoritative page;
2. segment question/context block;
3. OCR each block with relevant language models;
4. retain raw OCR;
5. normalize only safe typography/digits;
6. parse stem/options;
7. flag uncertainty;
8. compare with image source during review.

## 7. Figures

A question source crop is always preserved even if a separate figure crop is produced. `has_figure=true` does not mean the figure was successfully isolated; track a separate `figure_status`.

Suggested statuses:

- `none`
- `present_in_source_crop`
- `isolated_pending_review`
- `isolated_verified`

## 8. Shared contexts

Represent passages/tables/diagrams used by multiple questions as separate records. Each question references `context_id`; context stores its own source page/region and review state.

## 9. Completion

Year completion must be explicitly validated. If the project allows explanations to be added later, keep explanation completion as a separate downstream gate rather than blocking the verified-question dataset unless the user changes the policy.
