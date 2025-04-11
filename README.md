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

🚀 How to Run the Project
Clone the repository

bash
Copy
Edit
git clone https://github.com/hckr-SY/Gen-AI-resume-Screener.git
cd Gen-AI-resume-Screener
Install dependencies

Make sure you have Python 3.9+ installed.

nginx
Copy
Edit
pip install -r requirements.txt
Start Ollama (LLM must be available locally)

Pull and start the required model (e.g. mistral):

nginx
Copy
Edit
ollama pull mistral
Make sure ollama is running in the background.

(Optional) Preprocess Job Descriptions

If you want to cache parsed JDs:

nginx
Copy
Edit
python precompute_jds.py
(Optional) Preprocess Resumes

To parse all resumes from data/allCV/ and store them in the database:

nginx
Copy
Edit
python precompute_cvs.py
Run the Web App

arduino
Copy
Edit
streamlit run app.py