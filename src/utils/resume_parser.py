import pdfplumber
import docx
from fastapi import UploadFile


def extract_text_from_pdf(file: UploadFile) -> str:
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_text_from_docx(file: UploadFile) -> str:
    document = docx.Document(file.file)
    return "\n".join([para.text for para in document.paragraphs])


def extract_resume_text(file: UploadFile) -> str:
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)

    else:
        raise ValueError("Unsupported file type. Upload PDF or DOCX only.")
