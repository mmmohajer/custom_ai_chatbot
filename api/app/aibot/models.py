from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.db import Base
from app.config.models import BaseModelMixin


class KnowledgeBaseChunk(Base, BaseModelMixin):
    __tablename__ = "knowledge_base_chunks"

    chunk_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
        index=True
    )

    embedding = relationship(
        "KnowledgeBaseEmbedding",
        back_populates="chunk",
        uselist=False,
        cascade="all, delete-orphan"
    )


class KnowledgeBaseEmbedding(Base, BaseModelMixin):
    __tablename__ = "knowledge_base_embeddings"

    chunk_id: Mapped[int] = mapped_column(
        ForeignKey("knowledge_base_chunks.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(3072),
        nullable=False
    )

    chunk = relationship(
        "KnowledgeBaseChunk",
        back_populates="embedding"
    )