#!/usr/bin/env python3
"""Parse question/answer integer pairs from a text or machine-readable PDF answer key."""

import argparse
import json
import re
import subprocess
import unicodedata
from pathlib import Path

VERSION = "0.1.0"
BIDI = dict.fromkeys(map(ord, "\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069"), None)
DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def clean(text: str) -> str:
    return unicodedata.normalize("NFKC", text.translate(BIDI).translate(DIGITS))


def load_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        try:
            return subprocess.check_output(["pdftotext", "-layout", str(path), "-"], text=True)
        except FileNotFoundError as e:
            raise SystemExit("pdftotext is required for PDF answer keys") from e
    return path.read_text(encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--expected-count", required=True, type=int)
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--bank-id", required=True)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--max-option", type=int, default=4)
    args = p.parse_args()

    text = clean(load_text(args.input))
    answers = {}
    conflicts = []
    for line in text.splitlines():
        nums = [int(x) for x in re.findall(r"\d+", line)]
        if len(nums) < 2:
            continue
        for i in range(0, len(nums) - 1, 2):
            q, a = nums[i], nums[i + 1]
            if 1 <= q <= args.expected_count and 1 <= a <= args.max_option:
                if q in answers and answers[q] != a:
                    conflicts.append({"question_number": q, "answers": [answers[q], a]})
                answers[q] = a

    missing = [q for q in range(1, args.expected_count + 1) if q not in answers]
    if conflicts or missing or len(answers) != args.expected_count:
        raise SystemExit(
            f"Answer-key validation failed: parsed={len(answers)}, missing={missing[:20]}, conflicts={conflicts[:10]}"
        )

    records = [
        {
            "bank_id": str(args.bank_id),
            "year": args.year,
            "question_number": q,
            "official_correct_option": answers[q],
            "answer_source": "official_key",
            "parser_version": VERSION,
        }
        for q in range(1, args.expected_count + 1)
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"version": VERSION, "parsed": len(records), "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
