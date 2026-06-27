"""Interview preparation page."""

from __future__ import annotations

import streamlit as st

from utils.database import add_activity, initialize_database, load_profile, save_interview_score, split_list
from utils.interview import evaluate_answer, generate_questions
from utils.ui import badge, bullet_list, inject_styles, page_header, panel, status_kind


st.set_page_config(page_title="Interview Preparation | AI Career Mentor", layout="wide")
inject_styles()
initialize_database()
profile = load_profile()

page_header(
    "Interview Preparation",
    "Practice HR, technical, behavioral, and coding questions with scored feedback.",
    [("Question bank", "info"), ("Mock scoring", "success")],
)
target = st.text_input("Target Career", value=profile.target_career if profile else "AI Engineer")
skills = split_list(profile.skills) if profile else []
questions = generate_questions(skills, target)

tabs = st.tabs(list(questions.keys()) + ["Mock Interview"])
for tab, (category, items) in zip(tabs[:-1], questions.items(), strict=False):
    with tab:
        panel(category, "Use these prompts to prepare concise, evidence-backed responses.")
        for index, question in enumerate(items, start=1):
            with st.expander(f"Question {index}", expanded=index == 1):
                st.write(question)

with tabs[-1]:
    panel("Mock interview", "Choose a question, answer it, and get immediate structured feedback.")
    selected_question = st.selectbox("Choose a question", [q for group in questions.values() for q in group])
    answer = st.text_area("Your answer", height=180)
    if st.button("Evaluate Answer", use_container_width=True):
        if not answer.strip():
            st.warning("Write an answer before evaluating.")
        else:
            result = evaluate_answer(answer, selected_question, target)
            save_interview_score(
                target_career=target,
                question=selected_question,
                answer=answer,
                score=int(result["score"]),
                feedback=str(result["feedback"]),
                suggestions=result["suggestions"],
            )
            add_activity("Mock interview evaluated", f"Score: {result['score']}%")
            c1, c2 = st.columns([1, 2])
            c1.metric("Score", f"{result['score']}%")
            with c2:
                st.markdown(badge(result["feedback"], status_kind(int(result["score"]))), unsafe_allow_html=True)
                st.progress(int(result["score"]) / 100)
            st.write("**Improvement suggestions**")
            bullet_list(result["suggestions"])
