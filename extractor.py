import os
import json
from PyPDF2 import PdfReader
import requests
from dotenv import load_dotenv
import re

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def clean_json_text(text: str) -> str:
    # Remove code block wrappers
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()

    # Attempt to fix broken newlines inside quoted strings
    lines = text.splitlines()
    fixed_lines = []
    in_string = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        quote_count = line.count('"')
        if quote_count % 2 == 1:
            in_string = not in_string
            fixed_lines.append(line.replace("\n", " "))
        elif in_string:
            fixed_lines[-1] += " " + line
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

import re

def query_groq_for_resume_info(resume_text: str, max_retries: int = 5) -> dict:
    system_prompt = (
        "You are a professional resume parser. Given the raw resume text, extract structured JSON with the following fields:\n"
        "- name\n- email\n- phone\n- bio\n- education\n- tech_stack\n- achievements\n- experience\n- projects\n- socials\n- tone\n\n"
        "⚠️ Return ONLY valid JSON. No markdown, comments, or extra text.\n"
        "Make sure fields like 'bio' or 'description' do not break due to newlines.\n\n"
        "Resume:\n"
    )

    note_text = ("\n\n\nNote for you: do not give any other extra content or feed back except the json structure.\n\n"
        "You should not give any other text except the json structure.\n\n"
        )

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "system", "content": system_prompt + resume_text + note_text}],
        "max_tokens": 2048 * 2,
        "temperature": 0.2
    }

    for attempt in range(1, max_retries + 1):
        print(f"🔁 Attempt {attempt} to extract structured data from Groq...")

        try:
            res = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
            response = res.json()
            raw_content = response["choices"][0]["message"]["content"]

            print("📨 Groq Response (preview):\n", raw_content)

            cleaned_text = clean_json_text(raw_content)

            return json.loads(cleaned_text)

        except json.JSONDecodeError:
            print("❌ Failed to parse valid JSON from Groq response.")
            if attempt < max_retries:
                print("🔄 Retrying...\n")
            else:
                print("🚫 Maximum retries reached. Extraction failed.")
        except Exception as e:
            print("❌ Error during Groq API call:", str(e))
            break

    return {}



def start_extraction_process():
    path = input("Enter resume file path (default: ./resume.pdf): ").strip() or "./resume.pdf"
    if not os.path.exists(path):
        print("❌ File not found.")
        return

    print("📄 Reading resume...")
    resume_text = extract_text_from_pdf(path)

    print("🤖 Asking Groq to extract structured data...")
    config = query_groq_for_resume_info(resume_text)

    if config:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
        print("✅ config.json created from resume!")
        print("✅ Resume parsed and data pre-filled. You can now review or overwrite fields.")
        print("Extracted Data:")
        print(json.dumps(config, indent=4))
    else:
        print("⚠️ Extraction failed or incomplete.")

if __name__ == "__main__":
    start_extraction_process()
