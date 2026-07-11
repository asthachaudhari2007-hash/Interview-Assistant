"""
embeddings.py
------------------------------------
Embedding model loader

Uses HuggingFace embeddings for all LLMs.
"""

from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings(model_name="Gemini"):
    """
    Return the embedding model.

    The model_name parameter is kept only for compatibility
    with the rest of the project.
    """

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )