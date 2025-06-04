from pathlib import Path
from typing import Optional

from pdfminer.high_level import extract_text


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    return extract_text(str(pdf_path))


def store_pdf(project_path: Path, pdf_file: Path) -> Path:
    """Store a PDF inside the project and return its relative path."""
    dest_dir = project_path / "pdfs"
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / pdf_file.name
    with open(pdf_file, "rb") as src, open(dest, "wb") as dst:
        dst.write(src.read())
    return dest
