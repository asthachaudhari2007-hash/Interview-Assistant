from rag.pdf_loader import load_resume
from rag.chunking import chunk_documents
from rag.vector_store import create_vectorstore
from rag.retriever import retrieve_resume_context

# Load Resume
documents = load_resume("uploads/resume.pdf")

# Chunk Resume
chunks = chunk_documents(documents)

# Create Vector DB
vector_db = create_vectorstore(
    chunks,
    model_name="Gemini"
)

# Query
query = "Tell me about the candidate's projects."

context = retrieve_resume_context(
    vector_db,
    query,
)

print("=" * 80)
print(context)