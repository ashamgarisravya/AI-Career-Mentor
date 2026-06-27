"""Learning roadmap page."""

from __future__ import annotations

import sqlite3

import streamlit as st

from utils.database import add_activity, initialize_database, load_profile, save_roadmap, split_list
from utils.roadmap import calculate_progress, generate_roadmaps
from utils.production import get_logger
from utils.ui import badge, bullet_list, inject_styles, page_header, panel, status_kind


st.set_page_config(page_title="Learning Roadmap | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()
profile = load_profile()
logger = get_logger(__name__)

page_header(
    "Learning Roadmap",
    "Plan the next 90 days with weekly milestones, project work, resources, and progress tracking.",
    [("30/60/90 plan", "info"), ("Progress tracking", "success")],
)
target = st.text_input("Target Career", value=profile.target_career if profile else "AI Engineer").strip() or "AI Engineer"
skills = split_list(profile.skills) if profile else []

with st.spinner("Preparing roadmap..."):
    roadmaps = generate_roadmaps(skills, target)
completed = {}
for period, items in roadmaps.items():
    for item in items:
        key = f"{period}-{item['week']}"
        completed[str(item["week"])] = st.session_state.get(key, False)

progress_percent = calculate_progress(completed, roadmaps)
add = st.button("Refresh Roadmap", use_container_width=True)
if add:
    with st.spinner("Saving roadmap snapshot..."):
        try:
            save_roadmap(target_career=target, skills=skills, roadmap=roadmaps, progress=progress_percent)
            add_activity("Learning roadmap generated", f"Roadmap for {target}")
        except sqlite3.Error as exc:
            logger.exception("Roadmap save failed: %s", exc)
            st.error("Roadmap could not be saved. Please try again.")
        else:
            st.success("Roadmap saved.")
c1, c2, c3 = st.columns(3)
c1.metric("Learning Progress", f"{progress_percent}%")
c2.metric("Target Career", target)
c3.metric("Milestones", sum(len(items) for items in roadmaps.values()))
st.markdown(badge(f"{progress_percent}% complete", status_kind(progress_percent)), unsafe_allow_html=True)
st.progress(progress_percent / 100)

tabs = st.tabs(list(roadmaps.keys()))
for tab, (period, items) in zip(tabs, roadmaps.items(), strict=False):
    with tab:
        panel(period, "Weekly execution plan with a practical deliverable.")
        for item in items:
            with st.expander(str(item["week"]), expanded=True):
                left, right = st.columns([1.2, 1])
                with left:
                    st.write(f"**Goal:** {item['goal']}")
                    st.write(f"**Project:** {item['project']}")
                    st.write(f"**Milestone:** {item['milestone']}")
                    st.checkbox("Milestone completed", key=f"{period}-{item['week']}")
                with right:
                    st.write("**Resources**")
                    bullet_list(item["resources"])
