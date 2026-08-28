# Storage Policy

## Roles

Use two storage planes:

- **GitHub = control plane**: code, schemas, configs, hashes, quality gates, checkpoints, non-content metadata.
- **Google Drive = data plane**: source archives/PDFs, rendered pages, question crops, figures, OCR/raw transcription, structured datasets, validated exports, and reports.

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
```

### Folder meanings

- `01_sources/`: immutable originals such as RAR/ZIP, question PDFs, answer-key PDFs/JPGs.
- `02_working/`: rendered pages, OCR output, question crops, figure crops, intermediate JSON.
- `03_validated/`: reviewed structured records and validated data exports for the completed year.
- `04_reports/`: audit summaries, QA reports, human-readable status documents.

## Google Docs

Use Google Docs for human-readable project logs, audit summaries, review notes, and completion reports. Do not use Google Docs as binary/object storage for PDFs, images, archives, or large structured datasets.

## Resume behavior

When resuming a project:

1. Read the GitHub checkpoint first.
2. Resolve the named Google Drive root and bank/year folder through the connected Drive.
3. Treat Drive artifacts as authoritative for large working data.
4. Treat the GitHub checkpoint as authoritative for workflow state and the active gate.
5. Never advance to the next year until the current year completion gate is persisted.

## Privacy

Do not persist private Drive folder IDs or private Drive URLs in a public GitHub repository unless the user explicitly requests it. Store logical names/paths instead.
