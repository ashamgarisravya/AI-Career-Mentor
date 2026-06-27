"""Resume builder page."""

from __future__ import annotations

import sqlite3

import streamlit as st

from utils.database import add_activity, initialize_database, load_profile
from utils.production import get_logger
from utils.resume_builder import build_resume_pdf, completion_score, normalize_resume_data, validate_resume_data
from utils.ui import badge, bullet_list, inject_styles, page_header, panel, status_kind


st.set_page_config(page_title="Resume Builder | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()
profile = load_profile()
logger = get_logger(__name__)

page_header(
    "Resume Builder",
    "Create a professional resume PDF with validated personal details, education, skills, experience, projects, and certifications.",
    [("PDF export", "success"), ("Live preview", "info"), ("Validated input", "warning")],
)

default_education = f"{profile.degree}, {profile.college}".strip(", ") if profile else ""
default_links = ""

with st.form("resume_builder"):
    panel("Resume content", "Complete the required fields and preview the document before downloading.")
    details_tab, content_tab, proof_tab = st.tabs(["Personal Details", "Core Resume", "Proof"])
    with details_tab:
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name", value=profile.name if profile else "")
            email = st.text_input("Email", value=profile.email if profile else "")
            phone = st.text_input("Phone")
        with c2:
            location = st.text_input("Location")
            links = st.text_area("Portfolio / LinkedIn / GitHub", value=default_links, height=100)
            summary = st.text_area("Professional Summary", height=110)
    with content_tab:
        c1, c2 = st.columns(2)
        with c1:
            education = st.text_area("Education", value=default_education, height=140)
            skills = st.text_area("Skills", value=profile.skills if profile else "", help="Comma-separated values", height=140)
        with c2:
            experience = st.text_area("Experience", height=140)
            projects = st.text_area("Projects", height=140)
    with proof_tab:
        certifications = st.text_area("Certifications", height=130)
        st.caption("Use one line per certification, project bullet, or experience bullet for the cleanest PDF formatting.")
    submitted = st.form_submit_button("Generate Resume PDF", use_container_width=True)

resume_data = normalize_resume_data(
    {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "links": links,
        "summary": summary,
        "education": education,
        "skills": skills,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    }
)
errors = validate_resume_data(resume_data)
score = completion_score(resume_data)

c1, c2, c3 = st.columns(3)
c1.metric("Completeness", f"{score}%")
c2.metric("Required Fields", "Ready" if not errors else f"{len(errors)} issue(s)")
c3.metric("Format", "PDF")
st.markdown(badge(f"{score}% complete", status_kind(score)), unsafe_allow_html=True)
st.progress(score / 100)

preview_tab, validation_tab, export_tab = st.tabs(["Preview", "Validation", "Export"])

with preview_tab:
    with st.container(border=True):
        panel("Resume preview", "This preview mirrors the content that will be sent to the PDF generator.")
        st.subheader(resume_data["name"] or "Your Name")
        contact_parts = [resume_data["email"], resume_data["phone"], resume_data["location"], resume_data["links"]]
        st.caption(" | ".join(part for part in contact_parts if part) or "Contact details will appear here")
        sections = [
            ("Professional Summary", resume_data["summary"]),
            ("Education", resume_data["education"]),
            ("Skills", resume_data["skills"]),
            ("Experience", resume_data["experience"]),
            ("Projects", resume_data["projects"]),
            ("Certifications", resume_data["certifications"]),
        ]
        for title, body in sections:
            with st.expander(title, expanded=bool(body)):
                if body:
                    if title == "Skills":
                        bullet_list([item.strip() for item in body.replace("\n", ",").split(",") if item.strip()])
                    else:
                        bullet_list([line.strip(" -") for line in body.splitlines() if line.strip()])
                else:
                    st.write("Not provided yet.")

with validation_tab:
    with st.container(border=True):
        panel("Validation results")
        if errors:
            st.error("Fix the issues below before generating a PDF.")
            bullet_list(errors)
        else:
            st.success("All required resume inputs are valid.")

with export_tab:
    if submitted:
        if errors:
            st.error("PDF was not generated because validation failed.")
        else:
            with st.spinner("Generating professional PDF..."):
                try:
                    pdf_bytes = build_resume_pdf(resume_data)
                except ValueError as exc:
                    st.error(str(exc))
                except (OSError, RuntimeError) as exc:
                    logger.exception("Resume PDF generation failed: %s", exc)
                    st.error("Resume PDF could not be generated. Please review the content and try again.")
                else:
                    try:
                        add_activity("Resume PDF generated", f"Generated resume for {resume_data['name'] or 'learner'}")
                    except sqlite3.Error as exc:
                        logger.exception("Resume PDF activity save failed: %s", exc)
                        st.warning("PDF is ready, but activity history could not be updated.")
                    st.success("Resume PDF generated.")
                    st.markdown(badge("Download ready", "success"), unsafe_allow_html=True)
                    st.download_button(
                        "Download Resume PDF",
                        data=pdf_bytes,
                        file_name="ai_career_mentor_resume.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
    else:
        with st.container(border=True):
            panel("Export status")
            st.info("Review the preview and validation results, then generate the PDF.")
