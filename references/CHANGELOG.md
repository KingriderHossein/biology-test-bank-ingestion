# Changelog

## v0.2.0 - 2026-08-29

- Added an independent human-review gate before year completion.
- Added `references/human-review-protocol.md` with reviewer states, issue codes, correction loop, and pass criteria.
- Added `05_human_review` to the Google Drive year layout.
- Defined Google Sheets as the default question-level review surface.
- Required one review row per expected question and all rows to be `APPROVED` before the next year is unlocked.
- Added reviewer findings and correction history to provenance requirements.
- Seeded a 190-row human-review template for bank 1206 / year 1404.
- Bumped the active project checkpoint to v0.3.0.

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
