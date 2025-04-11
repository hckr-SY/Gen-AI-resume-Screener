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

## 🚀 How to Run the Project

Follow these steps to set up and run the GenAI Resume Screener on your machine:

1. 📥 Clone the Repository

git clone https://github.com/hckr-SY/Gen-AI-resume-Screener.git
cd Gen-AI-resume-Screener

2. 📦 Install Dependencies

Ensure you have Python 3.9+ installed.

pip install -r requirements.txt

3. 🤖 Start Ollama & Pull Model

Make sure Ollama is installed and running locally.

Pull the required model (e.g., mistral):

ollama pull mistral

4. 🧠 Preprocess Job Descriptions

Parse and cache all job descriptions from job_description.csv:

python precompute_jds.py

5. 📄 Preprocess Resumes 

Parse all resumes in data/allCV/ and insert them into the database:

python precompute_cvs.py

6. 🚀 Launch the Streamlit Web App

streamlit run app.py

Then open http://localhost:8501 in your browser to access the app.
