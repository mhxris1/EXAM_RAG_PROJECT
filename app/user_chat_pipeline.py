import os
import time
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from google import genai
from google.genai import types

from app.ambiguity_check import is_ambiguous 
from app.database import save_chat_message
from app.hyDe import hyDe
from app.query_rewrite import rewrite_query



#Use the same database initialised in embedder module
CHROMA_PATH = "/Users/muhxmmadharis/Desktop/Exam_Rag_Project/app/chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="RETRIEVAL_DOCUMENT", 
)

def chat(chat_id):

    while True:
        prompt = input("")
        save_chat_message(chat_id,"user",prompt)
        rewritten_query=rewrite_query(chat_id,prompt)
        ambiguity=is_ambiguous(rewritten_query)

        if ambiguity.is_ambiguous:
            question = ambiguity.clarifying_question
            save_chat_message(chat_id,"system",question)
            return {
            "response": question,
            "requires_clarification": True,
            "chat_id": chat_id
            }

        else:
            search=hyDe(rewritten_query)
            
