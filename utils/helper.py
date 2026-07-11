"""
helper.py
----------------------------------------------------
Helper functions for the AI Interview Preparation
Assistant.
"""

import streamlit as st
import re


# ==========================================================
# SESSION INITIALIZATION
# ==========================================================

def initialize_session():

    defaults = {

        # Interview Status
        "started": False,
        "interview_completed": False,

        # User Settings
        "selected_model": "Gemini",
        "role": "Python Developer",
        "experience": "Fresher",
        "difficulty": "Medium",
        "interview_type": "Technical",
        "total_questions": 5,

        # Current State
        "question_number": 0,
        "current_question": "",
        "current_answer": "",
        "current_evaluation": "",

        # Interview Data
        "questions": [],
        "answers": [],
        "evaluations": [],
        "scores": [],
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ==========================================================
# RESET INTERVIEW
# ==========================================================

def reset_interview():

    st.session_state.started = False
    st.session_state.interview_completed = False

    st.session_state.question_number = 0

    st.session_state.current_question = ""
    st.session_state.current_answer = ""
    st.session_state.current_evaluation = ""

    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.evaluations = []
    st.session_state.scores = []


# ==========================================================
# NEXT QUESTION
# ==========================================================

def next_question():

    st.session_state.question_number += 1


# ==========================================================
# SAVE QUESTION
# ==========================================================

def save_question(question):

    st.session_state.questions.append(question)


# ==========================================================
# SAVE ANSWER
# ==========================================================

def save_answer(answer):

    st.session_state.answers.append(answer)


# ==========================================================
# SAVE EVALUATION
# ==========================================================

def save_evaluation(evaluation):

    st.session_state.evaluations.append(evaluation)


# ==========================================================
# SAVE SCORE
# ==========================================================

def save_score(score):

    st.session_state.scores.append(score)


# ==========================================================
# PROGRESS BAR
# ==========================================================

def get_progress():

    if st.session_state.total_questions == 0:
        return 0

    return min(
        st.session_state.question_number
        / st.session_state.total_questions,
        1.0,
    )


# ==========================================================
# CHECK INTERVIEW COMPLETION
# ==========================================================

def interview_finished():

    return (
        st.session_state.question_number
        >= st.session_state.total_questions
    )


# ==========================================================
# AVERAGE SCORE
# ==========================================================

def average_score():

    if len(st.session_state.scores) == 0:
        return 0

    return round(
        sum(st.session_state.scores)
        / len(st.session_state.scores),
        2,
    )


# ==========================================================
# EXTRACT SCORE
# ==========================================================

def extract_score(text):

    """
    Extract score from evaluation text.

    Example:
    Score: 8.5/10
    """

    match = re.search(
        r"Score:\s*(\d+(\.\d+)?)",
        text,
        re.IGNORECASE,
    )

    if match:

        return float(match.group(1))

    return 0


# ==========================================================
# CLEAR CURRENT RESPONSE
# ==========================================================

def clear_response():

    st.session_state.current_answer = ""
    st.session_state.current_evaluation = ""