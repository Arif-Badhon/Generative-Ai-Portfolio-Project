RAG Portfolio Project
A state-of-the-art Retrieval-Augmented Generation (RAG) system leveraging modern generative AI and vector search technologies. This project demonstrates how to build a production-grade system that enables advanced question answering, document search, and contextual generation on your own infrastructure—private, scalable, and fast.

Table of Contents
Project Overview

Features

Tech Stack

Getting Started

Architecture

API Endpoints

Usage Examples

Testing

Project Structure

Troubleshooting

Contributing

License

Project Overview
This project showcases how to combine large language models (LLMs), local vector databases, and a modern Python web API for secure, high-performance knowledge and document retrieval. All LLM operations run locally—no data leaves your machine.
It is ideal for applications in internal research, enterprise QA, knowledge management, or compliance-sensitive AI tasks.

Features
Local LLM Inference: Runs entirely on your machine using Ollama and open-source models (e.g., Llama 3.1).

Vector Database Search: Uses Qdrant for fast, scalable semantic retrieval.

Flexible Document Ingestion: Upload PDF, DOCX, or TXT files for indexing and search.

FastAPI Back End: High-concurrency, type-safe REST API with automatic docs.

Modern Python Package Management: Built with uv for blazing-fast dependency resolution.

Modular, Extensible Codebase: Clean architecture, easy to extend/maintain.

Privacy and Security: No cloud calls—ideal for regulated sectors.

Fully Containerizable: Easily deploy with Docker.

Tech Stack
LLM: Ollama (local inference engine), Llama 3.1

Vector DB: Qdrant

Embeddings: Sentence Transformers

API: FastAPI + Uvicorn

Package Manager: uv

Code Editor: Cursor (recommended)

Testing & Quality: Pytest, Black, Ruff

DevOps: Docker-ready

Getting Started
1. Prerequisites
Python 3.10+

uv package manager

Ollama installed locally

Qdrant (Docker recommended)

2. Setup

# Clone the repository
git clone https://github.com/YOUR_USERNAME/rag-portfolio-project.git
cd rag-portfolio-project

# Install dependencies
uv sync

# Copy and configure environment variables
cp .env.example .env
# (Update .env if needed)


3. Start Qdrant (Vector DB)

docker run -p 6333:6333 qdrant/qdrant

4. Pull Ollama LLM Model

ollama pull llama3.1


5. Run the FastAPI Application

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

6. Open API Documentation
Access interactive docs at:
http://localhost:8000/docs


Architecture

                ┌────────────┐
                │   User     │
                └─────┬──────┘
                      │
               ┌──────▼───────┐
               │ FastAPI REST │
               │   Backend    │
               └─────┬────────┘
         ┌────────────┴────────────┐
         │                        │
 ┌───────▼─────┐        ┌─────────▼────────┐
 │ Document    │        │ Query, RAG Chain │
 │ Ingestion   │        │   & Generation   │
 └───────┬─────┘        └──────────────────┘
         │
 ┌───────▼────────┐
 │ Embedding      │
 │ Generation     │
 └───────┬────────┘
         │
 ┌───────▼─────────┐
 │ Qdrant Vector   │
 │ Database (DB)   │
 └───────┬─────────┘
         │
 ┌───────▼─────────┐
 │ Ollama LLM      │
 └─────────────────┘

Document Ingestion: Split files into semantic chunks and index as vectors.

Embedding Generation: Semantic vectors via Sentence Transformers.

Vector Search: Qdrant returns most relevant contexts for input queries.

Generative Augmentation: Ollama answers using retrieved context (true RAG).

API Endpoints

Method  |  Path          |  Description                    
--------+----------------+---------------------------------
GET     |  /             |  Root endpoint                  
GET     |  /health       |  Check system status            
POST    |  /ingest/file  |  Upload and index document      
POST    |  /query        |  Query system for answer        
DELETE  |  /reset        |  Reset vector database (danger!)

Automated docs: http://localhost:8000/docs

Usage Examples
1. Upload a Document (.pdf/.docx/.txt):
curl -X POST "http://localhost:8000/ingest/file" \
     -H "accept: application/json" \
     -F "file=@your_document.pdf"

2. Query the System:
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the key insight in the uploaded document?", "top_k": 5}'

3. Reset Collection:
curl -X DELETE "http://localhost:8000/reset"


Testing
Unit tests provided in /tests using Pytest.

Run all tests:
uv run pytest

Ensure code quality:
uv run black app/ tests/
uv run ruff app/ tests/


Project Structure
rag-portfolio-project/
├── .env                          # Environment config
├── pyproject.toml                # Dependencies config
├── README.md                     # This documentation
├── app/
│   ├── main.py                   # FastAPI app
│   ├── config.py                 # Config loader
│   ├── models/                   # Pydantic schemas
│   ├── core/                     # LLM, embeddings, vector DB
│   ├── services/                 # Document ingestion, RAG chain
│   └── api/                      # API routes and dependencies
├── data/
│   ├── documents/                # Raw document storage
│   └── processed/                # Chunked files
├── tests/
│   └── test_rag.py               # Unit tests
└── scripts/
    ├── setup_qdrant.py           # DB utils
    └── ingest_documents.py       # Bulk ingest


Troubleshooting
Missing Modules?
Run uv add <module-name> for any missing Python packages.

Ollama Model Not Found?
Double-check model name with ollama list and update .env.

Qdrant Not Running?
Ensure container is up (docker ps).

File Upload Errors?
Check you have python-multipart installed.

Contributing
Contributions are welcome! Please fork the repository, open issues, or submit pull requests for bug fixes, docs improvements, or new features.

License
Open-source under the MIT License.

Questions?
Contact the repository owner or open an issue – happy to help!