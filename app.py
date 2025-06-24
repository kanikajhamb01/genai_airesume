import streamlit as st
from github_analysis import analyze_github_repo
from resume_generator import generate_resume
import json
import os
import tempfile
import speech_recognition as sr

st.set_page_config(page_title="AI Resume Builder", layout="centered")

st.title("🧠 AI Resume Builder")
st.write("Build your professional resume with text or voice!")

# Step 1: Start from scratch or upload
resume_mode = st.radio("Select how you'd like to proceed:", ["Create New Resume", "Upload Previous Resume"])

user_data = {}

if resume_mode == "Upload Previous Resume":
    uploaded_file = st.file_uploader("Upload your existing resume (PDF)", type=["pdf"])
    if uploaded_file:
        with open("user_data/uploaded_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())
        st.success("Resume uploaded. You can choose to generate a new one from scratch too.")

else:
    # Step 2: Text or Voice Input
    input_mode = st.radio("How would you like to input your details?", ["Text", "Voice"])

    def get_voice_input(prompt):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info(f"🎙️ {prompt} (Speak now)")
            audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except Exception as e:
            st.error("Voice recognition failed. Please try again.")
            return ""

    def get_input(label):
        if input_mode == "Text":
            return st.text_input(label)
        else:
            return get_voice_input(label)

    # Step 3: Collect basic info
    user_data['name'] = get_input("Full Name")
    user_data['email'] = get_input("Email")
    user_data['phone'] = get_input("Phone Number")
    user_data['linkedin'] = get_input("LinkedIn URL")
    user_data['github'] = get_input("GitHub URL")
    user_data['education'] = get_input("Education (e.g., B.Tech, IGDTUW, 2021-2025)")
    user_data['skills'] = get_input("Skills (comma separated)")
    user_data['experience'] = get_input("Work Experience / Internships")
    user_data['projects'] = get_input("Personal Projects / Achievements")

    # Step 4: GitHub repo analysis
    repo_url = st.text_input("Enter a GitHub repository link (optional):")
    if repo_url:
        project_summary = analyze_github_repo(repo_url)
        user_data['project_summary'] = project_summary
        st.write("🔍 GitHub Analysis Summary:")
        st.success(project_summary)

# Step 5: Template selection
st.markdown("---")
template = st.selectbox("Choose a resume template:", ["Deedy", "ModernCV", "AwesomeCV"])
template_map = {
    "Deedy": "templates/deedy_template.tex",
    "ModernCV": "templates/moderncv_template.tex",
    "AwesomeCV": "templates/awesomecv_template.tex"
}

# Step 6: Generate Resume
if st.button("🚀 Generate Resume"):
    with st.spinner("Generating your resume..."):
        if resume_mode == "Create New Resume":
            # Save data as JSON
            os.makedirs("user_data", exist_ok=True)
            with open("user_data/resume.json", "w") as f:
                json.dump(user_data, f)

        # Call resume generation function
        output_path = generate_resume(user_data, template_map[template])
        if output_path:
            with open(output_path, "rb") as f:
                st.download_button(label="📄 Download Resume", data=f, file_name="AI_Resume.pdf", mime="application/pdf")
        else:
            st.error("Failed to generate resume.")
