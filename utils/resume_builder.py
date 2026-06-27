"""Professional resume PDF generation and validation."""

from __future__ import annotations

import re
from io import BytesIO
from typing import Any

REQUIRED_FIELDS = ("name", "email", "education", "skills")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_resume_data(data: dict[str, str]) -> dict[str, str]:
    """Trim resume builder input values."""
    return {key: str(value or "").strip() for key, value in data.items()}


def validate_resume_data(data: dict[str, str]) -> list[str]:
    """Return validation errors for required resume fields."""
    cleaned = normalize_resume_data(data)
    errors = []
    for field in REQUIRED_FIELDS:
        if not cleaned.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required.")
    if cleaned.get("email") and not EMAIL_RE.match(cleaned["email"]):
        errors.append("Enter a valid email address.")
    if cleaned.get("skills") and len(_split_items(cleaned["skills"])) < 3:
        errors.append("Add at least three skills.")
    if cleaned.get("projects") and len(cleaned["projects"].split()) < 8:
        errors.append("Add more detail to projects, including tools and outcomes.")
    return errors


def completion_score(data: dict[str, str]) -> int:
    """Estimate resume completeness as a percentage."""
    cleaned = normalize_resume_data(data)
    weighted_fields = {
        "name": 10,
        "email": 10,
        "phone": 5,
        "location": 5,
        "summary": 10,
        "education": 15,
        "skills": 15,
        "experience": 15,
        "projects": 10,
        "certifications": 5,
    }
    score = sum(weight for field, weight in weighted_fields.items() if cleaned.get(field))
    return max(0, min(100, score))


def build_resume_pdf(data: dict[str, str]) -> bytes:
    """Generate a professional resume PDF and return bytes."""
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

    cleaned = normalize_resume_data(data)
    errors = validate_resume_data(cleaned)
    if errors:
        raise ValueError(" ".join(errors))

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.58 * inch,
        leftMargin=0.58 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.5 * inch,
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ResumeName",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#101828"),
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Contact",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#475467"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#1d4ed8"),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ResumeBody",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#101828"),
            spaceAfter=4,
        )
    )

    story: list[Any] = [
        Paragraph(_xml(cleaned["name"]), styles["ResumeName"]),
        Paragraph(_contact_line(cleaned), styles["Contact"]),
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#d0d5dd")),
        Spacer(1, 6),
    ]

    _add_section(story, "Professional Summary", cleaned.get("summary"), styles)
    _add_section(story, "Education", cleaned.get("education"), styles)
    _add_skills(story, cleaned.get("skills", ""), styles)
    _add_section(story, "Experience", cleaned.get("experience"), styles)
    _add_section(story, "Projects", cleaned.get("projects"), styles)
    _add_section(story, "Certifications", cleaned.get("certifications"), styles)

    if cleaned.get("links"):
        _add_section(story, "Links", cleaned.get("links"), styles)

    document.build(story)
    return buffer.getvalue()


def _add_section(story: list[Any], title: str, body: str | None, styles: Any) -> None:
    if not body:
        return
    from reportlab.platypus import Paragraph

    story.append(Paragraph(title.upper(), styles["SectionTitle"]))
    for line in _split_lines(body):
        story.append(Paragraph(_xml(_bulletize(line)), styles["ResumeBody"]))


def _add_skills(story: list[Any], skills: str, styles: Any) -> None:
    if not skills:
        return
    from reportlab.lib import colors
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

    items = _split_items(skills)
    rows = []
    for index in range(0, len(items), 3):
        rows.append(
            [Paragraph(_xml(item), styles["ResumeBody"]) for item in items[index : index + 3]]
        )
    story.append(Paragraph("SKILLS", styles["SectionTitle"]))
    table = Table(rows, hAlign="LEFT", colWidths=[170, 170, 170])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("BOX", (0, 0), (-1, -1), 0.35, colors.HexColor("#d0d5dd")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#e4e7ec")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 5))


def _split_lines(value: str) -> list[str]:
    return [line.strip(" -\t") for line in value.splitlines() if line.strip()]


def _split_items(value: str) -> list[str]:
    normalized = value.replace("\n", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def _bulletize(line: str) -> str:
    return line if line.startswith("•") else f"• {line}"


def _contact_line(data: dict[str, str]) -> str:
    parts = [
        data.get("email", ""),
        data.get("phone", ""),
        data.get("location", ""),
        data.get("links", ""),
    ]
    return " | ".join(_xml(part) for part in parts if part)


def _xml(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
