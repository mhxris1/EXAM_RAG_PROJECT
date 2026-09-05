import os
from dotenv import load_dotenv
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer

#Load environment variables from the .env file
load_dotenv()

def chunk_document(doc):
    MAX_TOKENS = 1024
    HF_MODEL_ID = "google/gemma-3-4b-it"

    # Fetch token from environment
    hf_token = os.getenv("HF_TOKEN")

    # Fetch the Gemma tokenizer using the loaded token
    raw_tokenizer = AutoTokenizer.from_pretrained(
        HF_MODEL_ID,
        token=hf_token
    )

    #Gemini Tokeniser Wrapper
    docling_tokenizer = HuggingFaceTokenizer(
        tokenizer=raw_tokenizer,
        max_tokens=MAX_TOKENS
    )

    #Initialize HybridChunker
    chunker = HybridChunker(
        tokenizer=docling_tokenizer,
        max_tokens=MAX_TOKENS,
        merge_peers=True,
    )

    #Generate chunks
    chunks = list(chunker.chunk(dl_doc=doc))

    return chunks