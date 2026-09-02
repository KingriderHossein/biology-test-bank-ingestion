# Biology Test Bank Ingestion

Reusable ChatGPT Skill and deterministic helpers for converting exam archives/PDFs into a provenance-preserving structured question bank.

## Current version

Skill: `v0.4.0`

## Main rule

**One year at a time.** A later year remains locked until the active year passes machine validation, Markdown review-package validation, human review/correction, and final checkpoint persistence.

## Architecture

- `SKILL.md` — reusable control plane, routing, invariants, and gate order.
- `agents/openai.yaml` — UI metadata and default prompt.
- `scripts/` — deterministic helpers for source locking, answer-key parsing, segmentation, cropping, and validation.
- `references/` — runtime policies for storage, workflow, data, checkpoints, QA, Markdown review packages, and human review.
- `project/` — small project-specific checkpoints used to resume long-running banks across conversations.
- `CHANGELOG.md` — repository release history; it is not a runtime reference.

The repository does **not** publish raw exam PDFs, full question-image corpora, or the extracted copyrighted question corpus by default.

## Project state

Do not use README text as the authoritative status of a bank. Current state lives in:

`project/<bank-id>/current_checkpoint.json`

When resuming a bank, load its checkpoint and continue from the first incomplete or invalidated gate. This avoids stale project status in reusable Skill documentation.

## Persistent data

The default project architecture keeps reusable code, schemas, hashes, configs, and checkpoints in the control repository while large source/working/review artifacts use the configured Google Drive data plane. See `references/storage-policy.md` for the current policy.

## Runtime dependencies

The helper scripts use Python 3 and OpenCV. PDF rendering/text extraction uses Poppler command-line tools (`pdftoppm`, `pdftotext`, `pdfinfo`) when available.
