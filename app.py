import streamlit as st
from agents.matcher import get_all_candidates, calculate_match_score, boosted
from db import init_db
from utils.jd_loader import load_all_jds, load_jd
import pandas as pd

# Initialize DB and load all parsed job descriptions
init_db()
all_jds = load_all_jds()
roles = list(all_jds.keys())

# print(all_jds)

st.set_page_config(page_title="GenAI Resume Matcher", layout="wide")
st.title("🧠 GenAI-Powered Resume Shortlister")

# --- Step 1: Job Description Selection ---
st.sidebar.header("Job Role")
role = st.sidebar.selectbox("Select a JD to match candidates:", roles)
jd = load_jd(role)

st.subheader("📄 Job Description")
st.markdown(f"**Role:** {jd['job_title']}")
st.markdown("**Required Skills:**")
st.write(jd.get("required_skills", []))
st.markdown("**Responsibilities:**")
st.write(jd.get("job_responsibilities", []))

# --- Step 2: Candidate Matching ---
if st.button("🔍 Match Candidates"):
    st.info("Running semantic similarity matching...")

    ranked = []
    for candidate in get_all_candidates():
        raw_score = calculate_match_score(jd, candidate)
        display_score = boosted(raw_score)
        candidate["match_score"] = raw_score
        candidate["display_score"] = display_score
        ranked.append(candidate)

    ranked.sort(key=lambda c: c["match_score"], reverse=True)

    st.success("✅ Top 5 candidates:")
    for i, cand in enumerate(ranked[:5], 1):
        st.markdown(f"### {i}. {cand['name']} ({cand['display_score']}%)")
        st.write(f"📧 {cand['email']} | 📄 {cand['file']}")
        with st.expander("View Details"):
            st.markdown(f"**Skills:** {cand['skills']}")
            st.markdown(f"**Experience:** {cand['experience']}")
            st.markdown(f"**Education:** {cand['education']}")
            st.markdown(f"**Certifications:** {cand.get('certifications', '')}")
            st.markdown(f"**Achievements:** {cand.get('achievements', '')}")