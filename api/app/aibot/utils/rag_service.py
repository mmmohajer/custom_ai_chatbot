from app.aibot.utils.retrieval_service import retrieve_similar_chunks
from app.ai.openai_client import OpenAIClient


openai_client = OpenAIClient()


SYSTEM_MESSAGE = """
You are a helpful AI assistant.

You will receive:
1. A user question
2. Retrieved context from relevant website pages

Your job is to carefully analyze the retrieved context and answer the user's question if the answer can be reasonably understood from that context.

Do not mention the knowledge base, retrieved chunks, embeddings, or context.

Do not say "based on the knowledge base."

If the context contains enough information to answer directly, answer naturally and confidently.

If the context contains related information but not the exact answer, explain what is available and what is not clear.

Only say "I don't know." if the retrieved context gives no useful information for the question.

Do not make up prices, dates, policies, or facts that are not supported by the context.
Keep the answer concise and helpful.
"""


def answer_question_with_knowledge_base(
    user_question: str,
    similarity_threshold: float = 0.3,
    top_k: int = 5,
) -> dict:
    chunks = retrieve_similar_chunks(
        user_message=user_question,
        similarity_threshold=similarity_threshold,
        top_k=top_k,
    )

    context = "\n\n".join(
        [
            f"Source: {chunk['url']}\nContent: {chunk['chunk_text']}"
            for chunk in chunks
        ]
    )

    user_message = f"""
User question:
{user_question}

Knowledge base context:
{context}
"""

    answer = openai_client.generate_response(
        system_message=SYSTEM_MESSAGE,
        user_message=user_message,
    )

    return {
        "question": user_question,
        "answer": answer,
        "sources": [
            {
                "id": chunk["id"],
                "url": chunk["url"],
                "similarity": chunk["similarity"],
            }
            for chunk in chunks
        ],
    }