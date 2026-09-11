import os
import time
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from database import save_flashcards
from google import genai
from google.genai import types 
from pydantic import BaseModel, Field
from typing import List, Optional


#Use the same database initialised in embedder module
CHROMA_PATH = "/Users/muhxmmadharis/Desktop/Exam_Rag_Project/app/chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="RETRIEVAL_DOCUMENT", # Or RETRIEVAL_QUERY for querying
)



#Pydantic classes for flashcard blueprints
class Flashcard(BaseModel):
    question: str = Field(description="Direct, atomic question targeting ONE concept.")
    answer: str = Field(description="Concise, precise answer.")
    section: Optional[str] = Field(default=None, description="Section heading, or null if missing.")
    page_number: Optional[int] = Field(default=None, description="Page number, or null if missing.")

#Wrapper class to hold flashcards blueprint as we can't trust model to follow format instructions
class FlashcardBatch(BaseModel):
    cards: List[Flashcard]

FLASHCARD_SYSTEM_PROMPT = """
You are an Expert Instructional Designer specializing in spacing algorithms, active recall, and Anki flashcard creation.

Task: Extensively extract high-value flashcards from the provided batch of text chunks and their associated metadata. Ensure comprehensive coverage of all testable material.

Batch Processing Context:
You will receive up to 5 pairs of (text chunk, metadata). Process each pair systematically, mapping every generated card back to the exact metadata provided for that chunk.

Coverage & Thoroughness Rules:
1. Complete Exhaustion: Exhaustively identify every testable fact, term, mechanism, cause-and-effect relationship, sequence, and distinction in each chunk. Do not skip key details.
2. High Density: Aim for complete coverage—if a chunk contains multiple distinct facts, create as many individual cards as necessary to cover them all completely.
3. Quality Control: Omit card generation ONLY if a chunk is purely introductory fluff, boilerplate, or completely devoid of facts.

Flashcard Architecture Rules:
1. Minimum Information Principle: Each card must test exactly ONE atomic concept, definition, keyword, or relationship. If a concept has 3 key points, create 3 separate cards rather than 1 card with 3 answers.
2. Directness & Precision: Questions must be concise, specific, and targeted. Avoid vague or open-ended prompts (e.g., instead of "What is X?", ask "What is the primary function of X in process Y?").
3. Uniqueness: Avoid redundant or duplicate cards across chunks within or between batches.

Metadata Handling:
- Associate each card with the corresponding metadata object of the chunk it was derived from.
- Preserve missing/null metadata fields as null in the output.
"""

def get_chunks(file_id: int):

  collection = chroma_client.get_collection(
    name="Embeddings", 
    embedding_function=google_ef
  )
  results = collection.get(
      where={"file_id":int(file_id)},
      include=["documents", "metadatas"]
  )
  return results


def create_batches(file_id):

  results=get_chunks(file_id)

  max_batch = 5

  number_of_docs=len(results["ids"])

  batches=[]

  #Function to combine chunks of 5
  for i in range(0,number_of_docs,max_batch):
    docs=results["documents"][i:i+max_batch]
    metadatas=results["metadatas"][i:i+max_batch]

    #Taking above 5 docs and metadatas and combining them using zip
    docsxmetadata = zip(docs,metadatas)

    formatted_docsxmetadata=[]

    #Zip creates 2-item tuples so here we take the tuples one by one and format them into one string and add to a list
    for doc,meta in docsxmetadata:
      combine = f"{doc}\n{meta}"
      formatted_docsxmetadata.append(combine)

    #Here we join the 5 string created above into one string to create the batch of 5
    single_batch_string = "\n".join(formatted_docsxmetadata)

    #Here we add the batch to the master list
    batches.append(single_batch_string)

  return batches


def generate_flashcards(file_id):



  batches=create_batches(file_id)

  client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

  flashcards=[]

  for idx, single_batch in enumerate(batches):

    print(f"Processing batch {idx + 1} of {len(batches)}...")


    response = client.models.generate_content(
      model="gemini-3.1-flash-lite",
      contents = single_batch,
      #enforcing json formatting
      config=types.GenerateContentConfig(
                system_instruction=FLASHCARD_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=FlashcardBatch,
                temperature=0.2,
            )
    )

    #Validating format against Pydantic Schema
    parsed_batch = FlashcardBatch.model_validate_json(response.text)
    #Sequentially adding in flashcards to master list
    flashcards.extend(parsed_batch.cards)

    time.sleep(15)

    #Make flashcards list of dictionaries for json
    flashcard_dicts = [card.model_dump() for card in flashcards]

    save_flashcards(file_id, flashcard_dicts)

  print("flashcards saved")

  return flashcard_dicts









        






  

  



  








