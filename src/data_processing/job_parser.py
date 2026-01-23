# src/data_processing/job_parser.py

import json
from pathlib import Path

RAW_JD_PATH = Path("data/raw/job_descriptions/job_descriptions.txt")
PROCESSED_JD_PATH = Path("data/processed/job_descriptions.json")


def parse_job_descriptions():
    with open(RAW_JD_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    # Split job descriptions (assuming ROLE starts each JD)
    raw_jobs = content.split("ROLE:")

    jobs = []

    for job in raw_jobs:
        if not job.strip():
            continue

        job_data = {
            "role": "",
            "level": "",
            "responsibilities": [],
            "required_skills": [],
            "preferred_skills": []
        }

        lines = job.strip().split("\n")
        section = None

        for line in lines:
            line = line.strip()

            if line.startswith("LEVEL:"):
                job_data["level"] = line.replace("LEVEL:", "").strip()

            elif line.startswith("RESPONSIBILITIES:"):
                section = "responsibilities"

            elif line.startswith("REQUIRED SKILLS:"):
                section = "required_skills"

            elif line.startswith("PREFERRED SKILLS:"):
                section = "preferred_skills"

            elif line.startswith("-") and section:
                job_data[section].append(line.replace("-", "").strip())

            elif not job_data["role"]:
                job_data["role"] = line.strip()

        jobs.append(job_data)

    PROCESSED_JD_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(PROCESSED_JD_PATH, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    print(f"Parsed {len(jobs)} job descriptions successfully.")
    return jobs

if __name__ == "__main__":
    parse_job_descriptions()
