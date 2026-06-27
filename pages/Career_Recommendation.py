"""Career recommendation page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.database import (
    add_activity,
    initialize_database,
    load_latest_resume_analysis,
    load_profile,
    split_list,
)
from utils.knowledge import recommend_careers


st.set_page_config(page_title="Career Recommendation | AI Career Mentor", layout="wide")
initialize_database()
profile = load_profile()
resume = load_latest_resume_analysis()

st.title("Career Recommendation")

with st.form("career_form"):
    c1, c2 = st.columns(2)
    with c1:
        skills_text = st.text_area("Skills", value=profile.skills if profile else "")
        education = st.text_input("Education", value=profile.degree if profile else "")
    with c2:
        interests_text = st.text_area("Interests", value=profile.interests if profile else "")
        industry = st.text_input("Target Industry", value="")
    submitted = st.form_submit_button("Recommend Careers", use_container_width=True)

skills = split_list(skills_text)
interests = split_list(interests_text)
recommendations = recommend_careers(
    skills,
    interests,
    education,
    industry,
    resume_text=resume["resume_text"] if resume else "",
    resume_missing_skills=resume["missing_skills"] if resume else [],
)

if submitted:
    add_activity("Career recommendations generated", f"Top role: {recommendations[0]['title']}")

st.subheader("Top career matches")
st.dataframe(
    pd.DataFrame(
        [
            {
                "Career": item["title"],
                "Match": f"{item['match']}%",
                "Salary": item["salary_range"],
                "Growth": item["growth"],
                "Industry": item["industry"],
            }
            for item in recommendations
        ]
    ),
    use_container_width=True,
    hide_index=True,
)

for item in recommendations[:3]:
    with st.container(border=True):
        st.subheader(f"{item['title']} - {item['match']}% match")
        st.write(f"**Expected Salary:** {item['salary_range']}")
        st.write(f"**Growth:** {item['growth']}")
        st.write(f"**Required Skills:** {', '.join(item['required_skills'])}")
        if item["missing_skills"]:
            st.write(f"**Skills to Build:** {', '.join(item['missing_skills'])}")
        st.write(f"**Why Recommended:** {item['why']}")
        st.write("**Learning Resources:**")
        for resource in item["resources"]:
            st.write(f"- {resource}")
