"""Production hardening helpers for logging and validation."""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

LOG_PATH = Path(os.getenv("LOG_PATH", "logs/app.log"))
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_PDF_BYTES = int(os.getenv("MAX_PDF_UPLOAD_MB", "8")) * 1024 * 1024


def get_logger(name: str) -> logging.Logger:
    """Return an application logger configured once."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    return logger


def validate_email(value: str, *, required: bool = False) -> str | None:
    """Validate an email address and return an error message when invalid."""
    cleaned = value.strip()
    if required and not cleaned:
        return "Email is required."
    if cleaned and not EMAIL_RE.match(cleaned):
        return "Enter a valid email address."
    return None


def validate_required(values: dict[str, str]) -> list[str]:
    """Validate required text fields."""
    return [f"{label} is required." for label, value in values.items() if not value.strip()]


def validate_pdf_upload(uploaded_file: Any) -> list[str]:
    """Validate an uploaded Streamlit PDF file before parsing."""
    if uploaded_file is None:
        return []
    errors = []
    name = str(getattr(uploaded_file, "name", "") or "")
    if not name.lower().endswith(".pdf"):
        errors.append("Upload a PDF file with a .pdf extension.")
    size = int(getattr(uploaded_file, "size", 0) or 0)
    if size <= 0:
        errors.append("Uploaded PDF is empty.")
    if size > MAX_PDF_BYTES:
        errors.append("Uploaded PDF must be 8 MB or smaller.")
    return errors


def safe_int(value: Any, default: int = 0) -> int:
    """Convert a value to int without raising."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
