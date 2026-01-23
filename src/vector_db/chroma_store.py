import chromadb
from chromadb.config import Settings

CHROMA_PATH = "chroma_db"

_client = None


def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_PATH,
            settings=Settings(
                anonymized_telemetry=False
            )
        )
    return _client


def get_collection(name: str):
    client = get_client()
    return client.get_or_create_collection(name)
