from app.core.embeddings import EmbeddingGenerator
from app.core.vector_store import VectorStore
from app.core.llm import OllamaLLM
from typing import List, Dict

class RAGChain:
    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        vector_store: VectorStore,
        llm: OllamaLLM
    ):
        self.embedding_generator = embedding_generator
        self.vector_store = vector_store
        self.llm = llm
    
    def ingest_documents(self, documents: List[Dict]):
        """Ingest documents into vector store"""
        texts = [doc["text"] for doc in documents]
        metadata = [doc["metadata"] for doc in documents]
        
        # Generate embeddings
        embeddings = self.embedding_generator.generate(texts)
        
        # Store in vector database
        self.vector_store.add_documents(texts, embeddings, metadata)
        
        return {"status": "success", "documents_ingested": len(documents)}
    
    def query(self, question: str, top_k: int = 5) -> Dict:
        """Query the RAG system"""
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_single(question)
        
        # Retrieve relevant documents
        search_results = self.vector_store.search(
            query_embedding,
            limit=top_k,
            score_threshold=0.6
        )
        
        # Format context from retrieved documents
        context_parts = []
        sources = []
        
        for result in search_results:
            context_parts.append(result.payload["text"])
            sources.append({
                "source": result.payload.get("source", "unknown"),
                "score": result.score,
                "chunk_index": result.payload.get("chunk_index", 0)
            })
        
        context = "\n\n".join(context_parts)
        
        # Generate answer using LLM
        if not context:
            answer = "I don't have any relevant information to answer this question."
        else:
            answer = self.llm.generate(question, context)
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "context_used": len(search_results)
        }
