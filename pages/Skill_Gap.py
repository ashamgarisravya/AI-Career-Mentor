"""Skill gap analysis page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.database import initialize_database, load_latest_resume_analysis, load_profile, split_list
from utils.knowledge import find_career, missing_skills_for_target


st.set_page_config(page_title="Skill Gap Analysis | AI Career Mentor", layout="wide")
initialize_database()
profile = load_profile()
resume = load_latest_resume_analysis()

st.title("Skill Gap Analysis")

target = st.text_input("Target Career", value=profile.target_career if profile else "AI Engineer")
skills = split_list(profile.skills) if profile else []
if resume:
    skills.extend(resume["missing_skills"])
current_skills = st.text_area("Current Skills", value=", ".join(split_list(profile.skills) if profile else []))
skills = split_list(current_skills)

career = find_career(target)
missing = missing_skills_for_target(skills, career.title)

if not missing:
    st.success("No major skill gap detected for the selected target career.")
else:
    rows = []
    for index, skill in enumerate(missing):
        rows.append(
            {
                "Missing Skill": skill,
                "Priority": "High" if index < 2 else "Medium",
                "Difficulty": "Intermediate" if skill in {"Machine Learning", "Deep Learning", "Cloud"} else "Beginner",
                "Estimated Learning Time": "2-4 weeks" if index < 2 else "1-2 weeks",
                "Recommended Course": f"Focused {skill} course + one mini project",
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    for row in rows:
        with st.container(border=True):
            st.subheader(row["Missing Skill"])
            st.write(f"Priority: {row['Priority']}")
            st.write(f"Difficulty: {row['Difficulty']}")
            st.write(f"Estimated Learning Time: {row['Estimated Learning Time']}")
            st.write(f"Recommended Course: {row['Recommended Course']}")
