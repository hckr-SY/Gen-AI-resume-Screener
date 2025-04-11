# agents/matcher.py

import sqlite3
from db import DB_PATH
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_all_candidates():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT name, email, phone, skills, education, experience, 
               certifications, achievements, file_name 
        FROM candidates
    """)
    candidates = c.fetchall()
    conn.close()

    return [
        {
            "name": row[0],
            "email": row[1],
            "phone": row[2],
            "skills": row[3],
            "education": row[4],
            "experience": row[5],
            "certifications": row[6] or "",
            "achievements": row[7] or "",
            "file": row[8]
        }
        for row in candidates
    ]

def preprocess_text(text):
    if not text:
        return ""
    return text.replace(",", " and")  # or do more advanced cleanup here later

def boosted(score):
    sim = score / 100
    return round((1.4 * sim) / (0.4 + sim) * 100, 2)

def cosine_text_similarity(text1, text2):
    if not text1 or not text2:
        return 0
    
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)
    try:
        embeddings = model.encode([text1, text2])
        sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return int(sim * 100)
    except Exception as e:
        print(f"⚠️ Cosine similarity error: {e}")
        return 0

def calculate_match_score(jd, candidate):
    # Safely extract JD fields
    jd_text = lambda key: " ".join(jd.get(key, [])) if isinstance(jd.get(key), list) else jd.get(key, "")

    # Handle education which might be a dict or list
    # Handle education which might be a dict or list
    edu_jd = jd.get("education_required", "")
    if isinstance(edu_jd, list):
        edu_field = " ".join(
            f"{e.get('degree', '')} in {e.get('field', '')}" if isinstance(e, dict) else str(e)
            for e in edu_jd
        )
    elif isinstance(edu_jd, dict):
        edu_field = f"{edu_jd.get('degree', '')} in {edu_jd.get('field', '')}"
    else:
        edu_field = str(edu_jd)


    # Candidate fields
    skill_text = candidate.get("skills", "")
    experience = candidate.get("experience", "")
    education = candidate.get("education", "")
    certifications = candidate.get("certifications", "")
    achievements = candidate.get("achievements", "")

    # Cosine-based similarities
    skill_sim = boosted(cosine_text_similarity(jd_text("required_skills"), skill_text))
    exp_sim = boosted(cosine_text_similarity(jd_text("job_responsibilities"), experience))
    edu_sim = boosted(cosine_text_similarity(edu_field, education))
    cert_sim = boosted(cosine_text_similarity(jd_text("required_skills"), certifications))
    ach_sim = boosted(cosine_text_similarity(jd_text("job_responsibilities"), achievements))

    # Final weighted score
    score = (
        skill_sim * 0.4 +
        exp_sim * 0.25 +
        edu_sim * 0.15 +
        cert_sim * 0.1 +
        ach_sim * 0.1
    )

    # print(f"\n🕵️ Checking candidate: {candidate['name']}")
    # print(f"Skills: {candidate['skills']}")
    # print(f"Experience: {candidate['experience']}")
    # print(f"Education: {candidate['education']}")
    # print(f"Certifications: {candidate.get('certifications', '')}")
    # print(f"Achievements: {candidate.get('achievements', '')}")


    return round(score, 2)
