import json
from pathlib import Path
from src.RAG.llm_feedback_engine import generate_llm_feedback


RANKINGS_PATH = Path("outputs/rankings/job_rankings.json")
RESUME_DIR = Path("data/processed/resumes")
OUTPUT_PATH = Path("outputs/skill_gaps/resume_feedback.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_resume_text(resume_id):
    with open(RESUME_DIR / f"{resume_id}.txt", "r", encoding="utf-8") as f:
        return f.read()


def generate_resume_feedback():
    rankings = load_json(RANKINGS_PATH)
    jobs = load_json(Path("data/processed/job_descriptions.json"))

    job_lookup = {job["role"]: job for job in jobs}

    feedback_output = {}   

    TOP_K = 3

    for job_role, ranked_resumes in rankings.items():
        if job_role not in job_lookup:
            continue

        job = job_lookup[job_role]

        for item in ranked_resumes[:TOP_K]:
            resume_id = item["resume_id"]
            score = item["similarity_score"]
            
            print(f"Generating feedback for {resume_id} → {job_role}")

            resume_path = RESUME_DIR / f"{resume_id}.txt"
            resume_text = resume_path.read_text(encoding="utf-8")

            llm_feedback = generate_llm_feedback(
                resume_text=resume_text,
                job=job,
                similarity_score=score
            )

            if resume_id not in feedback_output:
                feedback_output[resume_id] = []

            feedback_output[resume_id].append({
                "job_role": job_role,
                "similarity_score": score,
                "ai_feedback": llm_feedback
            })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(feedback_output, f, indent=2)

    print("Feedback generated successfully.")

def generate_feedback_for_single_resume(
    resume_text: str,
    job: dict,
    similarity_score: float
):
    """
    Real-time feedback generation (used by FastAPI)
    """

    llm_feedback = generate_llm_feedback(
        resume_text=resume_text,
        job=job,
        similarity_score=similarity_score
    )

    return {
        "job_role": job["role"],
        "similarity_score": similarity_score,
        "ai_feedback": llm_feedback
    }



