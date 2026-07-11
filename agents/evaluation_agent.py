"""
evaluation_agent.py
-------------------------------------------------------
AI Evaluation Agent

Evaluates candidate interview answers.

Features
--------
✔ Score (0-10)
✔ Strengths
✔ Weaknesses
✔ Ideal Answer
✔ Suggestions
✔ Resume-based Evaluation (RAG)

Supports:
- Gemini
- Llama 3.2

Author: Astha Chaudhari
"""

import re

from llm import get_llm
from prompts import (
    EVALUATION_PROMPT,
    RESUME_EVALUATION_PROMPT,
)


class EvaluationAgent:
    """
    AI Interview Evaluation Agent.
    """

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.3,
    ):
        self.llm = get_llm(
            model_name=model_name,
            temperature=temperature,
        )

    # ---------------------------------------------------
    # Normal Evaluation
    # ---------------------------------------------------

    def evaluate_answer(
        self,
        question: str,
        answer: str,
    ):
        """
        Evaluate answer without resume.
        """

        chain = EVALUATION_PROMPT | self.llm

        response = chain.invoke(
            {
                "question": question,
                "answer": answer,
            }
        )

        return response.content.strip()

    # ---------------------------------------------------
    # Resume Evaluation
    # ---------------------------------------------------

    def evaluate_resume_answer(
        self,
        resume_context: str,
        question: str,
        answer: str,
    ):
        """
        Evaluate answer using resume context.
        """

        chain = RESUME_EVALUATION_PROMPT | self.llm

        response = chain.invoke(
            {
                "resume_context": resume_context,
                "question": question,
                "answer": answer,
            }
        )

        evaluation = response.content.strip()

        score = self.extract_score(evaluation)

        return {
            "score": score,
            "rating": self.get_rating(score),
            "color": self.get_score_color(score),
            "evaluation": evaluation,
        }

    # ---------------------------------------------------

    @staticmethod
    def extract_score(evaluation: str):
        """
        Extract numeric score.
        """

        match = re.search(
            r"Score:\s*(\d+(\.\d+)?)",
            evaluation,
            re.IGNORECASE,
        )

        if match:
            return float(match.group(1))

        return 0.0

    # ---------------------------------------------------

    @staticmethod
    def get_score_color(score):

        if score >= 8:
            return "🟢"

        if score >= 5:
            return "🟡"

        return "🔴"

    # ---------------------------------------------------

    @staticmethod
    def get_rating(score):

        if score >= 9:
            return "Excellent"

        if score >= 8:
            return "Very Good"

        if score >= 7:
            return "Good"

        if score >= 5:
            return "Average"

        return "Needs Improvement"

    # ---------------------------------------------------

    def evaluate(
        self,
        question,
        answer,
    ):
        """
        Normal evaluation.
        """

        evaluation = self.evaluate_answer(
            question,
            answer,
        )

        score = self.extract_score(
            evaluation
        )

        return {
            "score": score,
            "rating": self.get_rating(score),
            "color": self.get_score_color(score),
            "evaluation": evaluation,
        }


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    MODEL = "Gemini"

    QUESTION = (
        "Explain the difference between a Python List and Tuple."
    )

    ANSWER = (
        "List is mutable while Tuple is immutable. "
        "Lists use square brackets and tuples use parentheses."
    )

    evaluator = EvaluationAgent(MODEL)

    result = evaluator.evaluate(
        QUESTION,
        ANSWER,
    )

    print("=" * 60)
    print("Evaluation Result")
    print("=" * 60)

    print("\nScore :", result["score"])
    print("Rating :", result["rating"])
    print("\n")
    print(result["evaluation"])