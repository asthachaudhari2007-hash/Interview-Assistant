"""
vector_store.py
----------------------------------------
Creates and manages the FAISS vector database.
"""

from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embeddings


def create_vectorstore(
    chunks,
    model_name="Gemini"
):
    """
    Create a FAISS vector database from document chunks.
    """

    if not chunks:
        raise ValueError("No document chunks were provided.")

    embeddings = get_embeddings(model_name)

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    return vectorstore


def load_vectorstore(
    embeddings,
    folder_path
):
    """
    Load an existing FAISS vector database.
    """

    return FAISS.load_local(
        folder_path,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def save_vectorstore(
    vectorstore,
    folder_path
):
    """
    Save the FAISS vector database.
    """

    vectorstore.save_local(folder_path)