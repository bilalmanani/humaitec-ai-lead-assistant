import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

from app.services.lead_scoring import calculate_lead_score


load_dotenv()


class LeadInfo(BaseModel):
    business: str
    requirement: str
    problem: str
    recommended_service: str
    timeline: str
    budget: str
    missing_information: list[str]
    follow_up_question: str


conversation = """
Client: I run an online clothing store.
Client: I want to automate customer support on WhatsApp.
Client: Customers mostly ask about order status and delivery.
Client: I want to start within one month.
"""

prompt = f"""
Extract lead information from this client conversation.

Rules:
- Use only information present in the conversation.
- Write "Unknown" if information is missing.
- Do not invent budget, business facts, or requirements.
- Recommended service must be one of:
  Web Development,
  Mobile App Development,
  Custom Software Development,
  AI Integration and Automation,
  Data Analytics and Business Intelligence,
  Cloud and DevOps.
- Ask only one useful follow-up question.

Conversation:
{conversation}
"""

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

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

print(json.dumps(lead_summary, indent=2))