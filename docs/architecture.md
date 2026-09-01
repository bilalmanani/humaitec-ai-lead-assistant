# HUMAITEC AI Lead & Knowledge Assistant Architecture

## Purpose

The system helps HUMAITEC answer client questions, understand business requirements, recommend appropriate services, qualify potential clients, and save lead summaries.

## System Flow

Client
↓
Streamlit Web Interface/React 
↓
FastAPI Backend
↓
Query Processing
↓
ChromaDB Vector Search
↓
Relevant HUMAITEC Knowledge Retrieved
↓
Gemini LLM
↓
AI Response + Lead Information Extraction
↓
PostgreSQL Database
↓
Admin Dashboard

## Components

### 1. Streamlit Web Interface

The client enters questions and project requirements through a simple chat interface.

### 2. FastAPI Backend

FastAPI receives client messages, calls the RAG pipeline, manages conversations, saves leads, and returns AI responses.

### 3. Knowledge Base

The knowledge base contains verified HUMAITEC information such as company overview, services, client problems, FAQs, and industries.

### 4. RAG Pipeline

The RAG pipeline converts HUMAITEC knowledge-base documents into embeddings and stores them in ChromaDB.

When a client asks a question, the system searches ChromaDB and retrieves relevant company information before asking Gemini to generate an answer.

### 5. Gemini LLM

Gemini generates a helpful, context-aware answer. It must use retrieved HUMAITEC information and clearly state when information is unavailable.

### 6. Lead Qualification

The system extracts:

- Business type
- Client requirement
- Business problem
- Recommended HUMAITEC service
- Timeline
- Budget
- Missing information
- Lead status: HOT, WARM, or COLD

### 7. PostgreSQL Database

PostgreSQL stores conversations, extracted lead information, lead summaries, status, and recommended next actions.

### 8. Admin Dashboard

The HUMAITEC team can view total leads, lead status, client requirements, recommended services, summaries, and next actions.