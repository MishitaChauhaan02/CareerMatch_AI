# src/feature_extraction/skill_extractor.py

import re

# Core skill taxonomy (expand later)
SKILL_SET = {
    # Programming
    "python", "c", "c++", "java", "sql", "javascript",

    # ML / AI
    "machine learning", "deep learning", "artificial intelligence",
    "nlp", "computer vision", "data science",

    # Frameworks
    "tensorflow", "pytorch", "scikit-learn", "keras",

    # Backend / Dev
    "fastapi", "flask", "django", "docker", "kubernetes",

    # Databases / Cloud
    "mysql", "postgresql", "mongodb", "aws", "gcp", "azure"
}

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def extract_skills(text: str):
    text = clean_text(text)

    matched_skills = set()

    for skill in SKILL_SET:
        if skill in text:
            matched_skills.add(skill)

    return sorted(matched_skills)

if __name__ == "__main__":
    sample_resume = """
    AI/ML Engineer skilled in Python, TensorFlow, PyTorch,
    NLP, Computer Vision, FastAPI, Docker, and AWS.
    """

    skills = extract_skills(sample_resume)
    print("Extracted Skills:", skills)
