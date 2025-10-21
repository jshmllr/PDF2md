# pdf2md

Convert PDFs to clean Markdown using [PyMuPDF](https://pymupdf.readthedocs.io/) via the lightweight helper [pymupdf4llm](https://github.com/pymupdf/pymupdf4llm). Supports optional image extraction.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Single file
python pdf2md.py path/to/file.pdf

# Folder of PDFs -> ./out
python pdf2md.py path/to/folder

# With images extracted to ./out/images
python pdf2md.py path/to/file.pdf --extract-images
