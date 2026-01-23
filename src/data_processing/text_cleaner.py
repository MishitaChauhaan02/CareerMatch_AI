import re
from pathlib import Path

PROCESSED_RESUME_DIR = Path("data/processed/resumes")

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[^a-z0-9\s\.\,\-\n]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_processed_resumes():
    """
    Cleans all processed resume text files using clean_text()
    """
    for file in PROCESSED_RESUME_DIR.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned_text = clean_text(raw_text)

        with open(file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"Cleaned: {file.name}")
