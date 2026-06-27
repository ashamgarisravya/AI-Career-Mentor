"""Resume builder page."""

from __future__ import annotations

import streamlit as st

from utils.database import add_activity, initialize_database, load_profile
from utils.resume_builder import build_resume_pdf
from utils.ui import badge, inject_styles, page_header, panel


st.set_page_config(page_title="Resume Builder | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()
profile = load_profile()

page_header(
    "Resume Builder",
    "Create a clean professional resume PDF from profile, education, project, and experience details.",
    [("PDF export", "success"), ("Profile assisted", "info")],
)

with st.form("resume_builder"):
    panel("Resume content", "Fill each section once, then generate a downloadable PDF.")
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name", value=profile.name if profile else "")
        email = st.text_input("Email", value=profile.email if profile else "")
        education = st.text_area("Education", value=f"{profile.degree}, {profile.college}" if profile else "")
        skills = st.text_area("Skills", value=profile.skills if profile else "")
    with c2:
        summary = st.text_area("Career Objective")
        projects = st.text_area("Projects")
        experience = st.text_area("Experience")
        certifications = st.text_area("Certifications")
    submitted = st.form_submit_button("Generate Resume PDF", use_container_width=True)

if submitted:
    pdf_bytes = build_resume_pdf(
        {
            "name": name,
            "email": email,
            "education": education,
            "skills": skills,
            "summary": summary,
            "projects": projects,
            "experience": experience,
            "certifications": certifications,
        }
    )
    add_activity("Resume PDF generated", f"Generated resume for {name or 'learner'}")
    st.success("Resume PDF generated.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Sections", 7)
    c2.metric("Format", "PDF")
    c3.metric("Status", "Ready")
    st.markdown(badge("Download ready", "success"), unsafe_allow_html=True)
    with st.container(border=True):
        panel("Export")
        st.download_button(
            "Download Resume PDF",
            data=pdf_bytes,
            file_name="ai_career_mentor_resume.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
else:
    with st.container(border=True):
        panel("Resume builder status")
        st.info("Fill the form and generate a downloadable professional PDF.")
