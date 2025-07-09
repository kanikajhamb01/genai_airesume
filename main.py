import streamlit as st
from resume_generator import generate_resume
from github_analysis import analyze_single_repo

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
    from resume_parser import extract_text_from_pdf, extract_basic_info

    st.title("🛠️ Resume Builder")

    # Step 1: Upload PDF resume (optional)
    st.markdown("### ✨ Step 1: Upload Previous Resume (Optional)")
    uploaded_file = st.file_uploader("Upload a PDF resume to auto-fill details (or fill manually)", type=["pdf"])

    # Default prefill
    prefill = {
        "name": "",
        "email": "",
        "contact": "",
        "skills": "",
        "linkedin": "",
        "github": "",
        "achievements": [],
        "certifications": [],
        "education": [],
        "projects": []
    }

    if uploaded_file:
        extracted_text = extract_text_from_pdf(uploaded_file)
        prefill = extract_basic_info(extracted_text)
        st.success("✅ Resume content extracted! Edit or add more details below.")

    # Step 2: Personal info inputs
    name = st.text_input("Full Name", value=prefill.get("name", ""))
    email = st.text_input("Email", value=prefill.get("email", ""))
    contact = st.text_input("Contact Number", value=prefill.get("contact", ""))
    skills = st.text_area("Skills (comma-separated)", value=prefill.get("skills", ""), height=100)
    linkedin = st.text_input("LinkedIn URL", value=prefill.get("linkedin", ""))
    github = st.text_input("GitHub Profile URL", value=prefill.get("github", ""))

    # Initialize session state list for fetched projects
    if "fetched_projects" not in st.session_state:
        st.session_state.fetched_projects = []

    # Step 3: Multi GitHub repo fetch
    st.markdown("### 🔍 Step 3: Fetch Projects from GitHub Repository URLs (Optional)")
    repo_url_input = st.text_input("Paste GitHub Repository URL to fetch project info", key="repo_url_input")

    if repo_url_input:
        if st.button("Fetch and Add Project"):
            repo_data = analyze_single_repo(repo_url_input)
            if "error" in repo_data:
                st.error(repo_data["error"])
            else:
                st.session_state.temp_project = {
                    "name": repo_data['name'],
                    "description": repo_data['description'],
                    "tech_stack": repo_data.get("tech_stack", repo_data.get("language", ""))
                }
                st.success("✅ Repository details fetched! Edit and confirm below.")

    # Editable fetched project before adding
    if "temp_project" in st.session_state:
        p = st.session_state.temp_project
        p["name"] = st.text_input("Project Name", value=p["name"], key="temp_proj_name")
        p["description"] = st.text_area("Project Description", value=p["description"], key="temp_proj_desc")
        p["tech_stack"] = st.text_input("Tech Stacks Used", value=p.get("tech_stack", ""), key="temp_proj_tech")

        if st.button("Add this project to my list"):
            st.session_state.fetched_projects.append({
                "name": p["name"],
                "description": p["description"],
                "tech_stack": p["tech_stack"]
            })
            del st.session_state.temp_project
            st.rerun()  # Refresh to clear input and temp project

    # Show all fetched projects
    st.markdown("### Projects Added From GitHub:")
    for i, proj in enumerate(st.session_state.fetched_projects):
        st.write(f"**{i+1}. {proj['name']}**")
        st.write(proj["description"])
        st.write(f"**Tech Stacks:** {proj.get('tech_stack', 'N/A')}")
        st.markdown("---")

    # Step 4: Manual projects input
    st.markdown("### 💼 Step 4: Add More Projects (Optional)")
    project_list_manual = []
    num_projects = st.number_input("How many additional projects do you want to add?", min_value=0, max_value=5, step=1)

    for i in range(num_projects):
        st.markdown(f"**Project {i+1}**")
        pname = st.text_input(f"Project {i+1} Name", key=f"pname_{i}")
        pdesc = st.text_area(f"Project {i+1} Description", key=f"pdesc_{i}")
        ptech = st.text_input(f"Project {i+1} Tech Stacks", key=f"ptech_{i}")
        if pname and pdesc:
            project_list_manual.append({
                "name": pname,
                "description": pdesc,
                "tech_stack": ptech
            })

    # Step 5: Education input
    st.markdown("### 🎓 Step 5: Add Education (Optional)")
    education_list = []
    num_edu = st.number_input("How many education entries do you want to add?", min_value=0, max_value=5, step=1)

    for i in range(num_edu):
        st.markdown(f"**Education {i+1}**")
        degree = st.text_input(f"Degree", key=f"degree_{i}")
        institution = st.text_input(f"Institution", key=f"institution_{i}")
        details = st.text_area(f"Details", key=f"details_{i}")
        if degree and institution:
            education_list.append({"degree": degree, "institution": institution, "details": details})

    # Step 6: Achievements
    st.markdown("### 🏆 Step 6: Add Achievements (Optional)")
    achievements_list = []
    num_ach = st.number_input("How many achievements do you want to add?", min_value=0, max_value=10, step=1)

    for i in range(num_ach):
        ach = st.text_input(f"Achievement {i+1}", key=f"ach_{i}")
        if ach:
            achievements_list.append(ach)

    # Step 7: Certifications
    st.markdown("### 📜 Step 7: Add Certifications (Optional)")
    certifications_list = []
    num_cert = st.number_input("How many certifications do you want to add?", min_value=0, max_value=10, step=1)

    for i in range(num_cert):
        cert = st.text_input(f"Certification {i+1}", key=f"cert_{i}")
        if cert:
            certifications_list.append(cert)

    # Step 8: Select template
    st.markdown("### 🎨 Step 8: Select Resume Template")
    template = st.selectbox("Choose Template", ["classic", "modern", "professional"])

    st.markdown("---")
    if st.button("🧾 Generate Resume"):
        # Combine fetched and manual projects
        combined_projects = st.session_state.fetched_projects + project_list_manual

        st.session_state.generated_data = {
            "name": name,
            "email": email,
            "contact": contact,
            "skills": skills,
            "linkedin": linkedin,
            "github": github,
            "projects": combined_projects,
            "education": education_list,
            "achievements": achievements_list,
            "certifications": certifications_list,
            "template": template
        }
        st.success("✅ Resume data ready! Proceeding to PDF generation...")
        st.session_state.page = "generate"
        st.rerun()

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
