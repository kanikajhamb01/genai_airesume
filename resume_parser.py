import fitz  # PyMuPDF
import re

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_basic_info(text):
    lines = text.split('\n')

    # Name: take first non-empty line (usually top of resume)
    name = ""
    for line in lines:
        if line.strip():
            name = line.strip()
            break

    # Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    email = email_match.group(0) if email_match else ""

    # Contact (phone) - simple patterns for Indian + Intl numbers
    contact_match = re.search(r"(\+?\d[\d\s\-]{7,}\d)", text)
    contact = contact_match.group(0).strip() if contact_match else ""

    # Skills (try to find line starting with skills keyword)
    skills = ""
    skills_match = re.search(r"(?i)skills\s*[:\-]?\s*(.*)", text)
    if skills_match:
        skills = skills_match.group(1).strip()

    # LinkedIn
    linkedin_match = re.search(r"(https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9\-_/]+)", text)
    linkedin = linkedin_match.group(0) if linkedin_match else ""

    # GitHub
    github_match = re.search(r"(https?://(www\.)?github\.com/[a-zA-Z0-9\-_/]+)", text)
    github = github_match.group(0) if github_match else ""

    # Achievements (look for keyword and capture lines after)
    achievements = []
    ach_match = re.search(r"(?i)achievements\s*[:\-]?\s*(.*)", text, re.DOTALL)
    if ach_match:
        ach_text = ach_match.group(1).strip()
        # Split by new lines or semicolon or bullets
        achievements = re.split(r"[\n;\u2022-]+", ach_text)
        achievements = [a.strip() for a in achievements if a.strip()]

    # Certifications (similar approach)
    certifications = []
    cert_match = re.search(r"(?i)certifications\s*[:\-]?\s*(.*)", text, re.DOTALL)
    if cert_match:
        cert_text = cert_match.group(1).strip()
        certifications = re.split(r"[\n;\u2022-]+", cert_text)
        certifications = [c.strip() for c in certifications if c.strip()]

    # Education (basic capturing lines after Education keyword)
    education = []
    edu_match = re.search(r"(?i)education\s*[:\-]?\s*(.*)", text, re.DOTALL)
    if edu_match:
        edu_text = edu_match.group(1).strip()
        # Split by new lines, then try to parse each line into degree, institution, details
        edu_lines = edu_text.split('\n')
        for line in edu_lines:
            parts = line.split(',')
            if len(parts) >= 2:
                education.append({
                    "degree": parts[0].strip(),
                    "institution": parts[1].strip(),
                    "details": ','.join(parts[2:]).strip() if len(parts) > 2 else ""
                })
            else:
                # If no commas, just put whole line as degree and blank institution
                education.append({
                    "degree": line.strip(),
                    "institution": "",
                    "details": ""
                })

    # Projects (try similar capture after 'projects' keyword)
    projects = []
    proj_match = re.search(r"(?i)projects\s*[:\-]?\s*(.*)", text, re.DOTALL)
    if proj_match:
        proj_text = proj_match.group(1).strip()
        proj_entries = re.split(r"[\n;\u2022-]+", proj_text)
        # Just keep name-description pairs if possible: e.g. "Name: Description"
        for entry in proj_entries:
            if ':' in entry:
                name, desc = entry.split(':', 1)
                projects.append({"name": name.strip(), "description": desc.strip()})
            else:
                # If no colon, treat whole as project name only
                projects.append({"name": entry.strip(), "description": ""})

    return {
        "name": name,
        "email": email,
        "contact": contact,
        "skills": skills,
        "linkedin": linkedin,
        "github": github,
        "achievements": achievements,
        "certifications": certifications,
        "education": education,
        "projects": projects
    }
