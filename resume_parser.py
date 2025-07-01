import fitz  # PyMuPDF
import re

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_basic_info(text):
    name = text.split('\n')[0].strip()

    # Extract email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    email = email_match.group(0) if email_match else ""

    # Extract skills (very basic)
    skills_match = re.search(r"(?i)skills\s*[:\-]?\s*(.*)", text)
    skills = skills_match.group(1) if skills_match else ""

    return {
        "name": name,
        "email": email,
        "skills": skills
    }
