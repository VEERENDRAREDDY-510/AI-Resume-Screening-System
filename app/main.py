import os

from fastapi import FastAPI, UploadFile, File, Form

from app.ai_service import analyze_resume
from app.resume_parser import extract_text


app = FastAPI(
    title="AI Resume Screening API",
    description="API for AI-powered resume screening and candidate ranking",
    version="1.0.0"
)


# Create uploads folder automatically
os.makedirs("uploads", exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "AI Resume Screening API is running"
    }


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Check that the uploaded file is a PDF
    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported."
        }

    # Save uploaded resume
    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from resume
    resume_text = extract_text(file_path)

    # Check whether text was extracted
    if not resume_text.strip():
        return {
            "error": "Could not extract text from the uploaded PDF."
        }

    # Analyze resume using Gemini
    result = analyze_resume(
        resume_text,
        job_description
    )

    return result