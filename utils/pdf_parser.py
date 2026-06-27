"""PDF parsing helpers."""

from __future__ import annotations

from io import BytesIO

from PyPDF2.errors import PdfReadError

from utils.production import get_logger


logger = get_logger(__name__)


def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from a PDF, returning an empty string if parsing fails."""
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except (PdfReadError, ValueError, OSError) as exc:
        logger.warning("PDF text extraction failed: %s", exc)
        return ""
