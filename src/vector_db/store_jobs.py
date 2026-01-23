# src/vector_db/store_jobs.py

from src.vector_db.chroma_store import get_collection
from src.data_processing.job_parser import parse_job_descriptions
from src.feature_extraction.embedding_engine import generate_embedding

def store_jobs():
    collection = get_collection("jobs")

    jobs = parse_job_descriptions()  # now returns list

    for idx, job in enumerate(jobs):
        job_text = f"""
        Role: {job['role']}
        Level: {job['level']}
        Responsibilities: {' '.join(job['responsibilities'])}
        Required Skills: {' '.join(job['required_skills'])}
        Preferred Skills: {' '.join(job['preferred_skills'])}
        """

        embedding = generate_embedding(job_text)

        collection.add(
            documents=[job_text],
            embeddings=[embedding],
            ids=[f"job_{idx}"],
            metadatas=[{
                "role": job["role"],
                "level": job["level"],
                "required_skills": ", ".join(job["required_skills"]),
                "preferred_skills": ", ".join(job["preferred_skills"])
            }]
        )

    print(f"Stored {len(jobs)} job descriptions in ChromaDB")


if __name__ == "__main__":
    store_jobs()
