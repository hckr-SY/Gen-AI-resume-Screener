import os
import re
import json
from agents.cv_extractor import extract_text_from_pdf, summarize_cv
from db import init_db, insert_candidate, candidate_exists
 


def clean_and_parse_json(text):
    try:
        # Remove markdown wrappers
        text = text.replace("```json", "").replace("```", "").strip()

        # Remove trailing commas
        text = re.sub(r",(\s*[\]}])", r"\1", text)

        # Fix unquoted property names: job_title: → "job_title":
        text = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)\s*:', r'\1"\2":', text)

        # Replace smart quotes (LLM quirk)
        text = text.replace("“", "\"").replace("”", "\"").replace("’", "'")

        return json.loads(text)

    except Exception as e:
        print("❌ Failed to parse JSON:")
        print("Error:", e)
        print("Raw input:\n", text[:500])
        return None

# === Step 2: Initialize Database ===

init_db()

# === Step 3: Parse All CVs and Insert into DB === COMPLETED

cv_dir = "data/allCV"
parsed_cvs = []

print("\n📂 Processing all CVs in 'data/allCV/'...\n")

required_fields = ["name", "email", "skills", "education", "experience"]

for file_name in os.listdir(cv_dir):
    if file_name.endswith(".pdf"):
        if candidate_exists(file_name):
            print(f"✅ Already in DB: {file_name}")
            continue

        print(f"🔍 Parsing new file: {file_name}")
        try:
            text = extract_text_from_pdf(os.path.join(cv_dir, file_name))
            raw_summary = summarize_cv(text)
            parsed = clean_and_parse_json(raw_summary)

            # Validate required fields before saving
            if parsed and all(field in parsed and parsed[field] for field in required_fields):
                parsed["file"] = file_name
                parsed_cvs.append(parsed)
                insert_candidate(parsed)
                print(f"✅ Parsed and saved to DB: {file_name}\n")
            else:
                print(f"⚠️ Skipping {file_name}: incomplete or malformed data.\n")

        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}\n")


# === Step 4: Final Output ===

print(f"\n✅ Finished processing {len(parsed_cvs)} new CV(s).")
if parsed_cvs:
    print("\nSample parsed CV:\n")
    print(parsed_cvs[0])
else:
    print("⚠️ No new CVs were processed.")