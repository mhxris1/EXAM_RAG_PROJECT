import os
import time
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from google import genai
from google.genai import types 

#Use the same database initialised in embedder module
CHROMA_PATH = "/Users/muhxmmadharis/Desktop/Exam_Rag_Project/app/chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="RETRIEVAL_DOCUMENT", # Or RETRIEVAL_QUERY for querying
)




