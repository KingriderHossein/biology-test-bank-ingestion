#!/usr/bin/env python3
"""Render a PDF to page PNGs with pdftoppm."""

import argparse
import shutil
import subprocess
from pathlib import Path

VERSION = "0.1.0"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pdf", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    p.add_argument("--dpi", type=int, default=300)
    args = p.parse_args()

    if shutil.which("pdftoppm") is None:
        raise SystemExit("pdftoppm is required")
    if not args.pdf.is_file():
        raise SystemExit(f"Missing PDF: {args.pdf}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.out_dir / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(args.dpi), str(args.pdf), str(prefix)],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    files = sorted(args.out_dir.glob("page-*.png"))
    print(f"render_pdf v{VERSION}: rendered {len(files)} page(s) at {args.dpi} DPI")


if __name__ == "__main__":
    main()
