import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_embedding(text: str):
    if not text or not isinstance(text, str):
        raise ValueError("Text for embedding must be a non-empty string")

    text = text.strip()

    if len(text) == 0:
        raise ValueError("Text for embedding cannot be empty")

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

