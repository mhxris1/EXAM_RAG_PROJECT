# EXAM_RAG_PROJECT

Document RAG & Intelligence Engine
A modular Python backend that turns complex PDFs into searchable, context-aware data using Google's Gemini, Pydantic, and Docling.
How It Works

[ Upload PDF ] ──> [ Parse & Extract Images ] ──> [ Check Query Intent ] ──> [ RAG Generation ]

Upload & Parse: Reads documents entirely in memory (saving disk space) and extracts text and figures.
Intent Check: Uses structured data validation to catch unclear questions before searching databases.
Generate Response: Combines the extracted document context with Gemini to deliver precise, type-safe answers.

Key Features

In-Memory Processing: Streams PDF bytes directly (io.BytesIO) to keep things fast and lightweight.
Layout-Aware Parsing (docling): Handles complex document structures and extracts embedded images.
Type-Safe Validation (pydantic): Enforces strict JSON schemas to ensure reliable, error-free LLM responses.
Modular Codebase: Cleanly separates parsing, intent checking, and generation into independent files.

Tech Stack
Language: Python
AI / LLM: Google GenAI SDK (gemini-2.5-flash)
Validation: Pydantic V2
Parsing: Docling & RapidOCR
Storage: SQLite
