# src/matching/embedding_matcher.py

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

RESUME_DIR = Path("data/processed/resumes")
JOB_PATH = Path("data/processed/job_descriptions.json")
OUTPUT_PATH = Path("outputs/scores/resume_job_scores.json")


def load_resumes():
    resumes = []
    for file in RESUME_DIR.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            resumes.append({
                "resume_id": file.stem,
                "text": f.read()
            })
    return resumes


def load_jobs():
    with open(JOB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_job_text(job):
    return f"""
    Role: {job['role']}
    Level: {job['level']}
    Responsibilities: {' '.join(job['responsibilities'])}
    Required Skills: {' '.join(job['required_skills'])}
    Preferred Skills: {' '.join(job['preferred_skills'])}
    """


def match_resumes_to_jobs():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    resumes = load_resumes()
    jobs = load_jobs()

    resume_texts = [r["text"] for r in resumes]
    job_texts = [build_job_text(j) for j in jobs]

    resume_embeddings = model.encode(resume_texts)
    job_embeddings = model.encode(job_texts)

    similarity_matrix = cosine_similarity(resume_embeddings, job_embeddings)

    results = []

    for i, resume in enumerate(resumes):
        for j, job in enumerate(jobs):
            results.append({
                "resume_id": resume["resume_id"],
                "job_role": job["role"],
                "job_level": job["level"],
                "similarity_score": round(float(similarity_matrix[i][j]), 4)
            })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("Resume and Job matching completed using embeddings.")

    return results
