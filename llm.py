"""
llm.py
---------------------------------------
Handles loading the Gemini model.
Compatible with Streamlit Cloud.
"""

import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

# ----------------------------------------
# Load Environment Variables
# ----------------------------------------

load_dotenv()


class LLMManager:
    """Handles loading Gemini."""

    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")

    def load_model(self, model_name: str = "Gemini", temperature: float = 0.7):

        if not self.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found. Please add it in Streamlit Secrets."
            )

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.google_api_key,
            temperature=temperature,
        )


# ----------------------------------------
# Global Manager
# ----------------------------------------

llm_manager = LLMManager()


def get_llm(model_name: str = "Gemini", temperature: float = 0.7):
    """
    Returns the Gemini model.
    """
    return llm_manager.load_model(
        model_name=model_name,
        temperature=temperature,
    )


# ----------------------------------------
# Test
# ----------------------------------------

if __name__ == "__main__":

    llm = get_llm()

    response = llm.invoke(
        "Introduce yourself in one sentence."
    )

    print(response.content)