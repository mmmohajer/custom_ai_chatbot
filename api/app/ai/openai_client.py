import os

from openai import OpenAI


class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPEN_AI_KEY")

        if not self.api_key:
            raise RuntimeError("OPEN_AI_KEY is not set")

        self.client = OpenAI(
            api_key=self.api_key
        )

    def generate_embedding(
        self,
        text: str,
        model: str = "text-embedding-3-large",
    ) -> list[float]:
        response = self.client.embeddings.create(
            model=model,
            input=text,
        )

        return response.data[0].embedding
    
    def generate_response(
        self,
        system_message: str,
        user_message: str,
        model: str = "gpt-4o",
    ) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        return response.choices[0].message.content