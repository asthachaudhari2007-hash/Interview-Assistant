"""
AI Interview Preparation Assistant
----------------------------------
Main Streamlit Application

Features
--------
✓ Resume Upload (RAG)
✓ Gemini / Llama Support
✓ Resume-Based Interview
✓ AI Evaluation
✓ Performance Dashboard
✓ Interview Report
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
import tempfile

import streamlit as st

from rag.pdf_loader import load_pdf
from rag.chunking import chunk_documents
from rag.vector_store import create_vectorstore
from rag.retriever import retrieve_resume_context

from llm import get_llm

from agents.question_agent import QuestionAgent
from agents.evaluation_agent import EvaluationAgent

from utils.session import (
    initialize_session,
    reset_interview,
    interview_finished,
    next_question,
    save_question,
    save_answer,
    save_score,
    save_evaluation,
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="💼",
    layout="wide",
)

initialize_session()

# ============================================================
# TITLE
# ============================================================

st.title("💼 AI Interview Preparation Assistant")

st.caption(
    "Practice Technical & HR Interviews using Gemini or Llama 3.2"
)

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙ Interview Settings")

    # -------------------------------------------------------
    # Resume Upload
    # -------------------------------------------------------

    uploaded_file = st.file_uploader(
        "📄 Upload Resume (Optional)",
        type=["pdf"],
    )

    st.divider()

    # -------------------------------------------------------
    # MODEL
    # -------------------------------------------------------

    selected_model = st.radio(
        "Choose AI Model",
        [
            "Gemini",
            "Llama 3.2",
        ],
    )

    st.session_state.selected_model = selected_model

    # -------------------------------------------------------
    # ROLE
    # -------------------------------------------------------

    role = st.selectbox(
        "Job Role",
        [
            "Python Developer",
            "Java Developer",
            "Data Analyst",
            "Machine Learning Engineer",
            "AI Engineer",
            "Full Stack Developer",
            "Backend Developer",
            "Frontend Developer",
        ],
    )

    st.session_state.role = role

    # -------------------------------------------------------
    # EXPERIENCE
    # -------------------------------------------------------

    experience = st.selectbox(
        "Experience",
        [
            "Fresher",
            "0-1 Years",
            "1-3 Years",
            "3-5 Years",
            "5+ Years",
        ],
    )

    st.session_state.experience = experience

    # -------------------------------------------------------
    # DIFFICULTY
    # -------------------------------------------------------

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard",
        ],
    )

    st.session_state.difficulty = difficulty

    # -------------------------------------------------------
    # INTERVIEW TYPE
    # -------------------------------------------------------

    interview_type = st.selectbox(
        "Interview Type",
        [
            "Technical",
            "HR",
            "Behavioral",
            "Mixed",
        ],
    )

    st.session_state.interview_type = interview_type

    # -------------------------------------------------------
    # NUMBER OF QUESTIONS
    # -------------------------------------------------------

    total_questions = st.slider(
        "Number of Questions",
        min_value=5,
        max_value=20,
        value=10,
    )

    st.session_state.total_questions = total_questions

    st.divider()

    start_interview = st.button(
        "🚀 Start Interview",
        use_container_width=True,
    )

# ============================================================
# RESUME PROCESSING
# ============================================================

if uploaded_file is not None:

    if not st.session_state.resume_uploaded:

        with st.spinner("Reading Resume..."):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as tmp:

                tmp.write(uploaded_file.read())

                pdf_path = tmp.name

            documents = load_pdf(pdf_path)

            chunks = chunk_documents(documents)

            vectorstore = create_vectorstore(chunks)

            st.session_state.vectorstore = vectorstore

            st.session_state.resume_uploaded = True

        st.success("✅ Resume processed successfully!")

else:

    st.session_state.resume_uploaded = False
    # ============================================================
# START INTERVIEW
# ============================================================

if start_interview:

    reset_interview()

    st.session_state.started = True
    st.session_state.question_number = 0
    st.session_state.current_question = ""
    st.session_state.current_answer = ""
    st.session_state.current_evaluation = ""
    st.session_state.interview_completed = False

    st.rerun()


# ============================================================
# WAIT UNTIL INTERVIEW STARTS
# ============================================================

if not st.session_state.started:

    st.info(
        "👈 Configure the interview settings from the sidebar and click **Start Interview**."
    )

    st.stop()


# ============================================================
# PROGRESS BAR
# ============================================================

progress = (
    st.session_state.question_number
    / st.session_state.total_questions
)

st.progress(progress)


c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Role",
        st.session_state.role,
    )

with c2:

    st.metric(
        "Interview",
        st.session_state.interview_type,
    )

with c3:

    st.metric(
        "Question",
        f"{st.session_state.question_number + 1}/{st.session_state.total_questions}",
    )

st.divider()


# ============================================================
# GENERATE FIRST QUESTION
# ============================================================

if st.session_state.current_question == "":

    with st.spinner("🤖 Generating Interview Question..."):

        question_agent = QuestionAgent(
            model_name=st.session_state.selected_model
        )

        # ---------------------------------------------
        # Resume Based Interview
        # ---------------------------------------------

        if st.session_state.resume_uploaded:

            query = f"""
Generate ONE interview question.

Role:
{st.session_state.role}

Experience:
{st.session_state.experience}

Difficulty:
{st.session_state.difficulty}

Interview Type:
{st.session_state.interview_type}

Focus on the candidate's resume.

Avoid asking repeated questions.
"""

            resume_context = retrieve_resume_context(
                st.session_state.vectorstore,
                query,
            )

            question = question_agent.generate_resume_question(
                resume_context=resume_context,
                role=st.session_state.role,
                experience=st.session_state.experience,
                difficulty=st.session_state.difficulty,
                interview_type=st.session_state.interview_type,
                previous_questions=st.session_state.questions,
            )

        # ---------------------------------------------
        # Normal Interview
        # ---------------------------------------------

        else:

            question = question_agent.generate_question(
                role=st.session_state.role,
                experience=st.session_state.experience,
                difficulty=st.session_state.difficulty,
                interview_type=st.session_state.interview_type,
                previous_questions=st.session_state.questions,
            )

        st.session_state.current_question = question

        save_question(question)

        next_question()


# ============================================================
# QUESTION CARD
# ============================================================

st.markdown("## 🎯 Interview Question")

st.markdown(
    f"""
<div style="
padding:20px;
border-radius:12px;
background:#F8FAFC;
border-left:8px solid #2563EB;
font-size:18px;
line-height:1.8;
">

{st.session_state.current_question}

</div>
""",
    unsafe_allow_html=True,
)

st.write("")


# ============================================================
# ANSWER INPUT
# ============================================================

st.markdown("## ✍ Your Answer")

answer = st.text_area(
    "",
    value=st.session_state.current_answer,
    height=220,
    placeholder="Type your answer here...",
)

st.session_state.current_answer = answer


# ============================================================
# BUTTONS
# ============================================================

left, right = st.columns([4, 1])

with left:

    submit = st.button(
        "✅ Submit Answer",
        use_container_width=True,
    )

with right:

    clear = st.button(
        "🗑 Clear",
        use_container_width=True,
    )

if clear:

    st.session_state.current_answer = ""

    st.rerun()
    # ============================================================
# EVALUATE ANSWER
# ============================================================

if submit:

    if answer.strip() == "":

        st.warning("⚠ Please enter your answer before submitting.")

    else:

        with st.spinner("🤖 Evaluating your answer..."):

            evaluator = EvaluationAgent(
                model_name=st.session_state.selected_model
            )

            # --------------------------------------------------
            # Resume-Based Evaluation
            # --------------------------------------------------

            if st.session_state.resume_uploaded:

                query = f"""
Evaluate the candidate's interview answer.

Interview Question:
{st.session_state.current_question}

Candidate Answer:
{answer}

Give:
1. Score out of 10
2. Strengths
3. Weaknesses
4. Suggestions
"""

                resume_context = retrieve_resume_context(
                    st.session_state.vectorstore,
                    query,
                )

                result = evaluator.evaluate_resume_answer(
                    resume_context=resume_context,
                    question=st.session_state.current_question,
                    answer=answer,
                )

            # --------------------------------------------------
            # Normal Evaluation
            # --------------------------------------------------

            else:

                result = evaluator.evaluate(
                    question=st.session_state.current_question,
                    answer=answer,
                )

            # --------------------------------------------------
            # Store Results
            # --------------------------------------------------

            score = result.get("score", 0)

            evaluation = result.get(
                "evaluation",
                "No feedback generated."
            )

            st.session_state.current_evaluation = evaluation

            save_answer(answer)

            save_score(score)

            save_evaluation(evaluation)

# ============================================================
# SHOW FEEDBACK
# ============================================================

if st.session_state.current_evaluation != "":

    st.divider()

    st.header("🤖 AI Feedback")

    latest_score = 0

    if len(st.session_state.scores) > 0:

        latest_score = st.session_state.scores[-1]

    col1, col2 = st.columns([1, 3])

    with col1:

        st.metric(
            "Score",
            f"{latest_score}/10",
        )

    with col2:

        if latest_score >= 8:

            st.success("🌟 Excellent Answer!")

        elif latest_score >= 6:

            st.info("👍 Good Answer!")

        else:

            st.warning("📚 Needs Improvement")

    st.markdown(
        f"""
<div style="
padding:20px;
background:#F8FAFC;
border-left:6px solid #2563EB;
border-radius:12px;
line-height:1.8;
">

{st.session_state.current_evaluation}

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    # ========================================================
    # ACTION BUTTONS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        next_btn = st.button(
            "➡ Next Question",
            use_container_width=True,
        )

    with col2:

        finish_btn = st.button(
            "🏁 Finish Interview",
            use_container_width=True,
        )
        # ============================================================
# NEXT QUESTION
# ============================================================

if "next_btn" in locals() and next_btn:

    # --------------------------------------------------------
    # Interview Finished?
    # --------------------------------------------------------

    if interview_finished():

        st.session_state.interview_completed = True

        st.rerun()

    with st.spinner("🤖 Generating next question..."):

        question_agent = QuestionAgent(
            model_name=st.session_state.selected_model
        )

        # ----------------------------------------------------
        # Resume-Based Question
        # ----------------------------------------------------

        if st.session_state.resume_uploaded:

            query = f"""
Generate ONE NEW interview question.

Role:
{st.session_state.role}

Experience:
{st.session_state.experience}

Difficulty:
{st.session_state.difficulty}

Interview Type:
{st.session_state.interview_type}

Rules:
- Focus on the uploaded resume.
- Do NOT repeat previous questions.
- Ask about another project, skill or technology.
"""

            resume_context = retrieve_resume_context(
                st.session_state.vectorstore,
                query,
            )

            new_question = question_agent.generate_resume_question(
                resume_context=resume_context,
                role=st.session_state.role,
                experience=st.session_state.experience,
                difficulty=st.session_state.difficulty,
                interview_type=st.session_state.interview_type,
                previous_questions=st.session_state.questions,
            )

        # ----------------------------------------------------
        # Normal Question
        # ----------------------------------------------------

        else:

            new_question = question_agent.generate_question(
                role=st.session_state.role,
                experience=st.session_state.experience,
                difficulty=st.session_state.difficulty,
                interview_type=st.session_state.interview_type,
                previous_questions=st.session_state.questions,
            )

    # --------------------------------------------------------
    # Reset for Next Question
    # --------------------------------------------------------

    st.session_state.current_question = new_question

    st.session_state.current_answer = ""

    st.session_state.current_evaluation = ""

    save_question(new_question)

    next_question()

    st.rerun()


# ============================================================
# FINISH INTERVIEW
# ============================================================

if "finish_btn" in locals() and finish_btn:

    st.session_state.interview_completed = True

    st.rerun()


# ============================================================
# INTERVIEW COMPLETED
# ============================================================

if st.session_state.interview_completed:

    st.balloons()

    st.success("🎉 Interview Completed Successfully!")

    total_questions = len(st.session_state.scores)

    average_score = 0

    if total_questions > 0:

        average_score = round(
            sum(st.session_state.scores) / total_questions,
            2,
        )

    highest_score = max(st.session_state.scores) if total_questions else 0

    lowest_score = min(st.session_state.scores) if total_questions else 0

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average",
            f"{average_score}/10",
        )

    with col2:

        st.metric(
            "Highest",
            f"{highest_score}/10",
        )

    with col3:

        st.metric(
            "Lowest",
            f"{lowest_score}/10",
        )

    st.divider()

    if average_score >= 8:

        st.success("🌟 Excellent Interview Performance!")

    elif average_score >= 6:

        st.info("👍 Good Performance! Keep Practicing.")

    else:

        st.warning("📚 Keep practicing to improve your interview skills.")

    # --------------------------------------------------------
    # Restart Interview
    # --------------------------------------------------------

    if st.button(
        "🔄 Start New Interview",
        use_container_width=True,
    ):

        reset_interview()

        st.rerun()
        # ============================================================
# PERFORMANCE DASHBOARD
# ============================================================

if st.session_state.interview_completed:

    st.divider()

    st.header("📊 Interview Performance Dashboard")

    scores = st.session_state.scores
    questions = st.session_state.questions
    answers = st.session_state.answers
    evaluations = st.session_state.evaluations

    if len(scores) > 0:

        average = round(sum(scores) / len(scores), 2)
        percentage = round((average / 10) * 100, 2)

    else:

        average = 0
        percentage = 0

    # ========================================================
    # OVERALL METRICS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average Score",
            f"{average}/10",
        )

    with col2:

        st.metric(
            "Percentage",
            f"{percentage}%",
        )

    with col3:

        if percentage >= 85:
            grade = "Excellent"

        elif percentage >= 70:
            grade = "Very Good"

        elif percentage >= 50:
            grade = "Good"

        else:
            grade = "Needs Improvement"

        st.metric(
            "Performance",
            grade,
        )

    st.divider()

    # ========================================================
    # SCORE CHART
    # ========================================================

    st.subheader("📈 Question-wise Scores")

    chart_data = {
        "Question": [
            f"Q{i+1}"
            for i in range(len(scores))
        ],
        "Score": scores,
    }

    st.line_chart(
        chart_data,
        x="Question",
        y="Score",
    )

    st.bar_chart(
        chart_data,
        x="Question",
        y="Score",
    )

    st.divider()

    # ========================================================
    # INTERVIEW REPORT
    # ========================================================

    st.subheader("📄 Complete Interview Report")

    report = ""

    for i in range(len(questions)):

        report += "=" * 70 + "\n"
        report += f"QUESTION {i+1}\n"
        report += "=" * 70 + "\n\n"

        report += f"Question:\n{questions[i]}\n\n"

        if i < len(answers):

            report += "Your Answer:\n"
            report += answers[i]
            report += "\n\n"

        if i < len(evaluations):

            report += "AI Feedback:\n"
            report += evaluations[i]
            report += "\n\n"

        if i < len(scores):

            report += f"Score : {scores[i]}/10\n\n"

    st.text_area(
        "Interview Summary",
        report,
        height=450,
    )

    st.download_button(
        "📥 Download Interview Report",
        data=report,
        file_name="Interview_Report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.divider()

    # ========================================================
    # FINAL FEEDBACK
    # ========================================================

    st.subheader("🎯 Final AI Feedback")

    if percentage >= 90:

        st.success("""
🌟 Excellent!

You demonstrated:

✅ Strong technical knowledge

✅ Good communication

✅ Clear explanations

✅ Confidence

You are interview-ready.
""")

    elif percentage >= 75:

        st.info("""
👍 Very Good!

Strengths:

✔ Good understanding

✔ Clear communication

Suggestions:

• Improve confidence

• Give more real-life examples

• Practice advanced questions
""")

    elif percentage >= 60:

        st.warning("""
📚 Average Performance

Suggestions:

• Improve technical depth

• Explain concepts more clearly

• Practice coding problems

• Prepare project explanations
""")

    else:

        st.error("""
⚠ Needs Improvement

Focus on:

• Core concepts

• Communication

• Mock interviews

• Resume-based preparation

Practice consistently and try another interview.
""")

    st.divider()

    # ========================================================
    # RESTART
    # ========================================================

    if st.button(
        "🚀 Start New Interview",
        use_container_width=True,
    ):

        reset_interview()

        st.rerun()