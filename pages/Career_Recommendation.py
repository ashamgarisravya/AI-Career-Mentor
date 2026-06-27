"""Career recommendation page."""

from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

from utils.database import (
    add_activity,
    initialize_database,
    load_latest_resume_analysis,
    load_profile,
    save_career_recommendations,
    split_list,
)
from utils.knowledge import recommend_careers
from utils.production import get_logger
from utils.ui import badge, bullet_list, inject_styles, page_header, panel, status_kind

st.set_page_config(page_title="Career Recommendation | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()
profile = load_profile()
resume = load_latest_resume_analysis()
logger = get_logger(__name__)

page_header(
    "Career Recommendation",
    "Compare profile and resume signals against high-fit career paths with salary, growth, and learning resources.",
    [("Profile aware", "info"), ("Resume aware", "success" if resume else "warning")],
)

with st.form("career_form"):
    panel(
        "Recommendation inputs",
        "Tune skills, interests, education, and target industry without changing saved profile data.",
    )
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
with st.spinner("Preparing career recommendations..."):
    recommendations = recommend_careers(
        skills,
        interests,
        education,
        industry,
        resume_text=resume["resume_text"] if resume else "",
        resume_missing_skills=resume["missing_skills"] if resume else [],
    )

if submitted:
    with st.spinner("Saving recommendation run..."):
        try:
            save_career_recommendations(
                skills=skills,
                interests=interests,
                education=education,
                target_industry=industry,
                recommendations=recommendations,
            )
            add_activity(
                "Career recommendations generated", f"Top role: {recommendations[0]['title']}"
            )
        except sqlite3.Error as exc:
            logger.exception("Career recommendation save failed: %s", exc)
            st.error("Recommendations were generated but could not be saved to history.")
        else:
            st.success("Career recommendations saved.")

top = recommendations[0]
c1, c2, c3 = st.columns(3)
c1.metric("Top Match", str(top["title"]))
c2.metric("Match Score", f"{top['match']}%")
c3.metric("Tracked Roles", len(recommendations))
st.markdown(
    " ".join(
        [
            badge(f"{top['match']}% match", status_kind(int(top["match"]))),
            badge(str(top["industry"]), "info"),
            badge(str(top["growth"]).split()[0] + " growth", "success"),
        ]
    ),
    unsafe_allow_html=True,
)

table_tab, detail_tab = st.tabs(["Compare Roles", "Role Details"])
with table_tab, st.container(border=True):
    panel("Top career matches")
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

with detail_tab:
    for item in recommendations[:3]:
        with st.expander(
            f"{item['title']} - {item['match']}% match", expanded=item is recommendations[0]
        ):
            left, right = st.columns([1.2, 1])
            with left:
                st.write(f"**Expected Salary:** {item['salary_range']}")
                st.write(f"**Growth:** {item['growth']}")
                st.write(f"**Why Recommended:** {item['why']}")
                st.progress(int(item["match"]) / 100)
            with right:
                st.write("**Required Skills**")
                bullet_list(item["required_skills"])
                if item["missing_skills"]:
                    st.write("**Skills to Build**")
                    bullet_list(item["missing_skills"])
            st.write("**Learning Resources**")
            bullet_list(item["resources"])
