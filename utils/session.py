"""
session.py
-------------------------
Manages Streamlit Session State
"""

import streamlit as st


def initialize_session():
    """Initialize all session state variables."""

    defaults = {
        "started": False,
        "resume_uploaded": False,
        "vectorstore": None,
        "selected_model": "Gemini",
        "role": "Python Developer",
        "experience": "Fresher",
        "difficulty": "Easy",
        "interview_type": "Technical",
        "total_questions": 5,
        "question_number": 0,
        "current_question": "",
        "current_answer": "",
        "current_evaluation": "",
        "questions": [],
        "answers": [],
        "scores": [],
        "evaluations": [],
        "interview_completed": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_interview():
    """Reset interview data."""

    st.session_state.started = False
    st.session_state.question_number = 0
    st.session_state.current_question = ""
    st.session_state.current_answer = ""
    st.session_state.current_evaluation = ""
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.scores = []
    st.session_state.evaluations = []
    st.session_state.interview_completed = False


def next_question():
    """Move to the next question."""
    st.session_state.question_number += 1


def interview_finished():
    """Return True if interview is complete."""
    return (
        st.session_state.question_number
        >= st.session_state.total_questions
    )


def save_question(question):
    st.session_state.questions.append(question)


def save_answer(answer):
    st.session_state.answers.append(answer)


def save_score(score):
    st.session_state.scores.append(score)


def save_evaluation(evaluation):
    st.session_state.evaluations.append(evaluation)