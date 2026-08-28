# Storage Policy

## Roles

Use two storage planes:

- **GitHub = control plane**: code, schemas, configs, hashes, quality gates, checkpoints, non-content metadata.
- **Google Drive = data plane**: source archives/PDFs, rendered pages, question crops, figures, OCR/raw transcription, structured datasets, validated exports, reports, and human-review packages.

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
- `04_reports/`: audit summaries, QA reports, narrative status documents.
- `05_human_review/`: independent reviewer package, question-level Google Sheet review queue, source references, review findings, and correction/re-review artifacts.

## Google Sheets

Use a native Google Sheet as the default question-level human-review surface. Keep one row per expected question and store reviewer state, issue type, note, reviewer identity, and review date. Human review is part of the completion gate.

## Google Docs

Use Google Docs for human-readable project logs, audit summaries, narrative review notes, and completion reports. Do not use Google Docs as binary/object storage for PDFs, images, archives, or large structured datasets.

## Resume behavior

When resuming a project:

1. Read the GitHub checkpoint first.
2. Resolve the named Google Drive root and bank/year folder through the connected Drive.
3. Treat Drive artifacts as authoritative for large working and human-review data.
4. Treat the GitHub checkpoint as authoritative for workflow state and the active gate.
5. Read human-review state before deciding whether the year can close.
6. Never advance to the next year until the current year human-review completion gate is persisted.

## Privacy

Do not persist private Drive folder IDs or private Drive URLs in a public GitHub repository unless the user explicitly requests it. Store logical names/paths instead.
