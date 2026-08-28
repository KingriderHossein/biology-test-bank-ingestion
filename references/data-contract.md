# Data Contract

## Year manifest

Required minimum fields:

```json
{
  "pipeline_version": "0.1.0",
  "bank_id": "1206",
  "year": 1404,
  "expected_question_count": 190,
  "source_files": {},
  "gates": {},
  "exceptions": []
}
```

## Question source record

```json
{
  "bank_id": "1206",
  "year": 1404,
  "question_number": 1,
  "subject": "english",
  "source_page": 2,
  "source_region": {"x0": 0, "y0": 0, "x1": 0, "y1": 0, "dpi": 300},
  "source_crop": "question_crops/q001_p02.jpg",
  "official_correct_option": 2,
  "answer_source": "official_key",
  "stem_raw": null,
  "stem_clean": null,
  "options_raw": null,
  "options_clean": null,
  "has_figure": null,
  "figure_status": "unknown",
  "context_id": null,
  "extraction_status": "segmented",
  "text_review_status": "pending",
  "answer_review_status": "official_unreviewed",
  "pipeline_version": "0.1.0"
}
```

## Invariants

- Question numbers are unique within `(bank_id, year)`.
- Official answer is an integer in the configured option range or an explicit null with an exception reason.
- Raw and clean fields are distinct.
- Every published question has a source page or equivalent provenance pointer.
- Every asset reference must resolve in the working dataset.
- `YEAR_COMPLETE` requires zero blocking exceptions.
