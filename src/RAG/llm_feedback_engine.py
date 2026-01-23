import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_llm_feedback(
    resume_text: str,
    job_description: str,
    similarity_score: float,
    matched_skills: list,
    missing_skills: list
):
    """
    Generates AI feedback and improvement suggestions
    for a SINGLE resume vs SINGLE job description.
    """

    prompt = f"""
You are an expert AI career coach and hiring manager.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

MATCH ANALYSIS:
- Semantic Similarity Score: {similarity_score}
- Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}
- Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}

TASK:
1. Briefly explain why the resume matches or does not match the job.
2. Clearly point out skill gaps or weaknesses.
3. Give 5–7 concrete, actionable suggestions to improve the resume.
4. Suggest what skills, tools, or projects the candidate should focus on next.

RULES:
- Be honest but encouraging
- Use bullet points for suggestions
- Do NOT repeat the resume text
- Do NOT mention scores explicitly in the suggestions
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional AI hiring assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()
