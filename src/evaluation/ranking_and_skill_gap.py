import json
import os
from collections import defaultdict

def generate_job_rankings(similarity_results, output_path, top_k=3):
    """
    similarity_results: list of dicts with
    resume_id, job_role, job_level, similarity_score
    """

    # Step 1: Store best score per resume per job
    job_resume_map = defaultdict(dict)

    for result in similarity_results:
        job_key = f"{result['job_role']} ({result['job_level']})"
        resume_id = result["resume_id"]
        score = result["similarity_score"]

        # Keep only the highest score per resume
        if resume_id not in job_resume_map[job_key]:
            job_resume_map[job_key][resume_id] = result
        else:
            if score > job_resume_map[job_key][resume_id]["similarity_score"]:
                job_resume_map[job_key][resume_id] = result

    # Step 2: Rank resumes per job
    final_rankings = {}

    for job_key, resumes in job_resume_map.items():
        sorted_resumes = sorted(
            resumes.values(),
            key=lambda x: x["similarity_score"],
            reverse=True
        )

        final_rankings[job_key] = sorted_resumes[:top_k]

    # Step 3: Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(final_rankings, f, indent=2)

    print("completed: Rankings and skill gap analysis generated.")

