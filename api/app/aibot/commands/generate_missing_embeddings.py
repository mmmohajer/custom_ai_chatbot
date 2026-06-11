from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.aibot.models import (
    KnowledgeBaseChunk,
    KnowledgeBaseEmbedding,
)
from app.aibot.utils.embedding_service import generate_embedding


def generate_missing_embeddings():
    db: Session = SessionLocal()

    try:
        chunks = (
            db.query(KnowledgeBaseChunk)
            .outerjoin(KnowledgeBaseEmbedding)
            .filter(KnowledgeBaseEmbedding.id.is_(None))
            .order_by(KnowledgeBaseChunk.id)
            .all()
        )

        total_chunks = len(chunks)

        print(f"Found {total_chunks} chunks without embeddings.")

        created_count = 0

        for index, chunk in enumerate(chunks, start=1):
            if not chunk.chunk_text:
                continue

            print(
                f"[{index}/{total_chunks}] "
                f"Generating embedding for chunk_id={chunk.id}"
            )

            embedding_vector = generate_embedding(chunk.chunk_text)

            embedding = KnowledgeBaseEmbedding(
                chunk_id=chunk.id,
                embedding=embedding_vector,
            )

            db.add(embedding)

            created_count += 1

            print(
                f"[{index}/{total_chunks}] "
                f"Created embedding for chunk_id={chunk.id}"
            )

        db.commit()

        print(f"Created {created_count} embeddings.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()