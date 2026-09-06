from pdf_parser import parse_pdf_and_store_images
from chunker import chunk_document
from embedder import embed_chunks

def process_document_pipeline(file_id: int, file_bytes: bytes, filename: str):
    """
    Master pipeline:
    1. Parse PDF & extract figures to DB
    2. Structurally chunk document with HybridChunker
    """
    # Convert PDF and extract binary assets to SQLite
    doc = parse_pdf_and_store_images(file_id, file_bytes, filename)
    
    #Generate layout-aware chunks
    chunks = chunk_document(doc)

    embed_chunks(chunks,file_id)

    print(f"Processed {len(chunks)} chunks for file_id: {file_id}")

    return {
        "status": "success",
        "file_id": file_id,
        "chunk_count": len(chunks),
        "chunks": chunks
    }