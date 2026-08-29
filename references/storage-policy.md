# Storage Policy

## Roles

Use two storage planes:

- **GitHub = control plane**: code, schemas, configs, hashes, quality gates, checkpoints, non-content metadata, workflow documentation, and Mermaid diagrams.
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
- `04_reports/`: audit summaries, QA/status reports, and legacy review artifacts that are no longer canonical.
- `05_human_review/`: the canonical Markdown review package for the active year.

## Canonical human-review package

Use this structure:

```text
05_human_review/
  <bank>_<year>_extracted_questions_review_vX.Y.Z.md
  images/
    qNNN_figure_01.png
    ...
  validation_summary_vX.Y.Z.json
  <bank>_<year>_review_md_package_vX.Y.Z.zip   # optional convenience bundle
```

The `.md` file plus `images/` directory are canonical. The ZIP is only a convenience bundle containing the same content.

Do not create a Google Doc, Google Sheet, approval table, issue-code form, reviewer-status system, or per-question checklist unless the user explicitly asks for it.

## Image storage rule

Every visual required by a question must be preserved in the review package as a faithful crop from the authoritative source. Do not redraw or regenerate source figures.

Keep full source question crops in `02_working/`; keep the smaller reviewer-facing visual crops in `05_human_review/images/` when published.

## Resume behavior

When resuming a project:

1. Read the GitHub checkpoint first.
2. Resolve the named Google Drive root and bank/year folder through connected Drive.
3. Treat Drive artifacts as authoritative for large working and review data.
4. Treat the GitHub checkpoint as authoritative for workflow state and active gate.
5. Read the canonical Markdown package state before deciding whether the year can close.
6. Never advance to the next year until the current year's Markdown review is finished and highlighted errors are resolved.

## Privacy

Do not persist private Drive folder IDs or private Drive URLs in a public GitHub repository unless the user explicitly requests it. Store logical names/paths instead.