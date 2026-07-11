"""
pdf_loader.py
-----------------------------
Loads PDF documents using LangChain.
"""

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    """
    Load a PDF file and return LangChain Documents.
    """

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    return documents