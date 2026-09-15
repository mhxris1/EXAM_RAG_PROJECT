import chromadb
import chromadb.utils.embedding_functions as embedding_functions


#Use the same database initialised in embedder module
CHROMA_PATH = "/Users/muhxmmadharis/Desktop/Exam_Rag_Project/app/chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="RETRIEVAL_DOCUMENT", 
)

collection = chroma_client.get_or_create_collection(name="Embeddings", embedding_function=google_ef)


def dense_search(search):
    search_vector = google_ef([search])
    results = collection.query(
        query_embeddings=search_vector,
        n_results=10  #top k chunks
    )
    chunks_retrieved = results["documents"][0]
    return chunks_retrieved