# src/matching/matching_engine.py

import numpy as np
from src.feature_extraction.embedding_engine import generate_embedding
from src.skills.skill_matcher import skill_match_engine


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )


def evaluate_resume(resume_text: str, job_description: str):
    """
    Evaluates a SINGLE resume against a SINGLE job description.
    Returns structured matching data for AI feedback generation.
    """

    # 1️⃣ Generate embeddings
    job_embedding = generate_embedding(job_description)
    resume_embedding = generate_embedding(resume_text)

    # 2️⃣ Semantic similarity
    similarity_score = cosine_similarity(
        job_embedding, resume_embedding
    )

    similarity_score = round(float(similarity_score), 4)

    # 3️⃣ Skill matching
    skill_result = skill_match_engine(
        resume_text=resume_text,
        job_description=job_description
    )

    skill_match_percentage = round(
        skill_result["skill_match_percentage"], 2
    )

    # 4️⃣ Final response (NO ranking, NO DB)
    return {
        "similarity_score": similarity_score,
        "skill_match_percentage": skill_match_percentage,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"]
    }


# 🔹 Local test
if __name__ == "__main__":
    job_description = """
    Looking for an AI/ML Engineer skilled in Python, Machine Learning,
    Deep Learning, NLP, FastAPI, Docker, and AWS.
    """

    resume_text = """
    I have experience in Python, machine learning, deep learning,
    and building APIs using FastAPI.
    """

    result = evaluate_resume(resume_text, job_description)

    print("\n📄 RESUME EVALUATION REPORT\n")
    print(f"🧠 Similarity Score: {result['similarity_score']}")
    print(f"🛠 Skill Match: {result['skill_match_percentage']}%")
    print(f"✅ Matched Skills: {', '.join(result['matched_skills'])}")
    print(f"❌ Missing Skills: {', '.join(result['missing_skills'])}")
