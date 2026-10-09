import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please add it to your .env file."
    )

# Create Gemini client
client = genai.Client(api_key=api_key)


def analyze_resume(resume_text: str, job_description: str):
    """
    Analyze a resume against a job description using Gemini AI.
    """

    prompt = f"""
You are an expert ATS (Applicant Tracking System) and recruitment assistant.

Analyze the following resume against the given job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON in exactly this structure:

{{
    "ats_score": 85,
    "matching_skills": ["Python", "FastAPI"],
    "missing_skills": ["Docker"],
    "strengths": [
        "Good Python knowledge",
        "Strong backend development skills"
    ],
    "weaknesses": [
        "No Docker experience"
    ],
    "recommendation": "Recommended for interview"
}}

Rules:
- ats_score must be an integer between 0 and 100.
- matching_skills must contain skills found in both the resume and job description.
- missing_skills must contain important skills from the job description that are missing from the resume.
- strengths should be based on the resume.
- weaknesses should identify relevant gaps.
- recommendation should be one of:
  "Highly Recommended for interview",
  "Recommended for interview",
  "Consider with caution",
  "Not Recommended"
- Return ONLY JSON.
- Do not use Markdown.
- Do not include ```json or ``` in the response.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result_text = response.text.strip()

        # Remove Markdown code fences if Gemini accidentally adds them
        if result_text.startswith("```json"):
            result_text = result_text[7:]

        if result_text.startswith("```"):
            result_text = result_text[3:]

        if result_text.endswith("```"):
            result_text = result_text[:-3]

        result_text = result_text.strip()

        # Convert Gemini response to Python dictionary
        result = json.loads(result_text)

        return result

    except json.JSONDecodeError:
        return {
            "ats_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "recommendation": "Unable to analyze resume",
            "error": "Gemini returned an invalid JSON response."
        }

    except Exception as e:
        return {
            "ats_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "recommendation": "Unable to analyze resume",
            "error": str(e)
        }