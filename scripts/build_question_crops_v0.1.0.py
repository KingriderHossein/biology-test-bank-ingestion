#!/usr/bin/env python3
"""Build question source crops from validated marker positions and official answers."""

import argparse
import json
from pathlib import Path

import cv2

VERSION = "0.1.0"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pages-dir", required=True, type=Path)
    p.add_argument("--markers", required=True, type=Path)
    p.add_argument("--answers", required=True, type=Path)
    p.add_argument("--bank-id", required=True)
    p.add_argument("--year", required=True, type=int)
    p.add_argument("--x0", required=True, type=int)
    p.add_argument("--x1", required=True, type=int)
    p.add_argument("--body-bottom", required=True, type=int)
    p.add_argument("--top-padding", type=int, default=25)
    p.add_argument("--next-padding", type=int, default=12)
    p.add_argument("--out-dir", required=True, type=Path)
    p.add_argument("--map-out", required=True, type=Path)
    args = p.parse_args()

    marker_data = json.loads(args.markers.read_text(encoding="utf-8"))
    if not marker_data.get("count_match"):
        raise SystemExit("Marker count is not validated")
    markers = [m for page in marker_data["pages"] for m in page["markers"]]
    markers.sort(key=lambda m: m["question_number"])

    answer_records = json.loads(args.answers.read_text(encoding="utf-8"))
    answers = {int(r["question_number"]): r for r in answer_records}
    if len(answers) != len(markers):
        raise SystemExit(f"Answer/marker mismatch: answers={len(answers)}, markers={len(markers)}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for idx, marker in enumerate(markers):
        q = int(marker["question_number"])
        page_num = int(marker["page"])
        page_path = args.pages_dir / f"page-{page_num:02d}.png"
        im = cv2.imread(str(page_path))
        if im is None:
            raise SystemExit(f"Missing rendered page: {page_path}")
        start = max(0, int(marker["y"]) - args.top_padding)
        if idx + 1 < len(markers) and int(markers[idx + 1]["page"]) == page_num:
            end = max(start + 40, int(markers[idx + 1]["y"]) - args.next_padding)
        else:
            end = min(args.body_bottom, im.shape[0])
        crop = im[start:end, args.x0:args.x1]
        out = args.out_dir / f"q{q:03d}_p{page_num:02d}.jpg"
        ok = cv2.imwrite(str(out), crop, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
        if not ok:
            raise SystemExit(f"Failed to write crop: {out}")
        a = answers[q]
        records.append(
            {
                "bank_id": str(args.bank_id),
                "year": args.year,
                "question_number": q,
                "source_page": page_num,
                "source_region": {"x0": args.x0, "y0": start, "x1": args.x1, "y1": end, "dpi": 300},
                "source_crop": str(out.name),
                "official_correct_option": int(a["official_correct_option"]),
                "answer_source": a.get("answer_source", "official_key"),
                "stem_raw": None,
                "stem_clean": None,
                "options_raw": None,
                "options_clean": None,
                "has_figure": None,
                "figure_status": "unknown",
                "context_id": None,
                "extraction_status": "segmented",
                "text_review_status": "pending",
                "pipeline_version": VERSION,
            }
        )

    args.map_out.parent.mkdir(parents=True, exist_ok=True)
    args.map_out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"version": VERSION, "crops": len(records), "map": str(args.map_out)}, indent=2))


if __name__ == "__main__":
    main()
