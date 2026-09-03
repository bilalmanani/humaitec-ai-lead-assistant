import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

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

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_assistant(question, history):
    results = database.similarity_search(question, k=3)

    context = "\n\n".join(
        document.page_content for document in results
    )

    previous_messages = "\n".join(history[-6:])

    prompt = f"""
You are the HUMAITEC AI Lead Assistant.

Use ONLY the HUMAITEC context below.
Use the conversation history to understand the client's previous answers.

Rules:
- Do not invent services, prices, or company details.
- If the answer is unavailable, say:
  "I do not have enough verified HUMAITEC information to answer that."
- Give a helpful, short answer.
- Ask only one useful follow-up question.

Conversation History:
{previous_messages}

HUMAITEC Context:
{context}

Client's New Message:
{question}
"""

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
    )

    answer = response.output_text

    history.append(f"Client: {question}")
    history.append(f"Assistant: {answer}")

    return answer, results


history = []

print("HUMAITEC AI Assistant started.")
print("Type 'exit' to close the chat.")

while True:
    question = input("\nClient: ").strip()

    if question.lower() == "exit":
        print("Chat closed.")
        break

    if not question:
        continue

    answer, results = ask_assistant(question, history)

    print("\nAssistant:", answer)
    print("\nSources:")
    for document in results:
        print("-", document.metadata["source"])