import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import time


#Create database instance
CHROMA_PATH = "/Users/muhxmmadharis/Desktop/Exam_Rag_Project/app/chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

batch_size=2
delay=3

#Gemini Embedding function wrapper
google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="RETRIEVAL_DOCUMENT",
)

def embed_chunks(chunks: list,file_id: int):

    #Create the schema
    collection = chroma_client.get_or_create_collection(name="Embeddings", embedding_function=google_ef)

    #Extract text from chunks
    document_text = [chunk.text for chunk in chunks]

    #Create list of id's using list comprehension
    list_of_ids = [f"{file_id}_chunk_{i}" for i, _ in enumerate(chunks, start=1)]

    #Create Metadata schema
    metadatas = []

    for i, chunk in enumerate(chunks, start=1):
    #Get headings
        headings_list = getattr(chunk.meta, "headings", [])
        heading_str = " > ".join(headings_list) if headings_list else "N/A"

    #Get pagenumber
        page_number = None
        doc_items = getattr(chunk.meta, "doc_items", [])

    #Check if doc_items isn't empty, if it has a prov attribute and then if the prov contains data
        if doc_items and hasattr(doc_items[0], "prov") and doc_items[0].prov:
            page_number = doc_items[0].prov[0].page_no

        #create dictionary
        metadatas.append({
        "file_id": file_id, # Passed into your function
        "chunk_index": i, # Current index from enumerate
        "page_number": page_number or 1, # Extracted page (or default fallback)
        "heading": heading_str # Formatted heading string
        })

    total_chunks = len(chunks)
    for i in range(0, total_chunks, batch_size):
        batch_docs = document_text[i:i + batch_size]
        batch_ids = list_of_ids[i:i + batch_size]
        batch_metadatas = metadatas[i:i + batch_size]

        collection.add(
            documents=batch_docs,
            ids=batch_ids,
            metadatas=batch_metadatas
        )
        
        # Pause briefly to prevent exceeding Gemini's Requests Per Minute (RPM) threshold
        if i + batch_size < total_chunks:
            time.sleep(delay)

