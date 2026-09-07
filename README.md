# HUMAITEC AI Lead & Knowledge Assistant

An AI-powered prototype that helps HUMAITEC understand client requirements, retrieve company information, recommend suitable services, qualify leads, and display lead data on an admin dashboard.

## Project Objective

The system uses Retrieval-Augmented Generation (RAG) to answer client questions using the HUMAITEC knowledge base. It also extracts lead details, recommends services, asks follow-up questions, assigns a HOT/WARM/COLD lead status, and displays leads in a PostgreSQL-powered dashboard.

## Features

* HUMAITEC knowledge base using Markdown documents
* RAG pipeline with document loading, chunking, embeddings, and ChromaDB
* Semantic search for relevant HUMAITEC information
* Gemini-powered client assistant with grounded answers
* Hallucination prevention for unavailable company information
* Conversation memory for natural follow-up questions
* AI lead qualification
* Lead scoring: HOT, WARM, and COLD
* PostgreSQL database for lead records
* Streamlit dashboard with metrics, filters, charts, and lead details
* Client scenario and hallucination testing report

## Technology Stack

* Python
* FastAPI
* LangChain
* ChromaDB
* Hugging Face Embeddings
* Google Gemini API
* PostgreSQL
* SQLAlchemy
* Streamlit
* Pydantic

## System Architecture

```mermaid
flowchart TD
    A[Client Question] --> B[RAG Retriever]
    B --> C[HUMAITEC Knowledge Base]
    C --> D[ChromaDB Vector Database]
    D --> E[Relevant Context]
    E --> F[Gemini AI Assistant]
    F --> G[Grounded Answer and Follow-up]

    F --> H[Lead Qualifier]
    H --> I[HOT WARM COLD Scoring]
    I --> J[PostgreSQL Database]
    J --> K[Streamlit Dashboard]
```

## How RAG Works

1. HUMAITEC documents are stored in the `knowledge_base` folder.
2. The ingestion script splits documents into smaller chunks.
3. Chunks are converted into embeddings using `all-MiniLM-L6-v2`.
4. ChromaDB stores the embeddings locally.
5. When a client asks a question, the system retrieves relevant chunks.
6. Gemini receives only the retrieved context and generates a grounded response.
7. If the required information is unavailable, the assistant says it does not have enough verified HUMAITEC information.

## Lead Qualification

The lead qualifier extracts:

* Business type
* Client requirement
* Client problem
* Recommended service
* Timeline
* Budget
* Missing information
* Follow-up question
* Lead status
* Score reason

### Lead Status Rules

| Status | Meaning                                                             |
| ------ | ------------------------------------------------------------------- |
| HOT    | Client has a clear requirement, timeline, and budget                |
| WARM   | Client has a clear requirement but important information is missing |
| COLD   | Client has a general inquiry or unclear requirement                 |

## Project Structure

```text
humaitec-ai-lead-assistant/
├── app/
│   ├── database/
│   │   ├── leads_db.py
│   │   └── seed_leads.py
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── retriever.py
│   │   ├── ask_assistant.py
│   │   └── chat_memory.py
│   ├── services/
│   │   ├── lead_qualifier.py
│   │   └── lead_scoring.py
│   ├── main.py
│   └── test_gemini.py
├── data/
│   └── chroma_db/
├── docs/
│   └── architecture.md
├── knowledge_base/
├── tests/
│   ├── client_scenarios.md
│   └── testing_report.md
├── dashboard.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/bilalmanani/humaitec-ai-lead-assistant.git
cd humaitec-ai-lead-assistant
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/humaitec_leads_db
```

Never upload the `.env` file to GitHub.

## Run the Project

### Start FastAPI

```bash
uvicorn app.main:app --reload
```

Open API documentation:

```text
http://127.0.0.1:8000/docs
```

### Build the ChromaDB vector database

```bash
python -m app.rag.ingest
```

### Test document retrieval

```bash
python -m app.rag.retriever
```

### Ask the RAG assistant

```bash
python -m app.rag.ask_assistant
```

### Start conversation memory demo

```bash
python -m app.rag.chat_memory
```

### Test lead qualification and scoring

```bash
python -m app.services.lead_qualifier
python -m app.services.lead_scoring
```

### Create PostgreSQL tables and demo leads

```bash
python -m app.database.leads_db
python -m app.database.seed_leads
```

### Start the Streamlit dashboard

```bash
streamlit run dashboard.py
```

Open:

```text
http://localhost:8501
```

## Testing

The project includes:

* HUMAITEC client scenarios
* Hallucination prevention tests
* RAG retrieval tests
* Service recommendation tests
* Lead scoring tests

See [tests/testing_report.md](tests/testing_report.md) for Day 6 testing results.

## Known Limitation

The Gemini free API tier can temporarily return a `429` rate-limit error during frequent requests. The application can be retried after the quota window resets.

## Future Scope

* Connect the assistant to a FastAPI chat endpoint
* Automatically save qualified chat leads to PostgreSQL
* Integrate with the HUMAITEC website
* Add WhatsApp integration
* Add CRM integration
* Improve dashboard analytics

## Author

Bilal Ahmad
Generative AI Internship Project for HUMAITEC
