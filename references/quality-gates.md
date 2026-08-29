# Quality Gates

## Gate 0 - Source locked
Pass when:
- required source files exist;
- hashes are stored;
- year and source roles are unambiguous.

## Gate 1 - Answer key complete
Pass when:
- expected number of question-answer pairs is present;
- question numbers are complete and unique;
- options are in allowed range;
- provenance is recorded.

## Gate 2 - Question blocks extracted
Pass when:
- exactly the expected question count is segmented;
- each question has one source page/region and source crop;
- beginning/middle/end visual samples pass;
- complex/page-boundary exceptions are logged.

## Gate 3 - Structured transcription
Pass when:
- each question has stem and expected options or an explicit type-specific structure;
- raw OCR is retained;
- parse failures are zero or logged as blocking exceptions.

## Gate 4 - Figure/context review
Pass when:
- every shared passage/context is separately represented and mapped;
- every image-bearing question is identified;
- every required visual has a faithful source crop or a logged blocking exception;
- visual assets are not redrawn or model-regenerated.

## Gate 5 - Internal extraction QA
Pass when:
- question boundaries and option ordering are checked;
- obvious OCR errors are corrected in cleaned text while raw OCR is preserved;
- scientific symbols/names and mixed-language text are reviewed as needed;
- answer, context, and figure associations are consistent;
- no blocking extraction exception remains.

## Gate 6 - Markdown review package QA
Pass when:
- the yearly `.md` review file contains exactly the expected number of question headings;
- numbering is complete, unique, and in range;
- every local image link resolves;
- image-reference count matches the image-bearing-question manifest;
- every published image crop has been opened and visually checked for clipping, wrong association, and missing essential content;
- shared contexts occur in the intended location;
- first, middle, last, and section-boundary questions have been rechecked;
- `scripts/validate_markdown_review_v0.3.0.py` returns success;
- no unresolved placeholder/image-label mismatch remains.

## Gate 7 - Human review complete
Pass when:
- the Markdown review package has been published in Google Drive;
- the reviewer has completed comparison against the original booklet;
- all highlighted text/image-crop errors are corrected or explicitly resolved;
- the regenerated final package passes Gate 6 again.

## Gate 8 - Year complete
Pass when:
- all project-required gates are true;
- validator returns success;
- final checkpoint is persisted;
- next year remains untouched until this state is saved.
