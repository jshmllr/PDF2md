# pdf2md

Convert PDFs to clean Markdown using [PyMuPDF](https://pymupdf.readthedocs.io/) via the lightweight helper [pymupdf4llm](https://github.com/pymupdf/pymupdf4llm). Supports optional image extraction.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Single file
`python pdf2md.py path/to/file.pdf`

### Folder of PDFs -> ./out
`python pdf2md.py path/to/folder`

### With images extracted to ./out/images
`python pdf2md.py path/to/file.pdf --extract-images`

### Make it Globally Runnable
If you want to run it from anywhere on your system, make it executable and move it into your 

PATH:
```bash
chmod +x pdf2md.py
mv pdf2md.py /usr/local/bin/pdf2md
```

Now you can just type:
```bash
pdf2md path/to/file.pdf
```
or
```bash
pdf2md path/to/folder --extract-images
```
and your Markdown files will appear in `./out/`.

## Notes

Works best on digitally generated PDFs (not scanned images).
For scanned documents, run OCR first with ocrmypdf 

```bash
pip install ocrmypdf
ocrmypdf input.pdf input_ocr.pdf
pdf2md input_ocr.pdf
```

