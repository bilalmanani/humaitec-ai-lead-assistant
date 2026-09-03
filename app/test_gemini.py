from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain RAG in one simple sentence."
)

print(response.output_text)