from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict
import uuid

class VectorStore:
    def __init__(self, host: str, port: int, collection_name: str, vector_size: int):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
        except Exception as e:
            print(f"Warning: Could not connect to Qdrant: {e}")
    
    def add_documents(self, texts: List[str], embeddings: List[List[float]], 
                     metadata: List[Dict] = None):
        """Add documents to vector store"""
        points = []
        for idx, (text, embedding) in enumerate(zip(texts, embeddings)):
            point_id = str(uuid.uuid4())
            payload = {"text": text}
            if metadata and idx < len(metadata):
                payload.update(metadata[idx])
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search(self, query_embedding: List[float], limit: int = 5, 
              score_threshold: float = 0.7):
        """Search for similar documents"""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold
            )
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
