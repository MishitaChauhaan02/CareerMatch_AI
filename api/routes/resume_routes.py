from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pypdf import PdfReader

from src.matching.matching_engine import evaluate_resume
from src.RAG.llm_feedback_engine import generate_llm_feedback

router = APIRouter()


def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        reader = PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid PDF file")


@router.post("/analyze-resume")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported")

    # 1️⃣ Extract resume text
    resume_text = extract_text_from_pdf(resume)

    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from resume")

    # 2️⃣ Resume ↔ Job evaluation
    evaluation = evaluate_resume(
        resume_text=resume_text,
        job_description=job_description
    )

    # 3️⃣ AI feedback & suggestions
    ai_feedback = generate_llm_feedback(
        resume_text=resume_text,
        job_description=job_description,
        similarity_score=evaluation["similarity_score"],
        matched_skills=evaluation["matched_skills"],
        missing_skills=evaluation["missing_skills"]
    )

    # 4️⃣ Final response
    return {
        "similarity_score": evaluation["similarity_score"],
        "skill_match_percentage": evaluation["skill_match_percentage"],
        "matched_skills": evaluation["matched_skills"],
        "missing_skills": evaluation["missing_skills"],
        "ai_feedback": ai_feedback
    }
