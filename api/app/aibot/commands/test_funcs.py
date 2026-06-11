from app.aibot.utils.retrieval_service import retrieve_similar_chunks
from app.aibot.utils.rag_service import answer_question_with_knowledge_base

def test_retrieval():
    chunks = retrieve_similar_chunks(
        user_message="What services do you offer?",
        similarity_threshold=0.3,
        top_k=5,
    )

    print(chunks)

def test_answer_question_with_knowledge_base():
    result = answer_question_with_knowledge_base(
        user_question="What services do you offer?",
        similarity_threshold=0.3,
        top_k=5,
    )

    print(result["answer"])
    # print(result["sources"])