from app.ai.openai_client import OpenAIClient

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap_percent: float = 0.2,
) -> list[str]:
    """
    Split text into fixed-size chunks with overlap.

    Each chunk contains `chunk_size` new characters plus an additional
    overlap region shared with the next chunk.

    Example:
        chunk_size = 1000
        overlap_percent = 0.2

        overlap_size = 200

        Chunk 1: text[0:1200]
        Chunk 2: text[1000:2200]
        Chunk 3: text[2000:3200]

    This approach helps preserve context across chunk boundaries,
    making it useful for RAG pipelines, embeddings, semantic search,
    and LLM-based retrieval systems.

    Args:
        text: Input text to split into chunks.
        chunk_size: Number of new characters introduced by each chunk.
        overlap_percent: Percentage of chunk_size to overlap with the
            following chunk (e.g. 0.2 = 20%).

    Returns:
        A list of text chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if not 0 <= overlap_percent < 1:
        raise ValueError("overlap_percent must be between 0 and 1")

    overlap_size = int(chunk_size * overlap_percent)

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size + overlap_size

        chunks.append(text[start:end])

        start += chunk_size

    return chunks

def generate_embedding(text: str) -> list[float]:
    """
    Generate a vector embedding for the provided text.

    Returns:
        A list of 3072 floats compatible with Vector(3072).
    """
    openai_client = OpenAIClient()
    return openai_client.generate_embedding(text)