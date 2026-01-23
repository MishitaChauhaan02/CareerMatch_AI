import pdfplumber
from pathlib import Path

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()


def extract_all_resumes(raw_dir: str, processed_dir: str):
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)

    processed_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file in raw_dir.glob("*.pdf"):
        text = extract_text_from_pdf(pdf_file)

        output_file = processed_dir / f"{pdf_file.stem}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Extracted: {pdf_file.name} → {output_file.name}")
