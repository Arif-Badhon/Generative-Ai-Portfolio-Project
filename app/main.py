from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.core.embeddings import EmbeddingGenerator
from app.core.vector_store import VectorStore
from app.core.llm import OllamaLLM
from app.services.document_processor import DocumentProcessor
from app.services.rag_chain import RAGChain
from app.models.schemas import QueryRequest, QueryResponse, IngestResponse
import tempfile
import os

# Initialize FastAPI app
app = FastAPI(
    title="RAG Portfolio Project",
    description="Production-grade Retrieval-Augmented Generation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
settings = get_settings()

embedding_generator = EmbeddingGenerator(settings.embedding_model)
vector_store = VectorStore(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
    collection_name=settings.qdrant_collection_name,
    vector_size=embedding_generator.dimension
)
llm = OllamaLLM(settings.ollama_base_url, settings.ollama_model)
document_processor = DocumentProcessor()

rag_chain = RAGChain(embedding_generator, vector_store, llm)

@app.get("/")
async def root():
    return {
        "message": "RAG Portfolio Project API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ollama_connected": True}

@app.post("/ingest/file", response_model=IngestResponse)
async def ingest_file(file: UploadFile = File(...)):
    """Upload and ingest a document into the RAG system"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Process document
        chunks = document_processor.process_document(tmp_path)
        
        # Ingest into RAG system
        result = rag_chain.ingest_documents(chunks)
        
        # Clean up
        os.unlink(tmp_path)
        
        return IngestResponse(**result, message=f"Successfully ingested {file.filename}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the RAG system"""
    try:
        result = rag_chain.query(request.question, request.top_k)
        return QueryResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reset")
async def reset_collection():
    """Reset the vector collection (delete all documents)"""
    try:
        vector_store.client.delete_collection(settings.qdrant_collection_name)
        vector_store._ensure_collection()
        return {"status": "success", "message": "Collection reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
