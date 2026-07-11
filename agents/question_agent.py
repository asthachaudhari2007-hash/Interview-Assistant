"""
question_agent.py
-------------------------------------------------------
AI Question Generation Agent

Supports:
✔ Normal Interview
✔ Resume-Based Interview (RAG)
✔ Gemini
✔ Llama 3.2

Author: Astha Chaudhari
"""

from llm import get_llm
from prompts import QUESTION_PROMPT, RESUME_QUESTION_PROMPT


class QuestionAgent:
    """
    Generates interview questions using the selected LLM.
    """

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.7,
    ):
        self.llm = get_llm(
            model_name=model_name,
            temperature=temperature,
        )

    # ----------------------------------------------------
    # NORMAL QUESTION GENERATION
    # ----------------------------------------------------

    def generate_question(
        self,
        role: str,
        experience: str,
        difficulty: str,
        interview_type: str,
        previous_questions=None,
    ):
        """
        Generate a normal interview question.
        """

        if previous_questions is None:
            previous_questions = []

        chain = QUESTION_PROMPT | self.llm

        response = chain.invoke(
            {
                "role": role,
                "experience": experience,
                "difficulty": difficulty,
                "interview_type": interview_type,
                "previous_questions": (
                    "\n".join(previous_questions)
                    if previous_questions
                    else "None"
                ),
            }
        )

        return response.content.strip()

    # ----------------------------------------------------
    # RESUME-BASED QUESTION GENERATION
    # ----------------------------------------------------

    def generate_resume_question(
        self,
        resume_context: str,
        role: str,
        experience: str,
        difficulty: str,
        interview_type: str,
        previous_questions=None,
    ):
        """
        Generate interview questions using resume context.
        """

        if previous_questions is None:
            previous_questions = []

        chain = RESUME_QUESTION_PROMPT | self.llm

        response = chain.invoke(
            {
                "resume_context": resume_context,
                "role": role,
                "experience": experience,
                "difficulty": difficulty,
                "interview_type": interview_type,
                "previous_questions": (
                    "\n".join(previous_questions)
                    if previous_questions
                    else "None"
                ),
            }
        )

        return response.content.strip()

    # ----------------------------------------------------
    # MULTIPLE NORMAL QUESTIONS
    # ----------------------------------------------------

    def generate_multiple_questions(
        self,
        role,
        experience,
        difficulty,
        interview_type,
        total_questions=5,
    ):

        questions = []

        for _ in range(total_questions):

            question = self.generate_question(
                role=role,
                experience=experience,
                difficulty=difficulty,
                interview_type=interview_type,
                previous_questions=questions,
            )

            questions.append(question)

        return questions

    # ----------------------------------------------------
    # MULTIPLE RESUME QUESTIONS
    # ----------------------------------------------------

    def generate_resume_questions(
        self,
        resume_context,
        role,
        experience,
        difficulty,
        interview_type,
        total_questions=5,
    ):

        questions = []

        for _ in range(total_questions):

            question = self.generate_resume_question(
                resume_context=resume_context,
                role=role,
                experience=experience,
                difficulty=difficulty,
                interview_type=interview_type,
                previous_questions=questions,
            )

            questions.append(question)

        return questions


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    MODEL = "Gemini"

    agent = QuestionAgent(MODEL)

    # Example resume context
    resume_context = """
    Candidate Name: Astha Chaudhari

    Skills:
    Python
    LangChain
    Streamlit
    FAISS
    Gemini API
    Llama 3.2

    Projects:
    1. AI Interview Preparation Assistant
    2. Mini RAG Studio
    3. Breast Cancer Prediction

    Internship:
    AI Developer Intern
    """

    questions = agent.generate_resume_questions(
        resume_context=resume_context,
        role="Python Developer",
        experience="Fresher",
        difficulty="Medium",
        interview_type="Technical",
        total_questions=5,
    )

    print("=" * 80)

    for i, q in enumerate(questions, start=1):

        print(f"\nQuestion {i}")
        print("-" * 60)
        print(q)
