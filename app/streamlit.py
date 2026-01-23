import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/analyze-resume"

st.set_page_config(
    page_title="AI Resume Matcher",
    layout="centered"
)

st.title("📄 AI Resume–Job Matcher")
st.caption("Upload a resume, paste a job description, and get AI-powered feedback")

# -------------------- Inputs --------------------

job_description = st.text_area(
    "📌 Paste Job Description",
    height=220,
    placeholder="Paste the full job description here..."
)

resume_file = st.file_uploader(
    "📄 Upload Resume (PDF only)",
    type=["pdf"]
)

# -------------------- Action --------------------

if st.button("🚀 Analyze Resume"):

    if not resume_file or not job_description.strip():
        st.error("Please upload a resume and paste a job description.")
        st.stop()

    with st.spinner("Analyzing resume... Please wait ⏳"):

        files = {
            "resume": (
                resume_file.name,
                resume_file.getvalue(),
                "application/pdf"
            )
        }

        data = {
            "job_description": job_description
        }

        response = requests.post(
            API_URL,
            files=files,
            data=data
        )

        if response.status_code != 200:
            st.error(f"Backend error ({response.status_code})")
            st.write(response.text)
            st.stop()

        result = response.json()

    # -------------------- Results --------------------

    st.success("✅ Analysis completed successfully")

    st.subheader("📊 Match Scores")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Similarity Score",
            f"{result['similarity_score']}%"
        )

    with col2:
        st.metric(
            "Skill Match",
            f"{result['skill_match_percentage']}%"
        )

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("✅ Matched Skills")
        if result["matched_skills"]:
            for skill in result["matched_skills"]:
                st.markdown(f"- {skill}")
        else:
            st.write("No strong matches found.")

    with col4:
        st.subheader("❌ Missing Skills")
        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.markdown(f"- {skill}")
        else:
            st.write("No major gaps detected.")

    st.divider()

    st.subheader("🧠 AI Feedback & Improvement Suggestions")
    st.markdown(result["ai_feedback"])
