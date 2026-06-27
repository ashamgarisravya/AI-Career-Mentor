"""Settings page."""

from __future__ import annotations

import json

import streamlit as st

from utils.ai import has_ai_key
from utils.database import export_data, initialize_database, load_setting, reset_database, save_setting
from utils.ui import badge, inject_styles, page_header, panel


st.set_page_config(page_title="Settings | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()

page_header(
    "Settings",
    "Manage local preferences, data export, AI key status, and database reset controls.",
    [("Local settings", "info"), ("Data export", "success")],
)

pref_tab, data_tab, danger_tab = st.tabs(["Preferences", "Data", "Reset"])

with pref_tab:
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            panel("Theme")
            theme = st.selectbox("Preferred Theme", ["System", "Light", "Dark"], index=["System", "Light", "Dark"].index(load_setting("theme", "System")))
            if st.button("Save Theme", use_container_width=True):
                save_setting("theme", theme)
                st.success("Theme preference saved.")
    with right:
        with st.container(border=True):
            panel("API Key")
            st.markdown(
                badge("AI key detected", "success") if has_ai_key() else badge("Rule-based mode", "warning"),
                unsafe_allow_html=True,
            )
            key_hint = st.text_input("Optional API Key Label", value=load_setting("api_key_label", ""), type="password")
            if st.button("Save API Key Label", use_container_width=True):
                save_setting("api_key_label", key_hint)
                st.success("API key label saved locally. Secrets should still be stored in environment variables.")

with data_tab:
    with st.container(border=True):
        panel("Export Data", "Download profile, resume analysis, activities, and settings as JSON.")
        data = export_data()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Profiles", len(data["profiles"]))
        c2.metric("Resume Analyses", len(data["resume_analyses"]))
        c3.metric("Activities", len(data["activities"]))
        c4.metric("Settings", len(data["settings"]))
        st.download_button(
            "Download JSON Export",
            data=json.dumps(data, indent=2),
            file_name="ai_career_mentor_export.json",
            mime="application/json",
            use_container_width=True,
        )

with danger_tab:
    with st.container(border=True):
        panel("Database Reset", "Clears local profile, resume, activity, and settings data.")
        confirm = st.checkbox("I understand this will delete local profile, resume, activity, and settings data.")
        if st.button("Clear Database", disabled=not confirm, use_container_width=True):
            reset_database()
            st.success("Database cleared.")
