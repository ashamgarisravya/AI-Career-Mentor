"""AI Career Mentor Streamlit application."""

from __future__ import annotations

import streamlit as st

from utils.database import initialize_database
from utils.production import get_logger
from utils.ui import inject_styles, page_header


APP_TITLE = "AI Career Mentor"
logger = get_logger(__name__)
PAGES = [
    ("Dashboard", "pages/Dashboard.py"),
    ("Resume Analyzer", "pages/Resume_Analyzer.py"),
    ("Career Recommendation", "pages/Career_Recommendation.py"),
    ("Skill Gap Analysis", "pages/Skill_Gap.py"),
    ("Learning Roadmap", "pages/Learning_Roadmap.py"),
    ("Interview Preparation", "pages/Interview_Prep.py"),
    ("Resume Builder", "pages/Resume_Builder.py"),
    ("Profile", "pages/Profile.py"),
    ("Settings", "pages/Settings.py"),
]


def configure_page() -> None:
    """Configure global Streamlit page settings."""
    st.set_page_config(
        page_title=APP_TITLE,
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_sidebar() -> None:
    """Render application navigation."""
    with st.sidebar:
        inject_styles()
        st.title(APP_TITLE)
        st.caption("Career planning, resumes, roadmaps, and interview prep")
        st.divider()
        try:
            from streamlit_option_menu import option_menu

            option_menu(
                None,
                [label for label, _ in PAGES],
                icons=[
                    "speedometer2",
                    "file-earmark-text",
                    "briefcase",
                    "bar-chart",
                    "map",
                    "mic",
                    "pencil-square",
                    "person",
                    "gear",
                ],
                default_index=0,
            )
        except ImportError:
            logger.info("streamlit-option-menu is unavailable; using native page links.")
            st.caption("Navigation")
        st.caption("Pages")
        for label, page_path in PAGES:
            st.page_link(page_path, label=label)
        st.divider()
        st.caption("Run with: streamlit run app.py")


def main() -> None:
    """Render the home page."""
    initialize_database()
    configure_page()
    inject_styles()
    render_sidebar()
    page_header(
        APP_TITLE,
        "A professional workspace for resume scoring, career fit, learning plans, and interview readiness.",
        [("Resume intelligence", "info"), ("Career planning", "success"), ("Interview prep", "warning")],
    )
    left, middle, right = st.columns(3)
    left.metric("Workflow", "9 pages")
    middle.metric("Data store", "Local SQLite")
    right.metric("Mode", "Private")
    with st.container(border=True):
        st.subheader("Command center")
        st.write(
            "Use the sidebar to manage your profile, analyze resumes, discover careers, "
            "close skill gaps, build a roadmap, practice interviews, and generate a PDF resume."
        )
        st.page_link("pages/Dashboard.py", label="Open Dashboard")


if __name__ == "__main__":
    main()
