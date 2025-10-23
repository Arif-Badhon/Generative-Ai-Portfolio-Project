# RAG Portfolio Project

A state-of-the-art Retrieval-Augmented Generation (RAG) system leveraging modern generative AI and vector search technologies. This project demonstrates how to build a production-grade system that enables advanced question answering, document search, and contextual generation on your own infrastructure—private, scalable, and fast.

---

## Table of Contents
- Project Overview
- Features
- Tech Stack
- Getting Started
- Architecture
- API Endpoints
- Usage Examples
- Testing
- Project Structure
- Troubleshooting
- Contributing
- License

---

## Project Overview
This project showcases how to combine large language models (LLMs), local vector databases, and a modern Python web API for secure, high-performance knowledge and document retrieval. All LLM operations run locally—no data leaves your machine.

Ideal for applications in internal research, enterprise QA, knowledge management, or compliance-sensitive AI tasks.

---

## Features
- **Local LLM Inference:** Runs entirely on your machine using Ollama and open-source models (e.g., Llama 3.1).
- **Vector Database Search:** Uses Qdrant for fast, scalable semantic retrieval.
- **Flexible Document Ingestion:** Upload PDF, DOCX, or TXT files for indexing and search.
- **FastAPI Back End:** High-concurrency, type-safe REST API with automatic documentation.
- **Modern Python Package Management:** Built with `uv` for blazing-fast dependency resolution.
- **Modular, Extensible Codebase:** Clean architecture, easy to extend and maintain.
- **Privacy and Security:** No cloud calls—ideal for regulated sectors.
- **Fully Containerizable:** Easily deploy with Docker.

---

## Tech Stack
- **LLM:** Ollama (local inference engine), Llama 3.1
- **Vector DB:** Qdrant
- **Embeddings:** Sentence Transformers
- **API:** FastAPI + Uvicorn
- **Package Manager:** uv
- **Code Editor:** Cursor (recommended)
- **Testing & Quality:** Pytest, Black, Ruff
- **DevOps:** Docker-ready

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- `uv` package manager
- Ollama installed locally
- Qdrant (Docker recommended)

### 2. Setup
git clone https://github.com/YOUR_USERNAME/rag-portfolio-project.git
cd rag-portfolio-project
uv sync
cp .env.example .env

(Update .env if needed)

### 3. Start Qdrant (Vector DB)

docker run -p 6333:6333 qdrant/qdrant

text

### 4. Pull Ollama LLM Model
ollama pull llama3.1

text

### 5. Run the FastAPI Application
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

text

### 6. Open API Documentation
Access at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Architecture
text
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
┌───▼─────┐ ┌───────▼────────┐
│ Document │ │ Query, RAG │
│ Ingestion│ │ Chain & Gen. │
└───┬──────┘ └────────────────┘
│
┌───▼────────┐
│ Embedding │
│ Generation │
└───┬────────┘
│
┌───▼─────────┐
│ Qdrant │
│ Vector DB │
└───┬─────────┘
│
┌───▼─────────┐
│ Ollama LLM │
└─────────────┘

text

**Workflow:**
- Documents are split into semantic chunks and indexed as vectors.
- Sentence Transformers generate embeddings.
- Qdrant retrieves the most relevant contexts.
- Ollama answers using retrieved context (true RAG).

---

## API Endpoints
| Method | Path           | Description                       |
|--------|----------------|-----------------------------------|
| GET    | `/`            | Root endpoint                     |
| GET    | `/health`      | Check system status               |
| POST   | `/ingest/file` | Upload and index document         |
| POST   | `/query`       | Query system for answer           |
| DELETE | `/reset`       | Reset vector database (danger!)   |

Docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Usage Examples
1. Upload a Document (.pdf/.docx/.txt)
curl -X POST "http://localhost:8000/ingest/file"
-H "accept: application/json"
-F "file=@your_document.pdf"

2. Query the System
curl -X POST "http://localhost:8000/query"
-H "Content-Type: application/json"
-d '{"question": "What is the key insight in the uploaded document?", "top_k": 5}'

3. Reset Collection
curl -X DELETE "http://localhost:8000/reset"

text

---

## Testing
- Unit tests in `/tests` using Pytest.
- Run all tests:
uv run pytest

text
- Ensure formatting and linting:
uv run black app/ tests/
uv run ruff app/ tests/

text

---

## Project Structure
rag-portfolio-project/
├── .env
├── pyproject.toml
├── README.md
├── app/
│ ├── main.py
│ ├── config.py
│ ├── models/
│ ├── core/
│ ├── services/
│ └── api/
├── data/
│ ├── documents/
│ └── processed/
├── tests/
│ └── test_rag.py
└── scripts/
├── setup_qdrant.py
└── ingest_documents.py

text

---

## Troubleshooting
- **Missing Modules?** Run `uv add <module-name>`
- **Ollama Model Not Found?** Check with `ollama list` or update `.env`
- **Qdrant Not Running?** Ensure the Docker container is up (`docker ps`)
- **File Upload Errors?** Install `python-multipart`

---

## Contributing
Contributions are welcome! Fork the repo, open issues, or submit pull requests for enhancements or bug fixes.

---

## License
Open-source under the MIT License.

---

## Questions?
Contact the repository owner or open an issue – happy to help!