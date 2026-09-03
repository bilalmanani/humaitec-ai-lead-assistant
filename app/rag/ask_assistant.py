from dotenv import load_dotenv
from google import genai
import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"

question = "What is HUMAITEC's exact office rent?"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

databasa=Chroma(
    persist_directory=str(CHROMA_DB_DIR),
    embedding_function=embeddings,
    collection_name="humaitec_knowledge"
)

results=databasa.similarity_search(question,k=3)


context = "\n\n".join(
    document.page_content for document in results
)

prompt = f"""
You are the HUMAITEC AI Lead Assistant.

Answer the client's question using ONLY the HUMAITEC context below.

Rules:
- Do not invent services, prices, promises, or company details.
- If the context does not contain the answer, say:
  "I do not have enough verified HUMAITEC information to answer that."
- Give a helpful, short answer.
- Ask one useful follow-up question.

HUMAITEC Context:
{context}

Client Question:
{question}
"""

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.interactions.create(
    model="gemini-3.8-flash",
    input=prompt,
)

print("\nClient Question:")
print(question)

print("\nAssistant Answer:")
print(response.output_text)

print("\nSources Used:")
for document in results:
    print("-", document.metadata["source"])