"""Professional resume PDF generation."""

from __future__ import annotations

from io import BytesIO


def build_resume_pdf(data: dict[str, str]) -> bytes:
    """Generate a simple professional resume PDF and return bytes."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(data.get("name", "Your Name"), styles["Title"]),
        Paragraph(data.get("email", ""), styles["Normal"]),
        Spacer(1, 12),
    ]
    sections = [
        ("Career Objective", data.get("summary", "")),
        ("Education", data.get("education", "")),
        ("Skills", data.get("skills", "")),
        ("Projects", data.get("projects", "")),
        ("Experience", data.get("experience", "")),
        ("Certifications", data.get("certifications", "")),
    ]
    for title, body in sections:
        if body.strip():
            story.append(Paragraph(title, styles["Heading2"]))
            story.append(Paragraph(body.replace("\n", "<br/>"), styles["BodyText"]))
            story.append(Spacer(1, 10))
    document.build(story)
    return buffer.getvalue()
