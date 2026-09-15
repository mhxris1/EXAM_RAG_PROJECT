import os
import time

from google import genai
from google.genai import types


CHAT_SYSTEM_PROMPT="""
You are an expert tutor and study assistant designed to help users deeply understand their uploaded documents.

## TASK
Answer the user's query using ONLY the provided context chunks. 
Do not assume or extrapolate beyond the text. 
If the answer cannot be found in the context, state: "I cannot find this information in the provided documents."

## GUIDELINES
- Break down complex concepts simply.
- Use the Socratic method when appropriate to encourage critical thinking rather than just giving away answers.

## FORMAT
- **Direct Answer:** 1-2 concise sentences answering the core query.
- **Explanation:** A brief breakdown or summary of the key concepts from the context.
"""

def chat_response(rewritten_query:str,chunks):

    formatted_chunks = [res["text"] for res in chunks][:5]
    context= "\n".join(formatted_chunks)

    final_prompt= f"{CHAT_SYSTEM_PROMPT}\n\n{context}\n\n{rewritten_query}"

    client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents = final_prompt,
        config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
                )
        )

    print("response generated")

    return response.text.strip()
    
    
