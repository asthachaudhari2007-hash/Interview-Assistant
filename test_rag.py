from rag.pdf_loader import load_resume
from rag.chunking import chunk_documents

docs = load_resume("resume.pdf")

chunks = chunk_documents(docs)

print("Pages:", len(docs))
print("Chunks:", len(chunks))

print(chunks[0].page_content)