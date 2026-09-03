from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

database = Chroma(
    persist_directory=str(CHROMA_DB_DIR),
    embedding_function=embeddings,
    collection_name="humaitec_knowledge",
)

question = "I need a system to manage students, fees, and attendance"

results = database.similarity_search(question, k=3)

print("\nQuestion:", question)

for document in results:
    print("\nSource:", document.metadata["source"])
    print("Content:", document.page_content)