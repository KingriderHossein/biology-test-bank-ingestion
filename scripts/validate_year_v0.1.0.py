#!/usr/bin/env python3
"""Validate a year workspace and optionally enforce YEAR_COMPLETE."""

import argparse
import json
from pathlib import Path

VERSION = "0.1.0"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--answers", type=Path)
    p.add_argument("--source-map", type=Path)
    p.add_argument("--structured", type=Path)
    p.add_argument("--require-complete", action="store_true")
    args = p.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    expected = int(manifest["expected_question_count"])
    errors = []
    warnings = []

    if not manifest.get("gates", {}).get("source_locked"):
        errors.append("source_locked=false")

    if args.answers:
        answers = json.loads(args.answers.read_text(encoding="utf-8"))
        qs = [int(r["question_number"]) for r in answers]
        if len(answers) != expected or sorted(qs) != list(range(1, expected + 1)):
            errors.append(f"answer key not complete: {len(answers)}/{expected}")
        bad = [r for r in answers if not 1 <= int(r["official_correct_option"]) <= 4]
        if bad:
            errors.append(f"invalid official answers: {len(bad)}")

    if args.source_map:
        source_map = json.loads(args.source_map.read_text(encoding="utf-8"))
        qs = [int(r["question_number"]) for r in source_map]
        if len(source_map) != expected or sorted(qs) != list(range(1, expected + 1)):
            errors.append(f"source map not complete: {len(source_map)}/{expected}")

    if args.structured:
        structured = json.loads(args.structured.read_text(encoding="utf-8"))
        if len(structured) != expected:
            errors.append(f"structured records not complete: {len(structured)}/{expected}")
        for r in structured:
            if not r.get("stem_clean"):
                errors.append(f"Q{r.get('question_number')}: missing stem_clean")
                if len(errors) > 20:
                    break

    blocking = manifest.get("exceptions", [])
    if blocking:
        warnings.append(f"manifest contains {len(blocking)} exception(s)")

    if args.require_complete:
        required = [
            "source_locked",
            "answer_key_complete",
            "question_blocks_extracted",
            "structured_transcription_complete",
            "figure_context_review_complete",
            "human_text_review_complete",
            "year_complete",
        ]
        for gate in required:
            if not manifest.get("gates", {}).get(gate):
                errors.append(f"completion gate false: {gate}")
        if blocking:
            errors.append("blocking exceptions remain")

    result = {
        "validator_version": VERSION,
        "bank_id": manifest.get("bank_id"),
        "year": manifest.get("year"),
        "expected": expected,
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
