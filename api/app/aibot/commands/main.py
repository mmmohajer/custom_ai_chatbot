import argparse

from app.aibot.commands.generate_missing_embeddings import (
    generate_missing_embeddings,
)
from app.aibot.commands.test_funcs import test_retrieval, test_answer_question_with_knowledge_base


def main():
    parser = argparse.ArgumentParser(
        description="Run app commands"
    )

    parser.add_argument(
        "command",
        choices=[
            "generate-missing-embeddings",
            "test-retrieval",
            "test-answer-question-with-knowledge-base",
        ],
    )

    args = parser.parse_args()

    if args.command == "generate-missing-embeddings":
        generate_missing_embeddings()

    elif args.command == "test-retrieval":
        test_retrieval()

    elif args.command == "test-answer-question-with-knowledge-base":
        test_answer_question_with_knowledge_base()


if __name__ == "__main__":
    main()