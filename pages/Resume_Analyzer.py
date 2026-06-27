"""Resume analyzer page."""

from __future__ import annotations

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


st.set_page_config(page_title="Resume Analyzer | AI Career Mentor", layout="wide")
initialize_database()
profile = load_profile()

st.title("Resume Analyzer")
st.caption(ai_status_message())

uploaded = st.file_uploader("Upload resume PDF", type=["pdf"])
resume_text = st.text_area("Or paste resume text", height=220)
target = st.text_input("Target Career", value=profile.target_career if profile else "AI Engineer")

if uploaded:
    extracted = extract_pdf_text(uploaded.getvalue())
    if extracted:
        st.success("PDF text extracted successfully.")
        with st.expander("Preview extracted text"):
            st.write(extracted[:3000])
    else:
        st.warning("Could not extract text from this PDF. Paste the resume text manually below.")
    resume_text = extracted or resume_text

if st.button("Analyze Resume", use_container_width=True):
    if not resume_text.strip():
        st.warning("Upload a readable PDF or paste resume text before analyzing.")
    else:
        analysis = analyze_resume_text(resume_text, target, split_list(profile.skills) if profile else [])
        save_resume_analysis(
            filename=uploaded.name if uploaded else "pasted-resume.txt",
            resume_text=resume_text,
            **analysis,
        )
        st.success("Resume analysis saved.")
        st.rerun()

latest = load_latest_resume_analysis()
if latest:
    st.subheader("Latest analysis")
    c1, c2, c3 = st.columns(3)
    c1.metric("ATS Score", f"{latest['ats_score']}%")
    c2.metric("Missing Skills", len(latest["missing_skills"]))
    c3.metric("Missing Keywords", len(latest["missing_keywords"]))
    st.progress(int(latest["ats_score"]) / 100)
    sections = [
        ("Strengths", latest["strengths"]),
        ("Weaknesses", latest["weaknesses"]),
        ("Missing Skills", latest["missing_skills"]),
        ("Missing Keywords", latest["missing_keywords"]),
        ("Suggested Improvements", latest["suggestions"]),
    ]
    for title, items in sections:
        with st.container(border=True):
            st.subheader(title)
            for item in items:
                st.write(f"- {item}")
    with st.container(border=True):
        st.subheader("Resume Summary")
        st.write(latest["summary"])
else:
    st.info("No resume analysis has been saved yet.")
