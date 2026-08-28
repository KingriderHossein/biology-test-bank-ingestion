#!/usr/bin/env python3
"""Detect stable printed question markers using connected components and a year-specific config."""

import argparse
import json
from pathlib import Path

import cv2

VERSION = "0.1.0"


def in_range(v, rule, low, high):
    return rule.get(low, float("-inf")) <= v <= rule.get(high, float("inf"))


def matches(x, y, w, h, area, rule):
    return (
        in_range(x, rule, "x_min", "x_max")
        and in_range(y, rule, "y_min", "y_max")
        and in_range(w, rule, "w_min", "w_max")
        and in_range(h, rule, "h_min", "h_max")
        and in_range(area, rule, "area_min", "area_max")
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pages-dir", required=True, type=Path)
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("--expected-count", required=True, type=int)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    threshold = int(cfg.get("threshold", 180))
    dedup_y = int(cfg.get("dedup_y", 20))
    page_glob = cfg.get("page_glob", "page-*.png")
    page_regex_split = cfg.get("page_number_separator", "-")
    rules = cfg.get("components", [])
    if not rules:
        raise SystemExit("Config must contain at least one component rule")

    all_pages = []
    q = 1
    for page in sorted(args.pages_dir.glob(page_glob)):
        try:
            pn = int(page.stem.split(page_regex_split)[-1])
        except ValueError:
            continue
        im = cv2.imread(str(page), cv2.IMREAD_GRAYSCALE)
        if im is None:
            raise SystemExit(f"Could not read image: {page}")
        _, bw = cv2.threshold(im, threshold, 255, cv2.THRESH_BINARY_INV)
        _, _, stats, _ = cv2.connectedComponentsWithStats(bw, 8)
        found = []
        for x, y, w, h, area in stats[1:]:
            for rule in rules:
                if matches(int(x), int(y), int(w), int(h), int(area), rule):
                    found.append(
                        {
                            "page": pn,
                            "x": int(x),
                            "y": int(y),
                            "w": int(w),
                            "h": int(h),
                            "area": int(area),
                            "marker_class": rule.get("name", "marker"),
                        }
                    )
                    break
        found.sort(key=lambda z: z["y"])
        dedup = []
        for item in found:
            if not dedup or abs(item["y"] - dedup[-1]["y"]) >= dedup_y:
                item["question_number"] = q
                q += 1
                dedup.append(item)
        all_pages.append({"page": pn, "count": len(dedup), "markers": dedup})

    detected = q - 1
    payload = {
        "version": VERSION,
        "expected_count": args.expected_count,
        "detected_count": detected,
        "count_match": detected == args.expected_count,
        "pages": all_pages,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"version": VERSION, "detected": detected, "expected": args.expected_count}, indent=2))
    if detected != args.expected_count:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
