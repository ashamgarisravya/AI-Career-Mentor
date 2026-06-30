"""Resume analyzer page."""

from __future__ import annotations

import sqlite3

import streamlit as st

from utils.ai import ai_status_message
from utils.ats import analyze_resume_text
from utils.database import (
    initialize_database,
    load_latest_resume_analysis,
    load_profile,
    save_resume_analysis,
    split_list,
)
from utils.pdf_parser import extract_pdf_text
from utils.production import get_logger, validate_pdf_upload, validate_required
from utils.ui import badge, bullet_list, empty_state, inject_styles, page_header, panel, status_kind

st.set_page_config(page_title="Resume Analyzer | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()
profile = load_profile()
logger = get_logger(__name__)

page_header(
    "Resume Analyzer",
    "Upload a resume or paste text to generate ATS score, strengths, gaps, and next actions.",
    [("PDF upload", "info"), ("ATS scoring", "success"), ("Private analysis", "warning")],
)
st.caption(ai_status_message())

input_col, target_col = st.columns([1.4, 1])
with input_col, st.container(border=True):
    panel("Resume input", "Upload a PDF or paste resume text directly.")
    uploaded = st.file_uploader("Upload resume PDF", type=["pdf"])
    resume_text = st.text_area("Or paste resume text", height=220)
with target_col:
    with st.container(border=True):
        panel("Target role", "The ATS score is calibrated to this role.")
        target = (
            st.text_input(
                "Target Career", value=profile.target_career if profile else "AI Engineer"
            ).strip()
            or "AI Engineer"
        )

if uploaded:
    upload_errors = validate_pdf_upload(uploaded)
    if upload_errors:
        st.error("Uploaded file is not ready for analysis.")
        bullet_list(upload_errors)
    else:
        with st.spinner("Extracting resume text..."):
            extracted = extract_pdf_text(uploaded.getvalue())
        if extracted:
            st.success("PDF text extracted successfully.")
            with st.expander("Preview extracted text"):
                st.write(extracted[:3000])
        else:
            st.warning(
                "Could not extract text from this PDF. Paste the resume text manually below."
            )
        resume_text = extracted or resume_text

if st.button("Analyze Resume", use_container_width=True):
    errors = validate_required({"Resume text": resume_text, "Target career": target})
    if uploaded:
        errors.extend(validate_pdf_upload(uploaded))
    if errors:
        st.error("Resume analysis needs a few fixes.")
        bullet_list(errors)
    else:
        with st.spinner("Analyzing resume and saving ATS history..."):
            try:
                analysis = analyze_resume_text(
                    resume_text, target, split_list(profile.skills) if profile else []
                )
                save_resume_analysis(
                    filename=uploaded.name if uploaded else "pasted-resume.txt",
                    resume_text=resume_text,
                    target_career=target,
                    **analysis,
                )
            except (sqlite3.Error, ValueError) as exc:
                logger.exception("Resume analysis failed: %s", exc)
                st.error("Resume analysis could not be completed. Please try again.")
            else:
                st.success("Resume analysis saved.")
                st.rerun()

latest = load_latest_resume_analysis()
if latest:
    st.subheader("Latest analysis")
    c1, c2, c3 = st.columns(3)
    c1.metric("ATS Score", f"{latest['ats_score']}%")
    c2.metric("Missing Skills", len(latest["missing_skills"]))
    c3.metric("Missing Keywords", len(latest["missing_keywords"]))
    st.markdown(
        " ".join(
            [
                badge(f"ATS {latest['ats_score']}%", status_kind(int(latest["ats_score"]))),
                badge(f"{len(latest['strengths'])} strengths", "success"),
                badge(f"{len(latest['suggestions'])} suggestions", "info"),
            ]
        ),
        unsafe_allow_html=True,
    )
    st.progress(int(latest["ats_score"]) / 100)
    summary_tab, gaps_tab, actions_tab = st.tabs(["Summary", "Gaps", "Actions"])
    with summary_tab:
        with st.container(border=True):
            panel("Resume Summary")
            st.write(latest["summary"])
        left, right = st.columns(2)
        with left, st.expander("Strengths", expanded=True):
            bullet_list(latest["strengths"])
        with right, st.expander("Weaknesses", expanded=True):
            bullet_list(latest["weaknesses"])
    with gaps_tab:
        left, right = st.columns(2)
        with left, st.container(border=True):
            panel("Missing Skills")
            bullet_list(latest["missing_skills"] or ["No major skill gaps detected."])
        with right, st.container(border=True):
            panel("Missing Keywords")
            bullet_list(latest["missing_keywords"] or ["No major keyword gaps detected."])
    with actions_tab, st.container(border=True):
        panel("Actionable suggestions")
        bullet_list(latest["suggestions"])
else:
    empty_state(
        "No resume analysis yet",
        "Upload a PDF or paste resume text to create the first ATS report.",
    )
