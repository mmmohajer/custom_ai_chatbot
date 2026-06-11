from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.aibot.models import KnowledgeBaseChunk
from app.aibot.schemas import (
    KnowledgeBaseChunkCreate,
    KnowledgeBaseChunkUpdate,
)
from app.aibot.utils.embedding_service import chunk_text
from app.aibot.schemas import ChatRequest
from app.aibot.utils.rag_service import answer_question_with_knowledge_base

def create_chunk(db: Session, data: KnowledgeBaseChunkCreate):
    chunks = chunk_text(data.chunk_text)

    saved_chunks = []

    for index, chunk in enumerate(chunks, start=1):
        db_chunk = KnowledgeBaseChunk(
            chunk_text=chunk,
            url=data.url,
        )

        db.add(db_chunk)
        saved_chunks.append(db_chunk)

    db.commit()

    for db_chunk in saved_chunks:
        db.refresh(db_chunk)

    return saved_chunks


def list_chunks(db: Session, page: int = 1, page_size: int = 10):
    offset = (page - 1) * page_size

    items = (
        db.query(KnowledgeBaseChunk)
        .order_by(KnowledgeBaseChunk.id)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total = db.query(KnowledgeBaseChunk).count()

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": items,
    }


def get_chunk(db: Session, chunk_id: int):
    chunk = (
        db.query(KnowledgeBaseChunk)
        .filter(KnowledgeBaseChunk.id == chunk_id)
        .first()
    )

    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found")

    return chunk


def update_chunk(db: Session, chunk_id: int, data: KnowledgeBaseChunkUpdate):
    chunk = get_chunk(db, chunk_id)

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(chunk, key, value)

    db.commit()
    db.refresh(chunk)

    return chunk


def delete_chunk(db: Session, chunk_id: int):
    chunk = get_chunk(db, chunk_id)

    db.delete(chunk)
    db.commit()

    return {"message": "Chunk deleted successfully"}

def chat(data: ChatRequest):
    return answer_question_with_knowledge_base(
        user_question=data.message,
        similarity_threshold=data.similarity_threshold,
        top_k=data.top_k,
    )