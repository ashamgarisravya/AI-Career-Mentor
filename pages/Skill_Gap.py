"""Skill gap analysis page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.database import initialize_database, load_latest_resume_analysis, load_profile, split_list
from utils.knowledge import analyze_skill_gap, extract_skills_from_text, find_career, merge_skills


st.set_page_config(page_title="Skill Gap Analysis | AI Career Mentor", layout="wide")
initialize_database()
profile = load_profile()
resume = load_latest_resume_analysis()

st.title("Skill Gap Analysis")

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
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    for row in rows:
        with st.container(border=True):
            st.subheader(row["Missing Skill"])
            st.write(f"Priority: {row['Priority']}")
            st.write(f"Difficulty: {row['Difficulty']}")
            st.write(f"Estimated Learning Time: {row['Estimated Learning Time']}")
            st.write(f"Recommended Learning Path: {row['Recommended Learning Path']}")
