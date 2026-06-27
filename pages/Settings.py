"""Settings page."""

from __future__ import annotations

import json

import streamlit as st

from utils.ai import has_ai_key
from utils.database import export_data, initialize_database, load_setting, reset_database, save_setting


st.set_page_config(page_title="Settings | AI Career Mentor", layout="wide")
initialize_database()

st.title("Settings")

with st.container(border=True):
    st.subheader("Theme")
    theme = st.selectbox("Preferred Theme", ["System", "Light", "Dark"], index=["System", "Light", "Dark"].index(load_setting("theme", "System")))
    if st.button("Save Theme", use_container_width=True):
        save_setting("theme", theme)
        st.success("Theme preference saved.")

with st.container(border=True):
    st.subheader("API Key")
    st.write("AI key detected." if has_ai_key() else "No AI key detected. Rule-based analysis is active.")
    key_hint = st.text_input("Optional API Key Label", value=load_setting("api_key_label", ""), type="password")
    if st.button("Save API Key Label", use_container_width=True):
        save_setting("api_key_label", key_hint)
        st.success("API key label saved locally. Secrets should still be stored in environment variables.")

with st.container(border=True):
    st.subheader("Export Data")
    data = export_data()
    st.download_button(
        "Download JSON Export",
        data=json.dumps(data, indent=2),
        file_name="ai_career_mentor_export.json",
        mime="application/json",
        use_container_width=True,
    )

with st.container(border=True):
    st.subheader("Database Reset")
    confirm = st.checkbox("I understand this will delete local profile, resume, activity, and settings data.")
    if st.button("Clear Database", disabled=not confirm, use_container_width=True):
        reset_database()
        st.success("Database cleared.")
