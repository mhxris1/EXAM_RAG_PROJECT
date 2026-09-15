import os

from google import genai
from google.genai import types
from typing import Optional
from pydantic import BaseModel, Field

class AmbiguityCheck(BaseModel):
    is_ambiguous: bool = Field(
        description="True if the user's query is vague, missing critical context, or has multiple distinct interpretations. False if the query is clear enough to search a knowledge base."
    )
    clarifying_question: Optional[str] = Field(
        description="If is_ambiguous is True, write a short, polite clarifying question to ask the user. Leave empty if False."
    )

AMBIGUIT_CHECK_PROMPT = """
You are an expert query intent evaluator.
Determine if a user query is too vague, lacks critical context, or has multiple interpretations for a knowledge base search.
"""

def is_ambiguous(rewritten_prompt: str):

    client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents = rewritten_prompt,
        config=types.GenerateContentConfig(
            system_instruction=AMBIGUIT_CHECK_PROMPT,
            response_mime_type="application/json",
            response_schema=AmbiguityCheck,
            temperature=0.2,
        )
    )
    return response.parsed