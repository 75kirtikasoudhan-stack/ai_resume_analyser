import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from main import extract_text_from_pdf
from main import score_resume

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

st.title("🤖 AI Resume Analyzer")

st.write(
    "Resume Ranking and Candidate Comparison Dashboard"
)

job_desc = st.text_area(
    "Paste Job Description Here"
)

results = []

resume_folder = "resumes"

if os.path.exists(resume_folder):

    for file in os.listdir(resume_folder):

        if file.endswith(".pdf"):

            filepath = os.path.join(
                resume_folder,
                file
            )

            text = extract_text_from_pdf(
                filepath
            )

            score, feedback = score_resume(
                text
            )

            results.append(
                {
                    "Resume": file,
                    "Score": score
                }
            )

    if len(results) > 0:

        df = pd.DataFrame(results)

        df = df.sort_values(
            by="Score",
            ascending=False
        )

        st.subheader(
            "🏆 Candidate Ranking"
        )

        st.dataframe(df)

        best_candidate = df.iloc[0]

        st.success(
            f"Best Candidate : "
            f"{best_candidate['Resume']} "
            f" | Score : "
            f"{best_candidate['Score']}"
        )

        st.subheader(
            "📊 Candidate Comparison"
        )

        st.bar_chart(
            df.set_index("Resume")
        )

        fig, ax = plt.subplots()

        ax.pie(
            df["Score"],
            labels=df["Resume"],
            autopct="%1.1f%%"
        )

        st.subheader(
            "📈 Score Distribution"
        )

        st.pyplot(fig)

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            "⬇ Download Report",
            csv,
            "candidate_report.csv",
            "text/csv"
        )

else:

    st.error(
        "resumes folder not found"
    )