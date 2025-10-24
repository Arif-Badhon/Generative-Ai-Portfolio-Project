from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5

class SourceInfo(BaseModel):
    source: str
    score: float
    chunk_index: int

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceInfo]
    context_used: int

class IngestResponse(BaseModel):
    status: str
    documents_ingested: int
    message: Optional[str] = None
