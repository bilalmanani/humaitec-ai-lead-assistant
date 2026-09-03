from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"


def load_knowledge_base():
    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.md"):
        loader = TextLoader(str(file_path), encoding="utf-8")
        loaded_documents = loader.load()

        for document in loaded_documents:
            document.metadata["source"] = file_path.name

        documents.extend(loaded_documents)

    return documents


def create_vector_database():
    documents = load_knowledge_base()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )

    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR),
        collection_name="humaitec_knowledge",
    )

    print(f"Knowledge-base files loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print("ChromaDB vector database created successfully.")


if __name__ == "__main__":
    create_vector_database()