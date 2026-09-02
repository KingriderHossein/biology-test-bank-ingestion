# Changelog

## v0.4.0 - 2026-09-02

- Refactored `SKILL.md` into a reusable control plane with progressive reference loading.
- Separated reusable Skill behavior from project-specific state; active bank/year/progress now belongs in `project/<bank-id>/current_checkpoint.json` rather than the Skill entrypoint or README.
- Added explicit resume routing that treats the checkpoint as authoritative and avoids repeating completed gates unless evidence was invalidated.
- Made `references/quality-gates.md` the authoritative completion policy instead of duplicating the full gate checklist in `SKILL.md`.
- Made `references/pipeline-mermaid.md` optional human-facing workflow documentation rather than a required runtime read.
- Clarified persistence failure behavior: do not claim Drive/repository persistence when the configured write did not occur.
- Added `default_prompt` to `agents/openai.yaml`.
- Moved this changelog from `references/` to repository root so it is not part of runtime reference context.
- Updated README and corrected the stale Skill version.

## v0.3.0 - 2026-08-29

- Replaced the canonical yearly human-review Google Doc with a Markdown review package.
- Canonical review output is now `.md` plus a relative `images/` directory in Google Drive.
- Added mandatory detection and source-cropping of every required question visual.
- Required faithful visual crops; source figures must not be redrawn or model-regenerated.
- Added `references/markdown-review-package.md` with output, image, QA, and reviewer-marking rules.
- Added `references/pipeline-mermaid.md` with the full end-to-end year-by-year workflow.
- Added `scripts/validate_markdown_review_v0.3.0.py` to check question counts, numbering, image references, and optional image counts.
- Added mandatory final package QA after Markdown generation and before publication.
- Standardized simple machine-readable reviewer highlighting as `==incorrect text==` when supported by the Markdown editor.
- Defined image-crop review: highlight the visible image label when the crop itself is wrong.
- Moved legacy Google Docs out of the canonical `05_human_review` path; they may be retained under `04_reports` for history.
- Updated the active 1206/1404 checkpoint to the Markdown review workflow.

## v0.2.1 - 2026-08-29

- Simplified the human-review workflow based on user feedback.
- Replaced the Google Sheets review queue with one Google Doc per year.
- Reviewer task is now only: compare with the original booklet and highlight incorrect extracted text/parts.
- Removed required per-question approval states, issue codes, reviewer identity, dates, notes, and approval rows.
- Human-review completion now means the reviewer finished and all highlighted extraction errors were resolved.
- Kept `05_human_review` as the Drive destination for the yearly review Doc.
- Bumped the active project checkpoint to v0.3.1.

## v0.2.0 - 2026-08-29

- Added an independent human-review gate before year completion.
- Added `references/human-review-protocol.md`.
- Added `05_human_review` to the Google Drive year layout.

## v0.1.1 - 2026-08-29

- Added Google Drive as the default persistent data plane for large source and working artifacts.
- Kept GitHub as the control plane for code, schemas, checkpoints, hashes, configs, and non-content metadata.
- Added `references/storage-policy.md` with the logical Drive layout and privacy rules.
- Added the logical Drive path for bank 1206 / year 1404 to the persistent checkpoint.
- Defined Google Docs as the surface for human-readable logs and reports, not binary/object storage.
- Bumped the active project checkpoint to v0.2.2.

## v0.1.0 - 2026-08-29

- Initial reusable question-bank ingestion skill.
- Enforced strict one-year-at-a-time execution.
- Added persistent checkpoint protocol for cross-chat continuation.
- Added provenance-preserving data contract and six quality gates.
- Added reusable scripts for workspace initialization, answer-key parsing, marker detection, question cropping, and year validation.
- Seeded project state for Biology exam code 1206, active year 1404.
