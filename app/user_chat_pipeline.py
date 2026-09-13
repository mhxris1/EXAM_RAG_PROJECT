import os
import time
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from google import genai
from google.genai import types

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
        rewritten_query=rewrite_query(chat_id,prompt)
        

        
            







