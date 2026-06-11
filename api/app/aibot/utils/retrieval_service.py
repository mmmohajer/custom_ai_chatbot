from sqlalchemy import text

from app.db import SessionLocal
from app.aibot.utils.embedding_service import generate_embedding


def retrieve_similar_chunks(
    user_message: str,
    similarity_threshold: float = 0.75,
    top_k: int = 5,
) -> list[dict]:
    db = SessionLocal()

    try:
        query_embedding = generate_embedding(user_message)

        query_embedding_str = (
            "[" + ",".join(map(str, query_embedding)) + "]"
        )

        sql = text("""
            SELECT
                c.id,
                c.chunk_text,
                c.url,
                1 - (
                    e.embedding <=> CAST(:query_embedding AS vector)
                ) AS similarity
            FROM knowledge_base_chunks c
            JOIN knowledge_base_embeddings e
                ON e.chunk_id = c.id
            WHERE
                1 - (
                    e.embedding <=> CAST(:query_embedding AS vector)
                ) >= :similarity_threshold
            ORDER BY
                e.embedding <=> CAST(:query_embedding AS vector)
            LIMIT :top_k
        """)

        results = db.execute(
            sql,
            {
                "query_embedding": query_embedding_str,
                "similarity_threshold": similarity_threshold,
                "top_k": top_k,
            },
        ).mappings().all()

        return [dict(row) for row in results]

    finally:
        db.close()