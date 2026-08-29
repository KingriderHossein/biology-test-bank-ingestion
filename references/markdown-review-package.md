# Markdown Review Package

## Canonical yearly review output

The human-review deliverable for each year is a Markdown package, not a Google Doc.

Place the package under the active year's `05_human_review/` folder in Google Drive:

```text
05_human_review/
  <bank>_<year>_extracted_questions_review_vX.Y.Z.md
  images/
    qNNN_figure_01.png
    qNNN_figure_02.png
    ...
  validation_summary_vX.Y.Z.json
  <bank>_<year>_review_md_package_vX.Y.Z.zip   # optional convenience bundle
```

The `.md` file and `images/` directory are the canonical review surface. A ZIP may be produced only as a convenience copy of the same package.

## Markdown structure

- Keep questions in exact exam order.
- Use one heading per question, for example `### سؤال 66` or `### Question 66`.
- Shared passages/contexts appear once before the questions that reference them.
- Keep extracted text editable as plain Markdown text so a reviewer can mark errors directly.
- Do not embed raw full-page screenshots when a smaller source figure is sufficient.

## Image-bearing questions

For every question that contains a visual element needed to understand or verify the question, preserve that visual as an image asset. This includes figures, graphs, pedigrees, diagrams, chemical/molecular structures, image-based tables, maps, and other non-text visual evidence.

Rules:

1. Detect image-bearing questions before publishing the package.
2. Crop the visual from the authoritative rendered source page/question crop.
3. Crop the visual itself, not the entire question block, unless the visual cannot be separated reliably.
4. Do not redraw, regenerate, beautify, or reinterpret the visual.
5. Save images with deterministic names such as `images/q066_figure_01.png`.
6. If a question has multiple independent visuals, use `_02`, `_03`, and so on.
7. Insert the image immediately below a visible label in the question block:

```markdown
**تصویر/نمودار منبع سؤال 66:**

![تصویر سؤال 66](images/q066_figure_01.png)
```

If the crop itself is wrong or incomplete, the reviewer can mark/highlight the visible image label.

## Mandatory final QA before publication

After generating the Markdown package, reopen and validate it before upload.

At minimum verify:

- question count equals the expected count;
- question numbering is complete, unique, and in range;
- first and last expected questions are present;
- every local Markdown image reference resolves;
- image-reference count matches the image-bearing-question manifest;
- every image crop is opened visually and checked for wrong-question association, clipping, or missing essential content;
- shared contexts are present once and mapped to the intended questions;
- section-boundary questions do not contain material from the next section;
- no stale placeholder such as `تصویر...` remains without an actual image reference;
- the final file is UTF-8 Markdown.

Run `scripts/validate_markdown_review_v0.3.0.py` for deterministic structural checks. Structural validation does not replace source/text review.

## Reviewer marking convention

The reviewer has one job: compare the Markdown package with the original booklet and highlight only incorrect extracted parts.

When the Markdown editor supports highlight syntax, use:

```markdown
==incorrect extracted text==
```

This `==...==` convention is preferred because it is simple and machine-searchable. No form, status table, issue code, reviewer name, or written explanation is required.

For an incorrect or incomplete image crop, highlight the nearby image label rather than editing the image.

## Correction loop

1. Read reviewer highlights.
2. Compare each highlighted fragment with the authoritative source.
3. Correct the structured dataset, not the raw OCR/source.
4. Regenerate the Markdown package and affected image crops if needed.
5. Run final QA again.
6. Republish the corrected package.
7. Repeat until the reviewer is finished and no unresolved highlighted errors remain.

Do not unlock the next year before this loop is complete.