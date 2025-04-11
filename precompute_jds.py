# precompute_jds.py

import pandas as pd
import ollama
import json
import pickle
import os
import re

CSV_PATH = "data/job_description.csv"
CACHE_PATH = "data/jd_cache.pkl"

def call_ollama_parse_jd(text, model="mistral"):
    prompt = f"""
You are an expert job description parser.

Strictly extract and return the following fields in **valid JSON format only** — no explanation or extra text.

Return only a JSON object with the following fields:
- "job_title" (string)
- "required_skills" (list of strings)
- "experience_required" (string)
- "education_required" (either a list of objects with 'degree' and 'field' or a string)
- "location" (string)
- "job_responsibilities" (list of strings)

Respond with strict JSON syntax — this will be parsed by `json.loads()` in code.

Job Description:
{text}
"""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


def clean_and_parse_json(text):
    try:
        text = text.strip("```json").strip("```").strip()

        # Fix unquoted keys
        text = re.sub(r'(?<=\{|,)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', text)

        # ✅ Fix bad escape characters (e.g., "\ M", "\ A")
        text = re.sub(r'\\([^\"ntbrf\\/])', r'\\\\\1', text)

        return json.loads(text)
    except Exception as e:
        print("❌ JSON parse failed:", e)
        return None

def run():
    df = pd.read_csv(CSV_PATH, encoding="ISO-8859-1")
    jds = {}

    for idx, row in df.iterrows():
        raw_text = row["Job Description"]
        try:
            raw_output = call_ollama_parse_jd(raw_text)
            parsed = clean_and_parse_json(raw_output)

            if parsed and "job_title" in parsed:
                print(f"✅ Parsed JD: {parsed['job_title']}")
                jds[row["Job Title"]] = parsed
            else:
                print(f"❌ JD at row {idx} could not be parsed")

        except Exception as e:
            print(f"❌ Error on row {idx}: {e}")

    with open(CACHE_PATH, "wb") as f:
        pickle.dump(jds, f)

    print(f"✅ Saved {len(jds)} parsed JDs to {CACHE_PATH}")

if __name__ == "__main__":
    run()
