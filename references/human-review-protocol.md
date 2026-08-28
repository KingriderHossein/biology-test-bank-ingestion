# Human Review Protocol

## Purpose

Use a minimal independent human check after question extraction. The reviewer should not fill forms, classify errors, or approve every question individually.

## One Google Doc per year

After the active year has been extracted and internally checked:

1. Create one native Google Doc under that year's `05_human_review/` folder.
2. Put every extracted question in order in the Doc.
3. For each question include the question number, extracted stem, extracted options, and official answer. Include the relevant figure/context when needed to verify the extraction.
4. Keep the document simple and easy to scan.

## Reviewer instruction

Tell the reviewer only this:

**Compare the extracted questions with the original booklet and highlight any text or extracted part that is wrong. Do not fill any form or status field.**

The reviewer may highlight a whole line, word, option, number, formula, label, or other incorrect extracted part.

## Correction loop

1. Read the highlighted portions from the review Doc.
2. Compare each highlighted portion with the authoritative source page/crop.
3. Correct the structured dataset.
4. Update the review Doc when the visible extraction changes.
5. Keep the original source and raw OCR unchanged.

## Pass condition

The human-review gate passes when the reviewer has completed the review and all highlighted extraction errors are corrected or explicitly resolved.

No per-question approval table, issue code, reviewer identity field, review date, review state, or correction form is required.

Do not unlock the next year before this gate passes.