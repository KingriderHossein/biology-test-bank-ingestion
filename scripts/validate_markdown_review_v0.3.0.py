#!/usr/bin/env python3
"""Validate a yearly Markdown human-review package.

Checks:
- expected number of question headings;
- unique and complete question numbering from 1..N;
- all local Markdown image references resolve;
- optional expected number of images.

This intentionally does not judge OCR/text correctness; that remains a source-review task.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

QUESTION_RE = re.compile(r"^###\s+(?:سؤال|Question)\s+(\d+)\s*$", re.MULTILINE)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--expected-count", type=int, required=True)
    parser.add_argument("--expected-images", type=int, default=None)
    parser.add_argument("--json-out", type=Path, default=None)
    args = parser.parse_args()

    md_path = args.markdown.resolve()
    text = md_path.read_text(encoding="utf-8")

    numbers = [int(x) for x in QUESTION_RE.findall(text)]
    seen = set(numbers)
    expected = set(range(1, args.expected_count + 1))

    duplicates = sorted(n for n in seen if numbers.count(n) > 1)
    missing = sorted(expected - seen)
    out_of_range = sorted(seen - expected)

    image_refs = IMAGE_RE.findall(text)
    local_image_refs = [
        r for r in image_refs
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", r)
    ]
    missing_images = []
    for ref in local_image_refs:
        path_part = ref.strip().split(' "', 1)[0].split(" '", 1)[0]
        path = (md_path.parent / path_part).resolve()
        if not path.exists():
            missing_images.append(ref)

    checks = {
        "question_count_matches": len(numbers) == args.expected_count,
        "question_numbers_complete": not missing,
        "question_numbers_unique": not duplicates,
        "question_numbers_in_range": not out_of_range,
        "all_local_images_resolve": not missing_images,
    }
    if args.expected_images is not None:
        checks["image_count_matches"] = len(image_refs) == args.expected_images

    passed = all(checks.values())
    result = {
        "markdown": str(md_path),
        "expected_question_count": args.expected_count,
        "observed_question_count": len(numbers),
        "first_question": min(numbers) if numbers else None,
        "last_question": max(numbers) if numbers else None,
        "missing_questions": missing,
        "duplicate_questions": duplicates,
        "out_of_range_questions": out_of_range,
        "image_reference_count": len(image_refs),
        "missing_image_references": missing_images,
        "checks": checks,
        "passed": passed,
    }

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload + "\n", encoding="utf-8")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
