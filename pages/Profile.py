"""Profile page."""

from __future__ import annotations

import streamlit as st

from utils.database import initialize_database, load_profile, save_profile, split_list
from utils.ui import badge, inject_styles, page_header, panel


st.set_page_config(page_title="Profile | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()
profile = load_profile()

page_header(
    "Profile",
    "Keep learner context current so recommendations, resume scoring, and roadmaps stay personalized.",
    [("Personalization", "info"), ("Local data", "success")],
)

form_tab, saved_tab = st.tabs(["Profile Form", "Saved Snapshot"])

with form_tab:
    with st.container(border=True):
        panel("Learner profile", "Core academic, skill, and career details used across the product.")
    with st.form("profile_form", clear_on_submit=False):
        left, right = st.columns(2)
        with left:
            name = st.text_input("Name", value=profile.name if profile else "")
            email = st.text_input("Email", value=profile.email if profile else "")
            college = st.text_input("College", value=profile.college if profile else "")
            degree = st.text_input("Degree", value=profile.degree if profile else "")
            branch = st.text_input("Branch", value=profile.branch if profile else "")
        with right:
            graduation_year = st.text_input("Graduation Year", value=profile.graduation_year if profile else "")
            experience_level = st.selectbox(
                "Experience Level",
                ["Beginner", "Intermediate", "Advanced", "Working Professional"],
                index=["Beginner", "Intermediate", "Advanced", "Working Professional"].index(profile.experience_level)
                if profile and profile.experience_level in ["Beginner", "Intermediate", "Advanced", "Working Professional"]
                else 0,
            )
            target_career = st.text_input("Target Career", value=profile.target_career if profile else "")
            skills = st.text_area("Skills", value=profile.skills if profile else "", help="Comma-separated values")
            interests = st.text_area("Interests", value=profile.interests if profile else "", help="Comma-separated values")

        submitted = st.form_submit_button("Save Profile", use_container_width=True)
        if submitted:
            if not name.strip():
                st.error("Please enter your name before saving.")
            else:
                save_profile(
                    name=name,
                    email=email,
                    college=college,
                    degree=degree,
                    branch=branch,
                    graduation_year=graduation_year,
                    skills=skills,
                    interests=interests,
                    target_career=target_career,
                    experience_level=experience_level,
                )
                st.success("Profile saved successfully.")
                st.rerun()

with saved_tab:
    if profile:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Name", profile.name or "Not set")
        c2.metric("Target Career", profile.target_career or "Not set")
        c3.metric("Skills", len(split_list(profile.skills)))
        c4.metric("Experience", profile.experience_level or "Not set")
        st.markdown(
            " ".join(
                [
                    badge(profile.experience_level or "Experience not set", "info"),
                    badge(f"{len(split_list(profile.interests))} interests", "success"),
                    badge(f"Updated {profile.updated_at}", "warning"),
                ]
            ),
            unsafe_allow_html=True,
        )
        left, right = st.columns([1.2, 1])
        with left:
            with st.container(border=True):
                panel("Academic profile")
                st.write(f"**Email:** {profile.email or 'Not set'}")
                st.write(f"**College:** {profile.college or 'Not set'}")
                st.write(f"**Degree / Branch:** {profile.degree or 'Not set'} / {profile.branch or 'Not set'}")
                st.write(f"**Graduation Year:** {profile.graduation_year or 'Not set'}")
        with right:
            with st.container(border=True):
                panel("Career signals")
                st.write(f"**Skills:** {profile.skills or 'Not set'}")
                st.write(f"**Interests:** {profile.interests or 'Not set'}")
    else:
        st.info("No saved profile yet. Complete the form to personalize the application.")
