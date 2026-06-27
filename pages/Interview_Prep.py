"""Interview preparation page."""

from __future__ import annotations

import streamlit as st

from utils.database import add_activity, initialize_database, load_profile, split_list
from utils.interview import evaluate_answer, generate_questions


st.set_page_config(page_title="Interview Preparation | AI Career Mentor", layout="wide")
initialize_database()
profile = load_profile()

st.title("Interview Preparation")
target = st.text_input("Target Career", value=profile.target_career if profile else "AI Engineer")
skills = split_list(profile.skills) if profile else []
questions = generate_questions(skills, target)

tabs = st.tabs(list(questions.keys()) + ["Mock Interview"])
for tab, (category, items) in zip(tabs[:-1], questions.items(), strict=False):
    with tab:
        for question in items:
            st.write(f"- {question}")

with tabs[-1]:
    selected_question = st.selectbox("Choose a question", [q for group in questions.values() for q in group])
    answer = st.text_area("Your answer", height=180)
    if st.button("Evaluate Answer", use_container_width=True):
        if not answer.strip():
            st.warning("Write an answer before evaluating.")
        else:
            result = evaluate_answer(answer)
            add_activity("Mock interview evaluated", f"Score: {result['score']}%")
            st.metric("Score", f"{result['score']}%")
            st.write(result["feedback"])
            st.write("Improvement suggestions:")
            for suggestion in result["suggestions"]:
                st.write(f"- {suggestion}")
