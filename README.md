#  Advanced PDF RAG Analyzer

An end-to-end Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask natural language questions about their contents.

The application extracts text from uploaded PDFs, converts the text into embeddings, stores them in a vector database, retrieves the most relevant information for a user's question, and uses an LLM to generate an answer.

---

# Features

- Upload one or multiple PDF documents
- Ask questions about uploaded PDFs
- Semantic search using vector embeddings
- Cross Encoder reranking for better retrieval
- Conversation memory for follow-up questions
- Streamlit-based chat interface
- FastAPI backend
- Modular project structure

---

# Tech Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| PDF Processing | PyMuPDF |
| Chunking | Custom Chunker |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| Retrieval | Semantic Search |
| Reranking | Cross Encoder (ms-marco-MiniLM-L-6-v2) |
| LLM | Groq (Llama 3.3) |
| Language | Python |

---

# Project Architecture

```
                         USER
                           │
                           ▼
                    Streamlit UI
                           │
                           ▼
                     FastAPI API
                           │
                           ▼

=====================================================
                 PDF INDEXING PIPELINE
=====================================================

Upload PDF
      │
      ▼
PyMuPDF
      │
Extract Text
      │
      ▼
Custom Chunker
      │
Split into Chunks
      │
      ▼
SentenceTransformer
      │
Generate Embeddings
      │
      ▼
ChromaDB
Store:
• Chunk Text
• Embeddings

=====================================================
              QUESTION ANSWERING PIPELINE
=====================================================

User Question
      │
      ▼
SentenceTransformer
Question Embedding
      │
      ▼
ChromaDB
Semantic Search
      │
Retrieve Top 5 Chunks
      │
      ▼
Cross Encoder
Reranking
      │
Top 3 Chunks
      │
      ▼
Prompt Builder

Prompt contains:
• Conversation History
• Retrieved Chunks
• Current Question

      │
      ▼
Groq Llama 3.3
      │
Generate Answer
      │
      ▼
Streamlit UI
```

---

# Workflow

## 1. Upload PDF

The user uploads one or more PDF documents using the Streamlit interface.

The PDFs are sent to the FastAPI backend and saved on the server.

---

## 2. Text Extraction

PyMuPDF extracts the text from each uploaded PDF.

---

## 3. Chunking

The extracted text is divided into smaller chunks using a custom chunking function.

Chunking makes retrieval more accurate and keeps the context manageable.

---

## 4. Embedding Generation

Each chunk is converted into a dense vector embedding using the SentenceTransformer model:

```
all-MiniLM-L6-v2
```

These embeddings capture the semantic meaning of each chunk.

---

## 5. Vector Storage

Each embedding, along with its corresponding chunk text, is stored in ChromaDB.

---

## 6. Question Processing

When the user asks a question:

- The question is converted into an embedding using the same SentenceTransformer model.
- ChromaDB performs semantic search.
- The five most relevant chunks are retrieved.

---

## 7. Reranking

A Cross Encoder model reranks the retrieved chunks and selects the most relevant ones.

---

## 8. Prompt Construction

The prompt is built using:

- Conversation history
- Retrieved chunks
- Current user question

---

## 9. Answer Generation

The prompt is sent to Groq's Llama 3.3 model, which generates the final answer.

The answer is returned to the Streamlit chat interface.

---

# Folder Structure

```
advanced_pdf_rag/

│

├── app/
│   ├── main.py
│   ├── pdf_reader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── reranker.py
│   ├── prompt_builder.py
│   ├── llm.py
│   └── memory.py
│

├── frontend/
│   └── streamlit_app.py
│

├── uploads/

├── chroma_db/

├── requirements.txt

├── .env

└── README.md
```

---

# Author

Developed as a learning project to understand:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Embeddings
- Reranking
- Prompt Engineering
- FastAPI
- Streamlit