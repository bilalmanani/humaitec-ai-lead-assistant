from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.rag.chat_memory import ask_assistant
from app.services.lead_qualifier import LeadInfo
from app.services.lead_scoring import calculate_lead_score
from app.database.leads_db import SessionLocal, Lead
import os
from google import genai
from google.genai import types

app = FastAPI(title="HUMAITEC AI Lead & Knowledge Assistant")


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[str]] = []


class QualifyRequest(BaseModel):
    conversation: str


@app.get("/")
def home():
    return {"message": "HUMAITEC AI Lead & Knowledge Assistant is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    answer, results = ask_assistant(req.message, req.history)
    sources = [doc.metadata.get("source", "Unknown") for doc in results] if results else []
    return {
        "answer": answer,
        "history": req.history,
        "sources": sources
    }


@app.post("/qualify")
def qualify_endpoint(req: QualifyRequest):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"""
Extract lead information from this client conversation.

Rules:
- Use only information present in the conversation.
- Write "Unknown" if information is missing.
- Do not invent budget, business facts, or requirements.
- Recommended service must be one of:
  Web Development, Mobile App Development, Custom Software Development,
  AI Integration and Automation, Data Analytics and Business Intelligence, Cloud and DevOps.
- Ask only one useful follow-up question.

Conversation:
{req.conversation}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LeadInfo,
            ),
        )
        lead = LeadInfo.model_validate_json(response.text)
        score = calculate_lead_score(
            requirement=lead.requirement,
            timeline=lead.timeline,
            budget=lead.budget,
        )
        lead_summary = lead.model_dump()
        lead_summary["lead_status"] = score["status"]
        lead_summary["score_reason"] = score["reason"]
        
        # Save to database if client has requirement
        if lead.business != "Unknown" or lead.requirement != "Unknown":
            session = SessionLocal()
            db_lead = Lead(
                business=lead.business if lead.business != "Unknown" else "Inquiring Client",
                requirement=lead.requirement,
                recommended_service=lead.recommended_service,
                timeline=lead.timeline,
                budget=lead.budget,
                lead_status=score["status"],
                summary=lead.problem if lead.problem != "Unknown" else lead.requirement,
                next_action=lead.follow_up_question
            )
            session.add(db_lead)
            session.commit()
            session.close()

        return lead_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leads")
def get_leads_endpoint():
    session = SessionLocal()
    leads = session.query(Lead).order_by(Lead.created_at.desc()).all()
    session.close()
    return [
        {
            "id": lead.id,
            "business": lead.business,
            "requirement": lead.requirement,
            "recommended_service": lead.recommended_service,
            "timeline": lead.timeline,
            "budget": lead.budget,
            "lead_status": lead.lead_status,
            "summary": lead.summary,
            "next_action": lead.next_action,
            "created_at": lead.created_at.isoformat() if lead.created_at else None,
        }
        for lead in leads
    ]