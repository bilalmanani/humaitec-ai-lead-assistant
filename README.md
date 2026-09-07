# HUMAITEC AI Lead & Knowledge Assistant

An AI-powered assistant that helps HUMAITEC understand client requirements, retrieve company information, recommend suitable services, qualify leads, and display lead data on an admin dashboard.

## Features

- HUMAITEC knowledge base using Markdown documents
- RAG pipeline with document loading, chunking, embeddings, and ChromaDB
- Semantic search for relevant HUMAITEC information
- Gemini-powered client assistant with grounded answers
- Hallucination prevention: the assistant does not invent unavailable company details
- Conversation memory for follow-up questions
- AI lead qualification
- Lead scoring: HOT, WARM, and COLD
- PostgreSQL database for qualified leads
- Streamlit lead dashboard with metrics, filters, charts, and lead details
- Day 6 testing report

## Technology Stack

- Python
- FastAPI
- LangChain
- ChromaDB
- Hugging Face Embeddings
- Google Gemini API
- PostgreSQL
- SQLAlchemy
- Streamlit
- Pydantic

## System Architecture

```mermaid
flowchart TD
    A[Client Question] --> B[RAG Retriever]
    B --> C[HUMAITEC Knowledge Base]
    C --> D[ChromaDB Vector Database]
    D --> E[Relevant Context]
    E --> F[Gemini AI Assistant]
    F --> G[Grounded Answer and Follow-up Question]

    F --> H[Lead Qualifier]
    H --> I[HOT / WARM / COLD Scoring]
    I --> J[PostgreSQL Leads Database]
    J --> K[Streamlit Dashboard]