from src.data_processing.pdf_extractor import extract_all_resumes
from src.data_processing.text_cleaner import clean_processed_resumes
from src.data_processing.job_parser import parse_job_descriptions
from src.matching.embedding_matcher import match_resumes_to_jobs
from src.evaluation.ranking_and_skill_gap import generate_job_rankings
from src.RAG.resume_feedback_generator import generate_resume_feedback

RAW_RESUMES_DIR = "data/raw/resumes"
PROCESSED_RESUMES_DIR = "data/processed/resumes"
JOB_DESCRIPTIONS_PATH = "data/raw/job_descriptions/job_descriptions.txt"
RANKING_OUTPUT_PATH = "outputs/rankings/job_rankings.json"


def run_pipeline():
    extract_all_resumes(RAW_RESUMES_DIR, PROCESSED_RESUMES_DIR)
    clean_processed_resumes()
    print("Step 1 completed: Resume extraction and cleaning done.")

    parse_job_descriptions()
    print("Step 2 completed: Job descriptions parsed successfully.")

    similarity_results = match_resumes_to_jobs()
    print("Step 3 completed: Resume-job similarity computed.")

    generate_job_rankings(similarity_results, RANKING_OUTPUT_PATH)
    print("Step 4 completed: Rankings and skill gaps generated.")

    generate_resume_feedback()
    print("Step 5 completed: Resume feedback generated.")


if __name__ == "__main__":
    run_pipeline()
