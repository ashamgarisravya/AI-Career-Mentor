"""PDF parsing helpers."""

from __future__ import annotations

from io import BytesIO


def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from a PDF, returning an empty string if parsing fails."""
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except Exception:
        return ""
