from chromadb import Embeddings
import time
import json

FLASHCARD_SYSTEM_PROMPT = """

You are an Expert Instructional Designer specializing in spacing algorithms, active recall, and Anki flashcard creation.

Task: Extract high-value flashcards from the provided text chunks.

Flashcard Rules:
1. Minimum Information Principle: Each card must test exactly ONE atomic concept, definition, keyword, or relationship.
2. Directness & Precision: Questions must be concise and targeted. Avoid broad or open-ended prompts.
3. Uniqueness: Avoid duplicate concepts across chunks.

Edge-Case Guidelines:
- If a section or metadata field (e.g., page_number) is missing, return null for that field.
- If a chunk lacks viable atomic facts, generate no cards for that chunk.

Output Format:
Output ONLY a raw JSON array matching this exact schema:
[
  {
    "question": "What is the primary function of the hippocampus in memory formation?",
    "answer": "Consolidating short-term memory into long-term memory",
    "section": "Neuroanatomy of Memory",
    "page_number": 12
  }
]

[BATCH_CHUNKS]

"""

def get_chunks(file_id: int):
    result = collection.get



