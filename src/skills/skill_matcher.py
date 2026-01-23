# src/skills/skill_matcher.py

import re
from typing import List, Dict

# 🔹 Canonical skill list (expand anytime)
CANONICAL_SKILLS = [
    "python", "java", "c++", "sql",
    "machine learning", "deep learning",
    "natural language processing", "computer vision",
    "fastapi", "flask", "django",
    "pytorch", "tensorflow", "scikit-learn",
    "docker", "kubernetes",
    "aws", "gcp", "azure",
    "nlp", "ml", "dl", "cv"
]

# 🔹 Normalize aliases → canonical form
SKILL_ALIASES = {
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "sklearn": "scikit-learn",
    "tf": "tensorflow"
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text


def extract_skills(text: str) -> List[str]:
    text = normalize_text(text)
    found_skills = set()

    for skill in CANONICAL_SKILLS:
        if skill in text:
            found_skills.add(skill)

    # Normalize aliases
    normalized_skills = set()
    for skill in found_skills:
        if skill in SKILL_ALIASES:
            normalized_skills.add(SKILL_ALIASES[skill])
        else:
            normalized_skills.add(skill)

    return sorted(normalized_skills)


def skill_match_engine(resume_text: str, job_description: str) -> Dict:
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    matched_skills = sorted(resume_skills.intersection(job_skills))
    missing_skills = sorted(job_skills - resume_skills)

    match_percentage = (
        round((len(matched_skills) / len(job_skills)) * 100, 2)
        if job_skills else 0.0
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": match_percentage
    }


# ✅ Wrapper for matching_engine import
def match_skills(resume_text: str, job_description: str) -> Dict:
    return skill_match_engine(resume_text, job_description)


# 🧪 Local test
if __name__ == "__main__":
    resume = """
    Experienced AI Engineer skilled in Python, Machine Learning,
    Deep Learning, PyTorch, NLP, and FastAPI.
    """

    job = """
    Looking for an ML Engineer with Python, NLP,
    Docker, AWS, and FastAPI experience.
    """

    result = match_skills(resume, job)
    print(result)
