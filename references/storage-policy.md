# Storage Policy

## Roles

Use two storage planes:

- **GitHub = control plane**: code, schemas, configs, hashes, quality gates, checkpoints, non-content metadata.
- **Google Drive = data plane**: source archives/PDFs, rendered pages, question crops, figures, OCR/raw transcription, structured datasets, validated exports, reports, and human-review documents.

Do not put raw copyrighted exam content or large binary artifacts in the public GitHub repository by default.

## Google Drive logical layout

Root folder: `Biology Test Bank Ingestion`

Per bank/year:

```text
Biology Test Bank Ingestion/
  <bank-id>/
    <year>/
      01_sources/
      02_working/
      03_validated/
      04_reports/
      05_human_review/
```

### Folder meanings

- `01_sources/`: immutable originals such as RAR/ZIP, question PDFs, answer-key PDFs/JPGs.
- `02_working/`: rendered pages, OCR output, question crops, figure crops, intermediate JSON.
- `03_validated/`: internally reviewed structured records and validated data exports for the active year.
- `04_reports/`: audit summaries and QA/status reports.
- `05_human_review/`: one Google Doc containing the active year's extracted questions for the reviewer to highlight incorrect parts.

## Human-review document

Use one native Google Doc per year. Put all extracted questions in order. The reviewer only highlights incorrect extracted text or parts.

Do not create a Google Sheet, approval table, issue-code form, reviewer-status system, or per-question checklist unless the user explicitly asks for it.

## Resume behavior

When resuming a project:

1. Read the GitHub checkpoint first.
2. Resolve the named Google Drive root and bank/year folder through connected Drive.
3. Treat Drive artifacts as authoritative for large working and review data.
4. Treat the GitHub checkpoint as authoritative for workflow state and active gate.
5. Never advance to the next year until the current year's review Doc has been completed and highlighted errors are resolved.

## Privacy

Do not persist private Drive folder IDs or private Drive URLs in a public GitHub repository unless the user explicitly requests it. Store logical names/paths instead.