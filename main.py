import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

required_skills = [
    "Python",
    "SQL",
    "Pandas",
    "NumPy",
    "Tableau",
    "Power BI"
]


def extract_text_from_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def score_resume(text):

    score = 0

    feedback = []

    for skill in required_skills:

        if skill.lower() in text.lower():

            score += 100 / len(required_skills)

            feedback.append(
                f"✅ Found {skill}"
            )

        else:

            feedback.append(
                f"❌ Missing {skill}"
            )

    return round(score), feedback
