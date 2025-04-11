# agents/cv_extractor.py

import fitz  # PyMuPDF
import ollama

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def summarize_cv(text, model="mistral"):
    prompt = f"""
You are an expert AI CV parser.

Extract and return the candidate's information in JSON format with these fields:

- name: Full name of the candidate
- email: Email address
- phone: Phone number
- skills: List of technical and soft skills. Include tools, programming languages, and anything from the Tech Stack, certifications, or experience sections.
- education: List of objects {{ degree, field, institution (if available) }}
- experience: List of objects {{ company, role, duration }}
- certifications: List of technical/professional certifications relevant to the field (e.g., AWS, CEH, GCP)
- achievements: List of any notable accomplishments or outcomes (e.g., "Published paper", "Deployed AI model", "Improved accuracy by 15%")

Make sure to include relevant information from anywhere in the resume — including sections like Skills, Experience, Projects, Certifications, and Achievements.

Return only valid JSON.
Resume:
\"\"\"
{text}
\"\"\"
"""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
