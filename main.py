import streamlit as st
from resume_generator import generate_resume
from github_analysis import analyze_github_projects

# ----------------------------
# Page 1: Landing Page
# ----------------------------
def landing_page():
    st.title("🚀 AI Resume Builder")
    st.subheader("Choose a template to get started")

    templates = ["classic", "modern", "professional"]
    cols = st.columns(3)

    for i, temp in enumerate(templates):
        with cols[i]:
            st.image(f"templates/{temp}/preview.png", caption=temp.title(), use_container_width=True)
            if st.button(f"Use {temp.title()}", key=f"use_btn_{temp}_{i}"):
                st.session_state["selected_template"] = temp
                st.session_state["page"] = "builder"
                st.rerun()

# ----------------------------
# Page 2: Builder Page
# ----------------------------
def builder_page():
    st.title("🛠️ Resume Builder")
    from resume_parser import extract_text_from_pdf, extract_basic_info

    st.markdown("### ✨ Step 1: Upload Previous Resume (Optional)")
    uploaded_file = st.file_uploader("Upload a PDF resume to auto-fill details (or fill manually)", type=["pdf"])

    prefill = {"name": "", "email": "", "skills": "", "projects": []}

    if uploaded_file:
        extracted_text = extract_text_from_pdf(uploaded_file)
        prefill = extract_basic_info(extracted_text)
        st.success("✅ Resume content extracted! Edit or add more details below.")

    st.markdown("### ✍️ Step 2: Fill or Edit Resume Details")

    name = st.text_input("Full Name", value=prefill["name"])
    email = st.text_input("Email", value=prefill["email"])
    skills = st.text_area("Skills (comma-separated)", value=prefill["skills"], height=100)

    st.markdown("### 💼 Step 3: Add Projects (Optional)")

    project_list = []
    num_projects = st.number_input("How many projects do you want to add?", min_value=0, max_value=5, step=1)

    for i in range(num_projects):
        st.markdown(f"**Project {i+1}**")
        pname = st.text_input(f"Project {i+1} Name", key=f"pname_{i}")
        pdesc = st.text_area(f"Project {i+1} Description", key=f"pdesc_{i}")
        if pname and pdesc:
            project_list.append({"name": pname, "description": pdesc})

    st.markdown("### 🎨 Step 4: Select Resume Template")
    template = st.selectbox("Choose Template", ["classic", "modern", "professional"])

    st.markdown("---")
    if st.button("🧾 Generate Resume"):
        st.session_state.generated_data = {
            "name": name,
            "email": email,
            "skills": skills,
            "projects": project_list,
            "template": template
        }
        st.success("✅ Resume data ready! Proceeding to PDF generation...")
        st.session_state.page = "generate"

# ----------------------------
# Page 3: Thank You Page
# ----------------------------
def thank_you_page():
    st.title("✅ Resume Generated!")
    st.write("Your resume has been successfully created.")

    try:
        with open("user_data/generated_resume.pdf", "rb") as f:
            st.download_button("📥 Download Resume", f, file_name="resume.pdf")
    except FileNotFoundError:
        st.error("Resume file not found. Please try generating it again.")

    if st.button("🔄 Start Over"):
        st.session_state.clear()
        st.rerun() 


