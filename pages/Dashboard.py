"""Dashboard page."""

from __future__ import annotations

import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.ats import analyze_resume_text
from utils.charts import bar_progress, gauge
from utils.database import (
    dashboard_analytics,
    initialize_database,
    load_latest_resume_analysis,
    load_profile,
    recent_activities,
    split_list,
)
from utils.knowledge import missing_skills_for_target
from utils.production import get_logger
from utils.ui import badge, inject_styles, page_header, panel, status_kind

st.set_page_config(page_title="Dashboard | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()
logger = get_logger(__name__)

profile = load_profile()
latest_resume = load_latest_resume_analysis()
try:
    analytics = dashboard_analytics()
except sqlite3.Error as exc:
    logger.exception("Dashboard analytics failed: %s", exc)
    analytics = {
        "counts": {
            "profiles": 0,
            "uploaded_resumes": 0,
            "ats_history": 0,
            "career_recommendations": 0,
            "roadmaps": 0,
            "interview_scores": 0,
        },
        "averages": {
            "avg_ats": 0,
            "avg_career_match": 0,
            "avg_learning_progress": 0,
            "avg_interview_score": 0,
        },
        "ats_history": [],
        "interview_scores": [],
        "career_recommendations": [],
    }

if profile is None:
    page_header(
        "Dashboard",
        "Your command center is ready once a learner profile is saved.",
        [("Setup required", "warning")],
    )
    st.info("Create your profile to unlock personalized career metrics.")
    st.page_link("pages/Profile.py", label="Create Profile")
    st.stop()

skills = split_list(profile.skills)
interests = split_list(profile.interests)
target = profile.target_career or "AI Engineer"
missing_skills = missing_skills_for_target(skills, target)
resume_score = (
    int(latest_resume["ats_score"])
    if latest_resume
    else analyze_resume_text("", target, skills)["ats_score"]
)
career_match = min(98, 35 + len(skills) * 10 + (15 if target else 0) + len(interests) * 4)
skill_gap = max(
    0, min(100, int((len(missing_skills) / max(len(skills) + len(missing_skills), 1)) * 100))
)
roadmap_progress = min(100, 20 + len(skills) * 8 + (15 if latest_resume else 0))
interview_readiness = min(100, (career_match + resume_score + (100 - skill_gap)) // 3)
if analytics["averages"]["avg_career_match"]:
    career_match = int(analytics["averages"]["avg_career_match"])
if analytics["averages"]["avg_learning_progress"]:
    roadmap_progress = int(analytics["averages"]["avg_learning_progress"])
if analytics["averages"]["avg_interview_score"]:
    interview_readiness = int(analytics["averages"]["avg_interview_score"])
resume_status = "Analyzed" if latest_resume else "Not analyzed"
resume_status_kind = "success" if latest_resume else "warning"

page_header(
    "Dashboard",
    f"Welcome back, {profile.name}. Track career fit, resume quality, learning progress, and interview readiness.",
    [(f"Target: {target}", "info"), (f"Resume: {resume_status}", resume_status_kind)],
)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("ATS Score", f"{resume_score}%")
m2.metric("Career Match", f"{career_match}%")
m3.metric("Resume Status", resume_status)
m4.metric("Learning Progress", f"{roadmap_progress}%")
m5.metric("Interview Readiness", f"{interview_readiness}%")

st.markdown(
    " ".join(
        [
            badge(f"ATS {resume_score}%", status_kind(resume_score)),
            badge(f"Career Match {career_match}%", status_kind(career_match)),
            badge(f"Skill Gap {skill_gap}%", "warning" if skill_gap else "success"),
            badge(f"Interview {interview_readiness}%", status_kind(interview_readiness)),
        ]
    ),
    unsafe_allow_html=True,
)

overview_tab, analytics_tab, profile_tab, activity_tab = st.tabs(
    ["Overview", "Analytics", "Profile", "Activity"]
)

with overview_tab:
    left_chart, right_chart = st.columns([1, 1.2])
    with left_chart:
        with st.container(border=True):
            panel(
                "Career Match Gauge",
                "A blended indicator based on target role, saved skills, interests, and resume signal.",
            )
            st.plotly_chart(
                gauge("Career Match", career_match, "#2563eb"), use_container_width=True
            )
    with right_chart:
        with st.container(border=True):
            panel("Readiness Breakdown", "A side-by-side view of the main SaaS operating metrics.")
            st.plotly_chart(
                bar_progress(
                    ["ATS", "Career Match", "Skill Readiness", "Learning", "Interview"],
                    [
                        resume_score,
                        career_match,
                        100 - skill_gap,
                        roadmap_progress,
                        interview_readiness,
                    ],
                ),
                use_container_width=True,
            )
    r1, r2 = st.columns(2)
    with r1, st.container(border=True):
        panel("Learning roadmap progress")
        st.progress(roadmap_progress / 100)
        st.write(f"{roadmap_progress}% complete based on profile readiness and resume activity.")
    with r2:
        with st.container(border=True):
            panel("Resume status")
            st.progress(resume_score / 100)
            st.write(
                "Latest resume analysis is available."
                if latest_resume
                else "Analyze a resume to unlock ATS insights."
            )

with analytics_tab:
    counts = analytics["counts"]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Uploaded Resumes", counts["uploaded_resumes"])
    c2.metric("ATS Runs", counts["ats_history"])
    c3.metric("Recommendations", counts["career_recommendations"])
    c4.metric("Roadmaps", counts["roadmaps"])
    c5.metric("Interview Scores", counts["interview_scores"])

    chart_left, chart_right = st.columns(2)
    with chart_left, st.container(border=True):
        panel("ATS history", "Saved resume analysis scores over time.")
        ats_rows = analytics["ats_history"]
        if ats_rows:
            figure = go.Figure(
                go.Scatter(
                    x=[row["created_at"] for row in ats_rows],
                    y=[row["ats_score"] for row in ats_rows],
                    mode="lines+markers",
                    line={"color": "#2563eb"},
                    marker={"size": 8},
                )
            )
            figure.update_yaxes(range=[0, 100], ticksuffix="%")
            figure.update_layout(height=280, margin={"l": 20, "r": 20, "t": 20, "b": 20})
            st.plotly_chart(figure, use_container_width=True)
        else:
            st.info("Analyze resumes to build ATS history.")
    with chart_right, st.container(border=True):
        panel("Interview score history", "Tracked mock interview feedback scores.")
        interview_rows = analytics["interview_scores"]
        if interview_rows:
            figure = go.Figure(
                go.Bar(
                    x=[row["created_at"] for row in interview_rows],
                    y=[row["score"] for row in interview_rows],
                    marker_color="#0f766e",
                )
            )
            figure.update_yaxes(range=[0, 100], ticksuffix="%")
            figure.update_layout(height=280, margin={"l": 20, "r": 20, "t": 20, "b": 20})
            st.plotly_chart(figure, use_container_width=True)
        else:
            st.info("Evaluate interview answers to build score history.")

    lower_left, lower_right = st.columns(2)
    with lower_left, st.container(border=True):
        panel("Career recommendation runs", "Most recent top role recommendations.")
        recommendation_rows = analytics["career_recommendations"]
        if recommendation_rows:
            figure = go.Figure(
                go.Bar(
                    x=[row["top_match"] for row in recommendation_rows],
                    y=[row["top_career"] for row in recommendation_rows],
                    orientation="h",
                    marker_color="#7c3aed",
                )
            )
            figure.update_xaxes(range=[0, 100], ticksuffix="%")
            figure.update_layout(height=280, margin={"l": 20, "r": 20, "t": 20, "b": 20})
            st.plotly_chart(figure, use_container_width=True)
        else:
            st.info("Generate recommendations to populate this chart.")
    with lower_right, st.container(border=True):
        panel("Database coverage", "Records tracked across the career mentor workflow.")
        labels = ["Profiles", "Resumes", "ATS", "Careers", "Roadmaps", "Interviews"]
        values = [
            counts["profiles"],
            counts["uploaded_resumes"],
            counts["ats_history"],
            counts["career_recommendations"],
            counts["roadmaps"],
            counts["interview_scores"],
        ]
        figure = go.Figure(go.Bar(x=labels, y=values, marker_color="#334155"))
        figure.update_layout(height=280, margin={"l": 20, "r": 20, "t": 20, "b": 20})
        st.plotly_chart(figure, use_container_width=True)

with profile_tab:
    s1, s2 = st.columns([2, 1])
    with s1, st.container(border=True):
        panel("User profile summary")
        c1, c2 = st.columns(2)
        c1.write(f"**College:** {profile.college or 'Not set'}")
        c1.write(f"**Degree:** {profile.degree or 'Not set'}")
        c1.write(f"**Branch:** {profile.branch or 'Not set'}")
        c2.write(f"**Graduation Year:** {profile.graduation_year or 'Not set'}")
        c2.write(f"**Experience:** {profile.experience_level or 'Not set'}")
        c2.write(f"**Resume Uploaded:** {'Yes' if latest_resume else 'No'}")
        st.write("**Skills:** " + (", ".join(skills) if skills else "No skills saved"))
        st.write("**Interests:** " + (", ".join(interests) if interests else "No interests saved"))
    with s2, st.container(border=True):
        panel("Quick actions")
        st.markdown("[Edit Profile](./Profile)")
        st.markdown("[Analyze Resume](./Resume_Analyzer)")
        st.markdown("[Find Careers](./Career_Recommendation)")
        st.markdown("[Build Roadmap](./Learning_Roadmap)")

with activity_tab, st.container(border=True):
    panel("Recent activity", "Latest saved profile, resume, roadmap, and interview events.")
    activities = recent_activities()
    if not activities:
        st.write("No activity yet. Save a profile or analyze a resume to begin.")
    else:
        st.dataframe(pd.DataFrame(activities), use_container_width=True, hide_index=True)
