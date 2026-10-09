import streamlit as st
import requests
import json
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Screening",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0B1220;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: white;
    }

    .subtitle {
        font-size: 18px;
        color: #94A3B8;
        margin-bottom: 30px;
    }

    .stButton button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 AI Resume AI")

    st.markdown("### Features")

    st.write("📄 Resume Parsing")
    st.write("🧠 AI Skill Matching")
    st.write("📊 ATS Score")
    st.write("🎯 Candidate Ranking")
    st.write("🔍 OCR for Scanned Resumes")

    st.divider()

    st.info(
        "Powered by FastAPI + Gemini AI + Tesseract OCR"
    )


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Resume Screening System")

st.caption(
    "Intelligent ATS Resume Analyzer powered by Gemini AI"
)

st.write("")


# ============================================================
# INPUT AREA
# ============================================================

col1, col2 = st.columns([1.2, 1])


# ============================================================
# JOB DESCRIPTION
# ============================================================

with col1:

    st.subheader("📄 Job Description")

    job_description = st.text_area(
        "Enter the job requirements",
        height=250,
        placeholder=(
            "Paste the complete job description here...\n\n"
            "Example:\n"
            "We are looking for a Data Analyst with skills in "
            "Python, SQL, Excel, Power BI and Tableau."
        )
    )


# ============================================================
# RESUME UPLOAD
# ============================================================

with col2:

    st.subheader("📂 Upload Resume")

    resume = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )


    if resume is not None:

        st.success(
            f"Selected: {resume.name}"
        )

        file_size = len(
            resume.getvalue()
        ) / 1024

        st.write(
            f"📦 File size: {file_size:.1f} KB"
        )


st.write("")


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze = st.button(
    "🚀 Analyze Resume",
    key="analyze_resume_button"
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:


    # --------------------------------------------------------
    # VALIDATE RESUME
    # --------------------------------------------------------

    if resume is None:

        st.error(
            "❌ Please upload a resume PDF."
        )

        st.stop()


    # --------------------------------------------------------
    # VALIDATE JOB DESCRIPTION
    # --------------------------------------------------------

    if not job_description.strip():

        st.error(
            "❌ Please enter a job description."
        )

        st.stop()


    # --------------------------------------------------------
    # SEND REQUEST TO FASTAPI
    # --------------------------------------------------------

    try:

        with st.spinner(
            "🤖 Gemini AI is analyzing the resume..."
        ):

            response = requests.post(

                "http://127.0.0.1:8000/upload-resume",

                files={

                    "file": (

                        resume.name,

                        resume.getvalue(),

                        "application/pdf"

                    )

                },

                data={

                    "job_description":
                    job_description

                },

                timeout=120

            )


    # --------------------------------------------------------
    # CONNECTION ERROR
    # --------------------------------------------------------

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI server."
        )

        st.code(
            "python -m uvicorn app.main:app --reload"
        )

        st.stop()


    # --------------------------------------------------------
    # TIMEOUT ERROR
    # --------------------------------------------------------

    except requests.exceptions.Timeout:

        st.error(
            "⏳ Request timed out. Please try again."
        )

        st.stop()


    # --------------------------------------------------------
    # OTHER REQUEST ERRORS
    # --------------------------------------------------------

    except requests.exceptions.RequestException as e:

        st.error(
            f"❌ Request Error: {str(e)}"
        )

        st.stop()


    # ========================================================
    # CHECK RESPONSE STATUS
    # ========================================================

    if response.status_code != 200:

        st.error(
            f"❌ API Error: {response.status_code}"
        )

        st.code(
            response.text
        )

        st.stop()


    # ========================================================
    # CONVERT RESPONSE TO JSON
    # ========================================================

    try:

        result = response.json()


    except ValueError:

        st.error(
            "❌ Invalid response received from FastAPI."
        )

        st.code(
            response.text
        )

        st.stop()


    # ========================================================
    # HANDLE BACKEND ERROR
    # ========================================================

    if "error" in result:

        st.error(
            f"❌ {result['error']}"
        )

        with st.expander(
            "🐞 Debug Information"
        ):

            st.json(result)

        st.stop()


    # ========================================================
    # SUCCESS MESSAGE
    # ========================================================

    st.success(
        "✅ Resume analyzed successfully!"
    )


    # ========================================================
    # GET RESULT VALUES
    # ========================================================

    score = result.get(
        "ats_score",
        0
    )


    recommendation = result.get(
        "recommendation",
        "Not Available"
    )


    # ========================================================
    # ATS SCORE SECTION
    # ========================================================

    st.divider()

    st.subheader(
        "📊 ATS SCORE"
    )


    score_col1, score_col2, score_col3 = st.columns(3)


    with score_col1:

        st.metric(

            label="ATS Score",

            value=f"{score}%"

        )


    with score_col2:

        st.metric(

            label="Recommendation",

            value=recommendation

        )


    with score_col3:

        if score >= 80:

            status = "Excellent"

        elif score >= 60:

            status = "Good"

        elif score >= 40:

            status = "Average"

        else:

            status = "Needs Improvement"


        st.metric(

            label="Match Level",

            value=status

        )


    st.write("")


    # ========================================================
    # ATS SCORE GAUGE
    # ========================================================

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            title={

                "text":
                "Resume Match Score"

            },

            number={

                "suffix":
                "%"

            },

            gauge={

                "axis": {

                    "range":
                    [0, 100]

                },

                "bar": {

                    "thickness":
                    0.3

                }

            }

        )

    )


    fig.update_layout(

        height=350,

        margin=dict(

            l=30,

            r=30,

            t=70,

            b=20

        )

    )


    st.plotly_chart(

        fig,

        width="stretch"

    )


    st.divider()


    # ========================================================
    # SKILLS SECTION
    # ========================================================

    st.subheader(
        "🧠 Skills Analysis"
    )


    skill_col1, skill_col2 = st.columns(2)


    # ========================================================
    # MATCHING SKILLS
    # ========================================================

    with skill_col1:

        st.markdown(
            "### ✅ Matching Skills"
        )


        matching_skills = result.get(

            "matching_skills",

            []

        )


        if matching_skills:


            for skill in matching_skills:

                st.success(
                    f"✓ {skill}"
                )


        else:

            st.info(
                "No matching skills found."
            )


    # ========================================================
    # MISSING SKILLS
    # ========================================================

    with skill_col2:

        st.markdown(
            "### ❌ Missing Skills"
        )


        missing_skills = result.get(

            "missing_skills",

            []

        )


        if missing_skills:


            for skill in missing_skills:

                st.error(
                    f"✗ {skill}"
                )


        else:

            st.success(
                "No major missing skills identified."
            )


    st.divider()


    # ========================================================
    # STRENGTHS AND WEAKNESSES
    # ========================================================

    st.subheader(
        "📋 Candidate Analysis"
    )


    analysis_col1, analysis_col2 = st.columns(2)


    # ========================================================
    # STRENGTHS
    # ========================================================

    with analysis_col1:

        st.markdown(
            "### 💪 Strengths"
        )


        strengths = result.get(

            "strengths",

            []

        )


        if strengths:


            for item in strengths:

                st.info(
                    f"• {item}"
                )


        else:

            st.info(
                "No strengths identified."
            )


    # ========================================================
    # WEAKNESSES
    # ========================================================

    with analysis_col2:

        st.markdown(
            "### ⚠️ Weaknesses"
        )


        weaknesses = result.get(

            "weaknesses",

            []

        )


        if weaknesses:


            for item in weaknesses:

                st.warning(
                    f"• {item}"
                )


        else:

            st.success(
                "No major weaknesses identified."
            )


    st.divider()


    # ========================================================
    # FINAL RECOMMENDATION
    # ========================================================

    st.subheader(
        "🎯 Final Recommendation"
    )


    st.info(
        recommendation
    )


    st.divider()


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    st.subheader(
        "📥 Download Analysis Report"
    )


    st.download_button(

        label="📄 Download JSON Report",

        data=json.dumps(

            result,

            indent=4

        ),

        file_name="resume_analysis_report.json",

        mime="application/json"

    )


    # ========================================================
    # DEBUG OUTPUT
    # ========================================================

    with st.expander(

        "🐞 Debug Output"

    ):

        st.json(
            result
        )