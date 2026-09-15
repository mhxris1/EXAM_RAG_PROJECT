import os

from google import genai
from google.genai import types
from typing import Optional
from pydantic import BaseModel, Field


HYDE_SYSTEM_PROMPT = """
You are an elite domain expert, technical writer, and master researcher. 
You possess deep, comprehensive knowledge across a wide range of subjects and write with absolute authority, precision, and clarity.

Read the user's query carefully and generate a definitive passage from an authoritative source document or technical manual that perfectly answers it. 
Naturally incorporate key technical terms, specific concepts, and contextual details.

Write strictly as a source document (no conversational filler). 
Output plain text only (no markdown, no preambles). Maximum 150 words.
"""

def hyDe(rewritten_query:str):

    final_prompt = f"{HYDE_SYSTEM_PROMPT}\n\n{rewritten_query}"

    client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents = final_prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=200
            )
    )

    print("hyDe response generated")
    return response.text.strip()
    