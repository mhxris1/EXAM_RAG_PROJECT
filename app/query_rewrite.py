import os

from google import genai
from google.genai import types
from database import get_chat_history 

SYSTEM_PROMPT = """
Act as a precise search query optimizer. 
Transform conversational user inputs into standalone, information-dense search queries using available chat history up to the last 5 turns. 
Resolve all pronouns, implicit references, and contextual gaps so the query is entirely self-contained. Optimize for zero-temperature generation by prioritizing direct entity naming and high keyword density. 
If the chat history is empty, new, or lacks context, output the raw user input verbatim. Output strictly the final query as a single plaintext sentence with no markdown, quotes, filler, or introductory text.
"""

def rewrite_query(chat_id: int,prompt:str):
    chat_history = get_chat_history(chat_id)

    if chat_history:

        formatted_history = '\n'.join([f"{msg['sender']}: {msg['content']}" for msg in chat_history])
        formatted_prompt = f"{formatted_history}\n{prompt}"
    else:
        formatted_prompt=f"User: {prompt}"

    final_prompt=f"{SYSTEM_PROMPT}\n{formatted_prompt}"

    client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=final_prompt,
        config=types.GenerateContentConfig(
            temperature=0.0,          #Zero randomness stay ont rack with convo
            max_output_tokens=100,    #Keep it brief 
        )
    )
    print("query rewritten")

    return response.text.strip()