from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.aibot.schemas import (
    KnowledgeBaseChunkCreate,
    KnowledgeBaseChunkUpdate,
    KnowledgeBaseChunkResponse,
    PaginatedKnowledgeBaseChunkResponse,
    ChatRequest,
    ChatResponse
)
from app.aibot import service


router = APIRouter(
    prefix="/knowledge-base",
    tags=["Knowledge Base"],
)


@router.post("/", response_model=list[KnowledgeBaseChunkResponse])
def create_chunk(
    data: KnowledgeBaseChunkCreate,
    db: Session = Depends(get_db),
):
    return service.create_chunk(db, data)


@router.get("/", response_model=PaginatedKnowledgeBaseChunkResponse)
def list_chunks(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.list_chunks(db, page, page_size)


@router.get("/{chunk_id}/", response_model=KnowledgeBaseChunkResponse)
def get_chunk(
    chunk_id: int,
    db: Session = Depends(get_db),
):
    return service.get_chunk(db, chunk_id)


@router.patch("/{chunk_id}/", response_model=KnowledgeBaseChunkResponse)
def update_chunk(
    chunk_id: int,
    data: KnowledgeBaseChunkUpdate,
    db: Session = Depends(get_db),
):
    return service.update_chunk(db, chunk_id, data)


@router.delete("/{chunk_id}/")
def delete_chunk(
    chunk_id: int,
    db: Session = Depends(get_db),
):
    return service.delete_chunk(db, chunk_id)

@router.post("/chat/", response_model=ChatResponse)
def chat(data: ChatRequest):
    return service.chat(data)