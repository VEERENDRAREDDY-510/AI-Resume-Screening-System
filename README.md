# AI Resume Screening & Candidate Ranking System

An AI-powered resume screening application that analyzes resumes against job descriptions and helps recruiters evaluate candidate suitability using Gemini AI.

## Overview

The **AI Resume Screening System** is a Python-based project designed to simplify the initial resume screening process. It extracts information from resumes, compares candidate profiles with job requirements, and generates AI-assisted insights to support recruitment decisions.

The project aims to reduce manual screening effort and provide a structured way to evaluate candidate skills and qualifications.

## Features

* **Resume Upload:** Upload resumes for analysis.
* **Resume Text Extraction:** Extract text from supported resume documents.
* **AI-Powered Analysis:** Use Google's Gemini AI to analyze resume content against a job description.
* **ATS-Style Matching Score:** Generate a score to indicate how closely a resume matches the specified requirements.
* **Skill Gap Identification:** Highlight relevant matching skills and potentially missing skills.
* **Candidate Insights:** Present strengths, weaknesses, and interview recommendations when returned by the AI service.
* **Interactive Web Interface:** Use Streamlit for a user-friendly experience.
* **API Integration:** Use FastAPI to handle resume analysis requests.

## Technologies Used

| Technology       | Purpose                                          |
| ---------------- | ------------------------------------------------ |
| Python           | Core programming language                        |
| FastAPI          | Backend API                                      |
| Streamlit        | Interactive user interface                       |
| Google Gemini AI | AI-powered resume analysis                       |
| Pandas           | Data manipulation, if used in the implementation |
| PyPDF            | PDF text extraction, if configured               |
| OCR / Tesseract  | Scanned document text extraction, if configured  |
| Git and GitHub   | Version control and project hosting              |

## Project Structure

```text
Resume-Screening-AI/
├── app/
│   ├── main.py
│   ├── ai_service.py
│   └── resume_parser.py
├── uploads/
├── streamlit_app.py
├── .gitignore
├── .env.example
└── README.md
```

*Note: The structure above represents the main expected files. Update it to match the actual files in your repository.*

## How It Works

1. The user uploads a resume through the application.
2. The system extracts readable text from the resume.
3. The user provides a job description.
4. The backend sends the resume text and job description to the AI analysis service.
5. The AI evaluates relevant skills, qualifications, strengths, and potential gaps.
6. The application displays the analysis results to the user.

## Installation and Setup

### Prerequisites

* Python 3.12 or another Python version supported by your installed dependencies
* Git
* A Google Gemini API key
* Internet access for the AI API

### 1. Clone the repository

```bash
git clone https://github.com/VEERENDRAREDDY-510/AI-Resume-Screening-System.git
cd AI-Resume-Screening-System
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If your project contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the packages required by your implementation. For example:

```bash
pip install fastapi uvicorn streamlit requests python-dotenv google-generativeai pypdf python-multipart
```

Additional packages may be needed for OCR, image processing, or other functionality.

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key.

**Security:** Never commit your `.env` file or expose your API key publicly. Keep `.env` in `.gitignore`.

### 5. Start the FastAPI backend

```bash
python -m uvicorn app.main:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

Explore the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Streamlit application

Open another terminal, activate the same virtual environment, and run:

```bash
streamlit run streamlit_app.py
```

Open the local URL displayed in the terminal.

*The commands and dependency list may need adjustments to match the current implementation.*

## Example Use Case

**Job Role:** Data Analyst

**Job Description:** Looking for a candidate with Python, SQL, Excel, data visualization, and analytical skills.

The user uploads a resume and submits the job description. The system analyzes the available resume content and presents a matching score, relevant skills, potential skill gaps, and other AI-generated observations.

*AI-generated scores and recommendations are estimates, not validated hiring decisions.*

## Future Enhancements

* Improve support for scanned PDF resumes through OCR.
* Add structured candidate comparison and ranking.
* Support batch processing of multiple resumes.
* Improve the accuracy and consistency of skill matching.
* Add downloadable candidate analysis reports.
* Add data validation, error handling, and automated tests.
* Improve accessibility and user interface design.

## Limitations

* Analysis quality depends on the readability and completeness of the resume.
* AI-generated scores may be inconsistent and should not be treated as objective measures of candidate quality.
* Resume analysis should support, not replace, human review.
* Personal information should be handled securely and only retained when necessary.

## Responsible Use

This project is intended as a learning and recruitment-support tool. Recruiters should review AI-generated outputs and avoid making hiring decisions solely on the basis of automated scores. Candidate data should be processed with appropriate privacy and security safeguards.

## Author

**Veerendra Reddy Gaddam**

* GitHub: [VEERENDRAREDDY-510](https://github.com/VEERENDRAREDDY-510)

## License

A license has not yet been specified. Add an appropriate open-source license if you intend to permit others to reuse or modify this project.
