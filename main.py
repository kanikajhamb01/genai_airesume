import os
import json
import google.generativeai as genai

# Load Gemini API key from environment variable or hardcode (for testing)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyAdxud0lQgq4RrfVKQ1_cXsDB64hE041PA"))

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# ========== Resume Text Enhancer ==========
def enhance_resume_content(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Error with Gemini:", e)
        return "Could not process your request."

# ========== GitHub Project Analyzer ==========
def analyze_github_repo_with_ai(readme_text, repo_name="Project"):
    prompt = f"""
    You are a resume expert. Extract useful resume bullet points from the following GitHub project README. 
    Summarize the project in 2-3 resume-style bullet points, focusing on tech stack, achievements, and functionality.

    Project Name: {repo_name}
    README:
    {readme_text}
    """
    return enhance_resume_content(prompt)

# ========== Example: Rewrite Skills ==========
def rewrite_skills(skills_raw):
    prompt = f"""
    Rewrite the following comma-separated skills into a clean professional format suitable for a resume:
    {skills_raw}
    """
    return enhance_resume_content(prompt)

# ========== Save Final User Data ==========
def save_user_data(user_data, path="user_data/resume.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(user_data, f, indent=4)
    return path
