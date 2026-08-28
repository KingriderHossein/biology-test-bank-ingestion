# Biology Test Bank Ingestion

Reusable ChatGPT Skill and deterministic helpers for converting exam archives/PDFs into a provenance-preserving structured question bank.

## Main rule

**One year at a time.** A later year must remain locked until the active year passes its completion gate and its checkpoint is persisted.

## What the repository stores

- `SKILL.md` - reusable workflow instructions.
- `scripts/` - deterministic helpers for source locking, answer-key parsing, segmentation, cropping, and validation.
- `references/` - data contract, quality gates, checkpoint protocol, and workflow rules.
- `project/` - small non-content checkpoints used to resume long-running banks across chats.

It does **not** publish raw exam PDFs, full question images, or the extracted copyrighted question corpus by default.

## Current seeded project

`project/1206/current_checkpoint.json` records the current state of exam code 1206. Year 1404 is active. Source lock, 190/190 official answers, and 190/190 source question crops are complete. Structured transcription is the next gate.

## Version

Skill: `v0.1.0`

## Runtime dependencies

The helper scripts use Python 3 and OpenCV. PDF rendering/text extraction uses Poppler command-line tools (`pdftoppm`, `pdftotext`, `pdfinfo`) when available.
