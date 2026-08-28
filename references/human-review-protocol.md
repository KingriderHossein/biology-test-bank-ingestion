# Human Review Protocol

## Purpose

Add an independent human verification layer between structured extraction and year completion.

## Required Drive package per year

Under the active year folder create `05_human_review/` and place or link:

- source question crops or source-reference files;
- structured question dataset for the year;
- official answer mapping;
- figure/shared-context references;
- a native Google Sheet review queue with one row per expected question;
- optional narrative QA/completion report.

## Review queue columns

At minimum include:

- question number;
- subject;
- source page;
- source crop/reference link;
- stem;
- options;
- official answer;
- figure flag;
- shared context ID;
- extraction status;
- reviewer result;
- issue type;
- reviewer note;
- reviewer identity;
- review date.

## Reviewer result states

- `PENDING`: not reviewed yet.
- `APPROVED`: extraction, options, source association, figure/context association, and answer mapping are acceptable.
- `NEEDS_CORRECTION`: a concrete correction is required.
- `UNCLEAR`: source or mapping is ambiguous and needs escalation.

## Issue types

Use stable issue codes when possible:

- `NONE`
- `OCR_TEXT`
- `OPTION_ORDER`
- `QUESTION_BOUNDARY`
- `FIGURE`
- `SHARED_CONTEXT`
- `ANSWER_MAPPING`
- `OTHER`

## Correction loop

1. Preserve the reviewer finding as an immutable review record.
2. Correct the structured dataset, not the reviewer history.
3. Record what changed and which question IDs were affected.
4. Return corrected questions for re-review when the change affects visible question content, option order, figure/context association, or answer mapping.
5. Resolve the finding only after the corrected version is accepted.

## Pass condition

The human-review gate passes only when:

- total review rows equals expected question count;
- every expected question is `APPROVED`;
- `PENDING = 0`;
- `NEEDS_CORRECTION = 0`;
- `UNCLEAR = 0`;
- all correction loops are closed.

Do not unlock the next year before these conditions are met.

## Independence

The reviewer should compare the published extraction against the authoritative source. Do not ask the reviewer to trust OCR/model output or infer missing text from the extraction itself.