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
- every suspected figure has a reviewed figure status;
- every shared passage/context is separately represented and mapped.

## Gate 5 - Human text review
Pass when:
- all required question text is compared against source;
- option order is verified;
- scientific symbols/names are checked;
- no blocking text exceptions remain.

## Gate 6 - Year complete
Pass when:
- all project-required gates are true;
- validator returns success;
- checkpoint is persisted;
- next year remains untouched until this state is saved.
