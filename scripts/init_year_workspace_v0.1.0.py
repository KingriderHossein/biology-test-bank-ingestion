#!/usr/bin/env python3
"""Initialize a provenance-preserving workspace for one exam year."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

VERSION = "0.1.0"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_pages(path: Path):
    if path.suffix.lower() != ".pdf":
        return None
    try:
        out = subprocess.check_output(["pdfinfo", str(path)], text=True, stderr=subprocess.STDOUT)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    for line in out.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def source_record(path: Path):
    return {
        "name": path.name,
        "sha256": sha256(path),
        "size_bytes": path.stat().st_size,
        "page_count": pdf_pages(path),
        "native_text_quality": "unknown",
        "ocr_required": None,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bank-id", required=True)
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--question-source", required=True, type=Path)
    p.add_argument("--answer-source", required=True, type=Path)
    p.add_argument("--expected-count", required=True, type=int)
    p.add_argument("--out-dir", required=True, type=Path)
    args = p.parse_args()

    for path in (args.question_source, args.answer_source):
        if not path.is_file():
            raise SystemExit(f"Missing source file: {path}")

    year_dir = args.out_dir / f"year_{args.year}"
    for name in ("data", "pages_300", "question_crops", "figures", "shared_contexts", "ocr_raw", "review"):
        (year_dir / name).mkdir(parents=True, exist_ok=True)

    manifest = {
        "pipeline_version": VERSION,
        "bank_id": str(args.bank_id),
        "year": args.year,
        "expected_question_count": args.expected_count,
        "source_files": {
            "questions": source_record(args.question_source),
            "answer_key": source_record(args.answer_source),
        },
        "gates": {
            "source_locked": True,
            "answer_key_complete": False,
            "question_blocks_extracted": False,
            "structured_transcription_complete": False,
            "figure_context_review_complete": False,
            "human_text_review_complete": False,
            "year_complete": False,
        },
        "exceptions": [],
    }
    out = year_dir / "data" / "year_manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"version": VERSION, "manifest": str(out), "source_locked": True}, indent=2))


if __name__ == "__main__":
    main()
