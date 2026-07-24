from fastapi import FastAPI, UploadFile, File
import os
import shutil

from app.pdf_reader import extract_text_from_pdf
from app.chunker import chunk_text
from app.embeddings import generate_embeddings
from app.vector_store import store_embeddings
from app.retriever import retrieve_chunks
from app.reranker import rerank
from app.prompt_builder import build_prompt
from app.llm import ask_groq
from app.memory import (
    add_message,
    get_history,
    clear_history
)

app = FastAPI(
    title="Advanced PDF RAG Analyzer",
    version="1.0.0"
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =====================================================
# Root Endpoint
# =====================================================

@app.get("/")
def root():
    return {
        "message": "Advanced PDF RAG Analyzer Backend is Running!"
    }


# =====================================================
# Upload PDF
# =====================================================

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    # Save uploaded PDF

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read PDF

    extracted_text = extract_text_from_pdf(file_path)

    # Chunk Text

    chunks = chunk_text(extracted_text)

    # Generate Embeddings

    embeddings = generate_embeddings(chunks)

    # Store in ChromaDB

    store_embeddings(
        chunks,
        embeddings
    )

    return {

        "success": True,

        "filename": file.filename,

        "characters": len(extracted_text),

        "number_of_chunks": len(chunks),

        "embedding_dimension": len(embeddings[0]),

        "stored_in_database": True

    }


# =====================================================
# Search Endpoint
# =====================================================

@app.get("/search")
def search(question: str):

    # Previous Conversation

    history = get_history()

    # Retrieve Similar Chunks

    retrieved = retrieve_chunks(question)

    retrieved_chunks = retrieved["documents"][0]

    # Re-rank

    reranked = rerank(
        question,
        retrieved_chunks
    )

    # Extract only chunk text

    top_chunks = [
        chunk
        for chunk, score in reranked
    ]

    # Prompt Builder

    prompt = build_prompt(
        question,
        top_chunks,
        history
    )

    # Ask LLM

    answer = ask_groq(prompt)

    # Save Conversation

    add_message(
        "user",
        question
    )

    add_message(
        "assistant",
        answer
    )

    return {
        "answer": answer
    }


# =====================================================
# Clear Memory
# =====================================================

@app.post("/clear-memory")
def clear_memory():

    clear_history()

    return {
        "message": "Conversation Cleared Successfully."
    }