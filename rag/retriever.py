"""
retriever.py
-----------------------------------------
Retrieves relevant resume chunks.
"""


def retrieve_resume_context(
    vectorstore,
    query,
    k=4,
):
    """
    Retrieve top-k relevant resume chunks.
    """

    docs = vectorstore.similarity_search(
        query,
        k=k,
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return context