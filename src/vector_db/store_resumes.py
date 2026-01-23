# src/vector_db/store_resumes.py

from pathlib import Path
from src.vector_db.chroma_store import get_collection
from src.feature_extraction.embedding_engine import generate_embedding

RESUME_DIR = Path("data/processed/resumes")

def store_resumes():
    collection = get_collection("resumes")

    resume_files = list(RESUME_DIR.glob("*.txt"))

    if not resume_files:
        print("No resumes found to store.")
        return

    for resume_file in resume_files:
        resume_id = resume_file.stem
        resume_text = resume_file.read_text(encoding="utf-8")

        embedding = generate_embedding(resume_text)

        collection.add(
            documents=[resume_text],
            embeddings=[embedding],
            ids=[resume_id],
            metadatas=[{"resume_id": resume_id}]
        )

        print(f"Stored resume: {resume_id}")

    print(f"\nStored {len(resume_files)} resumes in ChromaDB")


if __name__ == "__main__":
    store_resumes()
