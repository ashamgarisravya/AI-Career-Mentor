"""Skill gap analysis page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.database import initialize_database, load_latest_resume_analysis, load_profile, split_list
from utils.knowledge import analyze_skill_gap, extract_skills_from_text, find_career, merge_skills
from utils.ui import badge, bullet_list, inject_styles, page_header, panel


st.set_page_config(page_title="Skill Gap Analysis | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()
profile = load_profile()
resume = load_latest_resume_analysis()

page_header(
    "Skill Gap Analysis",
    "Compare profile and resume evidence against the selected career and prioritize what to learn next.",
    [("Resume compared", "success" if resume else "warning"), ("Prioritized gaps", "info")],
)

target = st.text_input("Target Career", value=profile.target_career if profile else "AI Engineer")
profile_skills = split_list(profile.skills) if profile else []
resume_skills = extract_skills_from_text(resume["resume_text"]) if resume else []
current_skills = st.text_area("Current Skills", value=", ".join(merge_skills(profile_skills, resume_skills)))
skills = split_list(current_skills)

career = find_career(target)
rows = analyze_skill_gap(skills, career.title, resume["resume_text"] if resume else "")

if not rows:
    st.success("No major skill gap detected for the selected target career.")
else:
    high_priority = sum(1 for row in rows if row["Priority"] == "High")
    c1, c2, c3 = st.columns(3)
    c1.metric("Missing Skills", len(rows))
    c2.metric("High Priority", high_priority)
    c3.metric("Detected Skills", len(skills))
    st.markdown(
        " ".join([badge(f"{career.title}", "info"), badge(f"{high_priority} high priority", "warning")]),
        unsafe_allow_html=True,
    )
    overview_tab, path_tab = st.tabs(["Gap Matrix", "Learning Paths"])
    with overview_tab:
        with st.container(border=True):
            panel("Skill gap matrix")
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    with path_tab:
        for row in rows:
            with st.expander(f"{row['Missing Skill']} - {row['Priority']} priority", expanded=row["Priority"] == "High"):
                left, right = st.columns([1, 2])
                with left:
                    st.metric("Priority", row["Priority"])
                    st.metric("Learning Time", row["Estimated Learning Time"])
                with right:
                    st.write(f"**Difficulty:** {row['Difficulty']}")
                    bullet_list([row["Recommended Learning Path"]])
