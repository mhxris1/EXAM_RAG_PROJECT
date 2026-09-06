import chromadb
import chromadb.utils.embedding_functions as embedding_functions



#Create database instance
chroma_client = chromadb.Client()


#Gemini Embedding function wrapper
google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="RETRIEVAL_DOCUMENT",
)

def embed_chunks(chunks: list,file_id: int):

    #reset database everytime for testing
    try:
        chroma_client.delete_collection(name="Embeddings")
    except Exception:
        pass # Collection didn't exist yet, safe to ignore

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


    collection.add(
    documents = document_text,
    ids= list_of_ids,
    metadatas=metadatas
    )

