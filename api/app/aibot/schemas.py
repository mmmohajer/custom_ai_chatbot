from datetime import datetime
from pydantic import BaseModel


class KnowledgeBaseChunkCreate(BaseModel):
    chunk_text: str
    url: str


class KnowledgeBaseChunkUpdate(BaseModel):
    chunk_text: str | None = None
    url: str | None = None


class KnowledgeBaseChunkResponse(BaseModel):
    id: int
    chunk_text: str
    url: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class PaginatedKnowledgeBaseChunkResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[KnowledgeBaseChunkResponse]

class ChatRequest(BaseModel):
    message: str
    similarity_threshold: float = 0.3
    top_k: int = 5


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[dict]