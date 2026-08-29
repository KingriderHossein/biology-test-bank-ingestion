# Human Review Protocol

## Purpose

Use a minimal independent human check after question extraction. The reviewer should not fill forms, classify errors, or approve every question individually.

## One Markdown package per year

After the active year has been extracted and internally checked:

1. Build one Markdown review file for the year.
2. Put every extracted question in exact exam order.
3. Keep shared passages/contexts once, immediately before the questions that use them.
4. For every image-bearing question, include the required cropped source visual through a relative `images/...` Markdown link.
5. Reopen and validate the package before publishing it to `05_human_review/`.

Read `markdown-review-package.md` for the output contract.

## Reviewer instruction

Tell the reviewer only this:

**Compare the Markdown questions with the original booklet and highlight only the extracted parts that are wrong. Do not fill any form or status field.**

Preferred Markdown marking convention:

```markdown
==incorrect extracted text==
```

The reviewer may highlight a whole line, word, option, number, formula, label, or other incorrect extracted part.

If a figure/image crop is wrong, incomplete, or belongs to the wrong question, highlight the visible image label next to that image. No explanation is required.

## Correction loop

1. Read the reviewer highlights from the returned Markdown file.
2. Compare each highlighted part with the authoritative source page/question crop.
3. Correct the structured dataset, not the original source or raw OCR.
4. If the error concerns an image, recrop the affected visual from the authoritative source.
5. Regenerate the Markdown package.
6. Reopen and rerun final package QA, including image-link validation and visual inspection of affected crops.
7. Republish the corrected package.
8. Repeat only when unresolved highlights remain.

## Pass condition

The human-review gate passes when:

- the reviewer has completed the review;
- all highlighted extraction errors are corrected or explicitly resolved;
- the regenerated final Markdown package passes QA;
- no unresolved image-crop problem remains.

No per-question approval table, issue code, reviewer identity field, review date, review state, Google Doc, Google Sheet, or correction form is required.

Do not unlock the next year before this gate passes.