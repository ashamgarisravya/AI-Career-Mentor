"""Learning roadmap page."""

from __future__ import annotations

import streamlit as st

from utils.database import add_activity, initialize_database, load_profile, split_list
from utils.roadmap import calculate_progress, generate_roadmaps


st.set_page_config(page_title="Learning Roadmap | AI Career Mentor", layout="wide")
initialize_database()
profile = load_profile()

st.title("Learning Roadmap")
target = st.text_input("Target Career", value=profile.target_career if profile else "AI Engineer")
skills = split_list(profile.skills) if profile else []

roadmaps = generate_roadmaps(skills, target)
add = st.button("Refresh Roadmap", use_container_width=True)
if add:
    add_activity("Learning roadmap generated", f"Roadmap for {target}")

completed = {}
for period, items in roadmaps.items():
    for item in items:
        key = f"{period}-{item['week']}"
        completed[str(item["week"])] = st.session_state.get(key, False)

progress_percent = calculate_progress(completed, roadmaps)
st.progress(progress_percent / 100)
st.caption(f"{progress_percent}% complete")

for period, items in roadmaps.items():
    st.subheader(period)
    for item in items:
        with st.container(border=True):
            st.write(f"**{item['week']}**")
            st.write(f"Goal: {item['goal']}")
            st.write(f"Project: {item['project']}")
            st.write(f"Milestone: {item['milestone']}")
            st.checkbox("Milestone completed", key=f"{period}-{item['week']}")
            st.write("Resources:")
            for resource in item["resources"]:
                st.write(f"- {resource}")
