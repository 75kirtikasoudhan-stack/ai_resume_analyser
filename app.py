import streamlit as st
import pdfplumber
import pandas as pd
import re
from io import BytesIO

# ------------------------
# Page Setup
# ------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ------------------------
# Functions
# ------------------------

def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_keywords(text):

    text = text.lower()

    words = re.findall(r'\b[a-zA-Z]+\b', text)

    return set(words)


def analyze_resume(resume_text, jd_text):

    resume_skills = extract_keywords(resume_text)

    jd_skills = extract_keywords(jd_text)

    matched = resume_skills.intersection(jd_skills)

    missing = jd_skills.difference(resume_skills)

    score = 0

    if len(jd_skills) > 0:

        score = round(
            (len(matched) / len(jd_skills)) * 100
        )

    return score, matched, missing


# ------------------------
# Title
# ------------------------

st.title("📄 AI Resume Analyzer")

st.markdown("---")

# ------------------------
# Job Description
# ------------------------

job_description = st.text_area(
    "📌 Enter Job Description",
    height=250,
    placeholder="""
Data Analyst

Python
SQL
Pandas
NumPy
Power BI
Tableau
Excel
Data Visualization
Machine Learning
"""
)

# ------------------------
# Upload Resumes
# ------------------------

uploaded_files = st.file_uploader(
    "Upload Multiple Resumes",
    type=["pdf"],
    accept_multiple_files=True
)

# ------------------------
# Analyze
# ------------------------

if st.button("🚀 Analyze Resumes"):

    if job_description == "":

        st.warning("Enter Job Description")

    elif len(uploaded_files) == 0:

        st.warning("Upload Resume Files")

    else:

        results = []

        for resume in uploaded_files:

            resume_text = extract_text_from_pdf(
                resume
            )

            score, matched, missing = analyze_resume(
                resume_text,
                job_description
            )

            results.append({
                "Resume": resume.name,
                "Match %": score,
                "Matched Skills":
                    ", ".join(sorted(matched)),
                "Missing Skills":
                    ", ".join(sorted(missing))
            })

        df = pd.DataFrame(results)

        df = df.sort_values(
            by="Match %",
            ascending=False
        )

        df.reset_index(
            drop=True,
            inplace=True
        )

        df.index += 1

        st.success("Analysis Completed")

        st.subheader("🏆 Candidate Ranking")

        st.dataframe(
            df,
            use_container_width=True
        )

        # Best Candidate

        best = df.iloc[0]

        st.subheader(
            "🥇 Best Matching Candidate"
        )

        st.success(
            f"{best['Resume']} | Match Score: {best['Match %']}%"
        )

        # Chart

        st.subheader("📊 Match Comparison")

        chart_df = df[["Resume", "Match %"]]

        st.bar_chart(
            chart_df.set_index("Resume")
        )

        # Download Excel

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False
            )

        excel_data = output.getvalue()

        st.download_button(
            label="📥 Download Report",
            data=excel_data,
            file_name="Resume_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )