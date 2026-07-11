from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents,
    chunk_size=800,
    chunk_overlap=150,
):
    """
    Split documents into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(documents)

    return chunks