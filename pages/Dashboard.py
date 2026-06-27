"""Dashboard page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.ats import analyze_resume_text
from utils.charts import bar_progress, gauge
from utils.database import (
    initialize_database,
    load_latest_resume_analysis,
    load_profile,
    recent_activities,
    split_list,
)
from utils.knowledge import missing_skills_for_target


st.set_page_config(page_title="Dashboard | AI Career Mentor", layout="wide")
initialize_database()

profile = load_profile()
latest_resume = load_latest_resume_analysis()

st.title("Dashboard")

if profile is None:
    st.info("Create your profile to unlock personalized career metrics.")
    st.page_link("pages/Profile.py", label="Create Profile")
    st.stop()

skills = split_list(profile.skills)
interests = split_list(profile.interests)
target = profile.target_career or "AI Engineer"
missing_skills = missing_skills_for_target(skills, target)
resume_score = int(latest_resume["ats_score"]) if latest_resume else analyze_resume_text("", target, skills)["ats_score"]
career_match = min(98, 35 + len(skills) * 10 + (15 if target else 0) + len(interests) * 4)
skill_gap = max(0, min(100, int((len(missing_skills) / max(len(skills) + len(missing_skills), 1)) * 100)))
roadmap_progress = min(100, 20 + len(skills) * 8 + (15 if latest_resume else 0))
interview_readiness = min(100, (career_match + resume_score + (100 - skill_gap)) // 3)

st.subheader(f"Welcome back, {profile.name}")
st.caption(f"Target career: {target}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("ATS Score", f"{resume_score}%")
m2.metric("Career Match", f"{career_match}%")
m3.metric("Skill Gap", f"{skill_gap}%")
m4.metric("Interview Readiness", f"{interview_readiness}%")

s1, s2 = st.columns([2, 1])
with s1:
    with st.container(border=True):
        st.subheader("User profile summary")
        c1, c2 = st.columns(2)
        c1.write(f"**College:** {profile.college or 'Not set'}")
        c1.write(f"**Degree:** {profile.degree or 'Not set'}")
        c1.write(f"**Branch:** {profile.branch or 'Not set'}")
        c2.write(f"**Graduation Year:** {profile.graduation_year or 'Not set'}")
        c2.write(f"**Experience:** {profile.experience_level or 'Not set'}")
        c2.write(f"**Resume Uploaded:** {'Yes' if latest_resume else 'No'}")
        st.write("**Skills:** " + (", ".join(skills) if skills else "No skills saved"))
        st.write("**Interests:** " + (", ".join(interests) if interests else "No interests saved"))
with s2:
    with st.container(border=True):
        st.subheader("Quick actions")
        st.markdown("- [Edit Profile](./Profile)")
        st.markdown("- [Analyze Resume](./Resume_Analyzer)")
        st.markdown("- [Find Careers](./Career_Recommendation)")
        st.markdown("- [Build Roadmap](./Learning_Roadmap)")

left_chart, right_chart = st.columns(2)
with left_chart:
    st.plotly_chart(gauge("Career Match", career_match, "#2563eb"), use_container_width=True)
with right_chart:
    st.plotly_chart(
        bar_progress(
            ["ATS", "Career Match", "Skill Readiness", "Roadmap", "Interview"],
            [resume_score, career_match, 100 - skill_gap, roadmap_progress, interview_readiness],
        ),
        use_container_width=True,
    )

r1, r2 = st.columns(2)
with r1:
    with st.container(border=True):
        st.subheader("Learning roadmap progress")
        st.progress(roadmap_progress / 100)
        st.write(f"{roadmap_progress}% complete based on profile readiness and resume activity.")
with r2:
    with st.container(border=True):
        st.subheader("Recent activity")
        activities = recent_activities()
        if not activities:
            st.write("No activity yet. Save a profile or analyze a resume to begin.")
        else:
            st.dataframe(pd.DataFrame(activities), use_container_width=True, hide_index=True)
