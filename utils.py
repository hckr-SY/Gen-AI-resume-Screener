import json
import re

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