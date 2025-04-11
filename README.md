# 🧠 GenAI Resume Screener

A Streamlit-based web application that uses Generative AI and semantic similarity to intelligently match candidate resumes with job descriptions.

---

## 🚀 Features

- LLM-based parsing of job descriptions and resumes (using Ollama + Mistral)
- Semantic cosine similarity scoring using Sentence Transformers
- Multi-agent architecture (JD parser, CV extractor, matcher, UI)
- SQLite-powered resume database
- Streamlit UI for viewing top-matching candidates

---

## 🛠 Technologies Used

- Python
- Streamlit
- Ollama (Mistral model)
- SentenceTransformers
- scikit-learn
- PyMuPDF
- SQLite
- Pandas

---

## 🧱 Project Structure

project_hackathon/
├── app.py                     # Streamlit web app
├── precompute_jds.py          # Parses JDs via Ollama
├── precompute_cvs.py          # ✅ Parses resumes and adds to DB
├── requirements.txt
├── README.md
│
├── agents/
│   ├── matcher.py             # Resume-JD matcher
│   └── cv_extractor.py        # Resume extractor using LLM
│
├── utils/
│   ├── __init__.py
│   └── jd_loader.py           # Load parsed JD cache
│
├── data/
│   ├── allCV/                 # Folder with PDF resumes
│   ├── job_description.csv    # Raw JDs
│   ├── jd_cache.pkl           # Pre-parsed JD cache
│   └── jobmatch.db            # Parsed resume DB

