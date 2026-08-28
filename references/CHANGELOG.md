# Changelog

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
