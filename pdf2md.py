#!/usr/bin/env python3
"""
pdf2md.py — Convert PDF files to Markdown, optionally extracting images.

Quick start:
  pip install -r requirements.txt
  python pdf2md.py path/to/file.pdf
  python pdf2md.py path/to/folder  # converts all PDFs in the folder

Options:
  -o, --outdir           Output directory (default: ./out)
  --extract-images       Also extract images referenced by the Markdown
  --images-dir           Where to put extracted images (default: <outdir>/images)
  --skip-existing        Skip writing .md if it already exists
"""

import argparse
import sys
import shutil
from pathlib import Path

try:
    import pymupdf4llm  # noqa: F401
except ImportError:
    print("Missing dependency: pymupdf4llm. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

import pymupdf4llm


def is_pdf(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() == ".pdf"


def convert_pdf(
    pdf_path: Path,
    outdir: Path,
    extract_images: bool,
    images_dir: Path,
    skip_existing: bool,
) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    basename = pdf_path.stem
    md_path = outdir / f"{basename}.md"

    if skip_existing and md_path.exists():
        return md_path

    # Ensure images dir exists or is clean if extracting
    if extract_images:
        images_dir.mkdir(parents=True, exist_ok=True)

    # Convert
    try:
        if extract_images:
            # This writes images and returns markdown with local references
            md_text = pymupdf4llm.to_markdown(
                str(pdf_path),
                write_images=True,
                image_path=str(images_dir),
            )
        else:
            md_text = pymupdf4llm.to_markdown(str(pdf_path))
    except Exception as e:
        raise RuntimeError(f"Failed to convert '{pdf_path}': {e}") from e

    md_path.write_text(md_text, encoding="utf-8")
    return md_path


def main():
    parser = argparse.ArgumentParser(description="Convert PDF files to Markdown.")
    parser.add_argument("input", type=str, help="Path to a PDF file or a folder containing PDFs")
    parser.add_argument("-o", "--outdir", type=str, default="out", help="Output directory (default: ./out)")
    parser.add_argument(
        "--extract-images",
        action="store_true",
        help="Extract images and reference them from the Markdown",
    )
    parser.add_argument(
        "--images-dir",
        type=str,
        default=None,
        help="Directory for extracted images (default: <outdir>/images)",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip conversion if the target .md already exists",
    )
    parser.add_argument(
        "--clean-images",
        action="store_true",
        help="If set with --extract-images, clears the images dir before writing",
    )

    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    outdir = Path(args.outdir).expanduser().resolve()
    images_dir = Path(args.images_dir).expanduser().resolve() if args.images_dir else (outdir / "images")

    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if args.extract_images and args.clean_images and images_dir.exists():
        # Wipe existing images dir for a clean run
        shutil.rmtree(images_dir)

    targets = []
    if input_path.is_dir():
        targets = sorted([p for p in input_path.iterdir() if is_pdf(p)])
        if not targets:
            print(f"No PDFs found in: {input_path}", file=sys.stderr)
            sys.exit(1)
    elif is_pdf(input_path):
        targets = [input_path]
    else:
        print("Input must be a .pdf file or a directory of PDFs.", file=sys.stderr)
        sys.exit(1)

    converted = []
    errors = []

    for pdf in targets:
        try:
            md = convert_pdf(
                pdf_path=pdf,
                outdir=outdir,
                extract_images=args.extract_images,
                images_dir=images_dir,
                skip_existing=args.skip_existing,
            )
            converted.append((pdf, md))
        except Exception as e:
            errors.append((pdf, str(e)))

    # Summary
    if converted:
        print("Converted:")
        for pdf, md in converted:
            print(f"  {pdf.name} -> {md}")
    if errors:
        print("\nErrors:", file=sys.stderr)
        for pdf, msg in errors:
            print(f"  {pdf.name}: {msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
