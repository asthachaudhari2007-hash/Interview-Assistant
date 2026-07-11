"""
llm.py
---------------------------------------
Handles loading and switching between
Gemini and Llama 3.2 models.
"""

import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

# ----------------------------------------
# Load Environment Variables
# ----------------------------------------

load_dotenv()


class LLMManager:
    """Handles loading different LLMs."""

    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")

    # ----------------------------------------

    def load_model(self, model_name: str, temperature: float = 0.7):

        model_name = model_name.strip()

        if model_name == "Gemini":

            if not self.google_api_key:
                raise ValueError(
                    "GOOGLE_API_KEY not found. Please check your .env file."
                )

            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=self.google_api_key,
                temperature=temperature,
            )

        elif model_name == "Llama 3.2":

            return ChatOllama(
                model="llama3.2",
                temperature=temperature,
            )

        else:

            raise ValueError(
                f"Unsupported model: {model_name}"
            )


# ----------------------------------------
# Global Manager
# ----------------------------------------

llm_manager = LLMManager()


def get_llm(model_name: str, temperature: float = 0.7):
    """
    Returns the selected LLM.
    """

    return llm_manager.load_model(
        model_name=model_name,
        temperature=temperature,
    )


# ----------------------------------------
# Test
# ----------------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print("Available Models")
    print("=" * 50)
    print("1. Gemini")
    print("2. Llama 3.2")
    print()

    choice = input("Enter model name: ")

    try:

        llm = get_llm(choice)

        response = llm.invoke(
            "Introduce yourself in one sentence."
        )

        print("\nResponse:\n")
        print(response.content)

    except Exception as e:

        print("\nError:")
        print(e)