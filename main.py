import streamlit as st
from resume_generator import generate_resume
from github_analysis import analyze_single_repo

# ----------------------------
# Page 1: Landing Page
# ----------------------------
def landing_page():
    # Hero Section
    st.markdown("""
        <div style='text-align: center; padding: 3rem 1rem; background-color: #f5f7fa; border-radius: 12px;'>
            <h1 style='font-size: 3rem; color: #2c3e50;'>Welcome to <span style='color:#27ae60;'>AI Resume Builder</span> 🚀</h1>
            <p style='font-size: 1.2rem; color: #555;'>Build beautiful, ATS-friendly resumes in minutes with the power of AI.</p>
        </div>
    """, unsafe_allow_html=True)

    # About Section
    st.markdown("""
        <div style='padding: 2rem 0;'>
            <h2>📄 About This Tool</h2>
            <p>This tool allows you to automatically generate a resume using a simple form or even fetch project info directly from your GitHub. Just pick a template, enter your details, and you're done!</p>
        </div>
    """, unsafe_allow_html=True)

    # Templates Section
    st.markdown("### 🎨 Choose a Resume Template")

    templates = ["classic", "modern", "professional"]
    cols = st.columns(3)

    for i, temp in enumerate(templates):
        with cols[i]:
            st.markdown("""
                <div style="padding: 10px; border-radius: 10px; background-color: #f9f9f9; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center;">
            """, unsafe_allow_html=True)

            st.image(f"templates/{temp}/preview.png", caption=temp.title(), use_container_width=True)

            if st.button(f"Use {temp.title()}", key=f"use_btn_{temp}_{i}"):
                st.session_state["selected_template"] = temp
                st.session_state["page"] = "builder"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # Features Section
    st.markdown("""
        <hr style="margin: 2rem 0;">
        <div>
            <h2>✨ Key Features</h2>
            <ul>
                <li>📎 Upload your existing resume for auto-extraction</li>
                <li>🧠 AI-assisted GitHub project integration</li>
                <li>🎯 Multiple professionally-designed templates</li>
                <li>💾 Download in ready-to-use PDF format</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # ✅ CTA Button: Properly inside the function
    st.markdown("""
        <div style='margin-top: 3rem; text-align: center;'>
            <style>
            div.stButton > button {
                background-color: #27ae60;
                color: white;
                font-size: 1.1rem;
                padding: 0.8rem 2rem;
                border-radius: 10px;
                border: none;
                box-shadow: 0 4px 14px rgba(39, 174, 96, 0.4);
            }
            </style>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Start Crafting Your Resume"):
        st.session_state["page"] = "builder"
        st.rerun()



# ----------------------------
# Page 2: Builder Page
# ----------------------------
def builder_page():
    from resume_parser import extract_text_from_pdf, extract_basic_info

    st.markdown("""
        <div style='padding: 2rem; background: linear-gradient(to right, #e8f5e9, #f1f8e9); border-radius: 12px; margin-bottom: 1rem;'>
            <h1 style='color: #2e7d32;'>🧠 Build Your Smart Resume</h1>
            <p style='color: #555;'>Upload an old resume, fetch GitHub projects, or manually enter details to generate your professional resume.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("💬 Need Help? Talk to our Resume Bot (Coming Soon)", expanded=False):
        st.info("This section will help you interact with a chatbot to fill resume sections intelligently.")

    st.markdown("---")

    # Step 1: Upload
    st.subheader("📄 Upload Existing Resume (Optional)")
    uploaded_file = st.file_uploader("Upload PDF resume", type=["pdf"])
    
    prefill = {
        "name": "", "email": "", "contact": "", "skills": "",
        "linkedin": "", "github": "", "achievements": [],
        "certifications": [], "education": [], "projects": []
    }

    if uploaded_file:
        extracted_text = extract_text_from_pdf(uploaded_file)
        prefill = extract_basic_info(extracted_text)
        st.success("✅ Resume parsed! You can now edit the fields.")

    # Step 2: Personal Info
    st.markdown("### 👤 Personal Info")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=prefill["name"])
            contact = st.text_input("Contact Number", value=prefill["contact"])
            linkedin = st.text_input("LinkedIn URL", value=prefill["linkedin"])
        with col2:
            email = st.text_input("Email", value=prefill["email"])
            github = st.text_input("GitHub Profile", value=prefill["github"])
        skills = st.text_area("Skills (comma-separated)", value=prefill["skills"])

    # Step 3: GitHub Projects
    st.markdown("### 🔍 Auto-Fetch Projects from GitHub")
    repo_url_input = st.text_input("Enter GitHub Repo URL")

    if "fetched_projects" not in st.session_state:
        st.session_state.fetched_projects = []

    if repo_url_input and st.button("Fetch Project"):
        from github_analysis import analyze_single_repo
        repo = analyze_single_repo(repo_url_input)
        if "error" in repo:
            st.error(repo["error"])
        else:
            st.session_state.temp_project = {
                "name": repo["name"],
                "description": repo["description"],
                "tech_stack": repo.get("tech_stack", repo.get("language", "")),
                "url": repo["url"]
            }
            st.success("✅ Project fetched!")

    if "temp_project" in st.session_state:
        st.markdown("📝 Edit Fetched Project:")
        p = st.session_state.temp_project
        p["name"] = st.text_input("Project Name", value=p["name"], key="temp_name")
        p["description"] = st.text_area("Description", value=p["description"], key="temp_desc")
        p["tech_stack"] = st.text_input("Tech Stack", value=p["tech_stack"], key="temp_tech")
        if st.button("Add Project to List"):
            st.session_state.fetched_projects.append(p)
            del st.session_state.temp_project
            st.rerun()

    if st.session_state.fetched_projects:
        st.markdown("✅ Projects Added:")
        for i, proj in enumerate(st.session_state.fetched_projects):
            st.markdown(f"""
            **{i+1}. {proj['name']}**
            - {proj['description']}
            - **Tech Stack:** {proj['tech_stack']}
            """)
            st.markdown("---")

    # Step 4: Manual Projects
    st.markdown("### 💼 Add Custom Projects")
    manual_projects = []
    num_projects = st.number_input("How many?", 0, 5, 0)

    for i in range(num_projects):
        st.markdown(f"**📝 Project {i+1}**")
        pname = st.text_input(f"Project {i+1} Name", key=f"mpname_{i}")
        pdesc = st.text_area(f"Description", key=f"mpdesc_{i}")
        ptech = st.text_input(f"Tech Stack", key=f"mptech_{i}")
        if pname and pdesc:
            manual_projects.append({
                "name": pname,
                "description": pdesc,
                "tech_stack": ptech
            })

    # Step 5: Education
    st.markdown("### 🎓 Education")
    education_list = []
    num_edu = st.number_input("Number of Education Entries", 0, 5, 0)
    for i in range(num_edu):
        deg = st.text_input(f"Degree {i+1}", key=f"deg_{i}")
        inst = st.text_input(f"Institution {i+1}", key=f"inst_{i}")
        detail = st.text_area(f"Details {i+1}", key=f"edetail_{i}")
        if deg and inst:
            education_list.append({"degree": deg, "institution": inst, "details": detail})

    # Step 6: Achievements
    st.markdown("### 🏆 Achievements")
    achievements = []
    num_ach = st.number_input("How many achievements?", 0, 10, 0)
    for i in range(num_ach):
        ach = st.text_input(f"Achievement {i+1}", key=f"ach_{i}")
        if ach:
            achievements.append(ach)

    # Step 7: Certifications
    st.markdown("### 📜 Certifications")
    certifications = []
    num_cert = st.number_input("How many certifications?", 0, 10, 0)
    for i in range(num_cert):
        cert = st.text_input(f"Certification {i+1}", key=f"cert_{i}")
        if cert:
            certifications.append(cert)

    # Step 8: Template
    st.markdown("### 🎨 Template Style")
    template = st.selectbox("Choose your preferred template", ["classic", "modern", "professional"])

    st.markdown("---")

    if st.button("🧾 Generate Resume"):
        all_projects = st.session_state.fetched_projects + manual_projects
        st.session_state.generated_data = {
            "name": name,
            "email": email,
            "contact": contact,
            "skills": skills,
            "linkedin": linkedin,
            "github": github,
            "projects": all_projects,
            "education": education_list,
            "achievements": achievements,
            "certifications": certifications,
            "template": template
        }
        st.success("✅ Resume data saved! Redirecting to PDF generation...")
        st.session_state["page"] = "generate"
        st.rerun()

# ----------------------------
# Page 3: Thank You Page
# ----------------------------
def thank_you_page():
    st.markdown("""
        <div style='text-align: center; padding: 3rem 1rem;'>
            <h1 style='font-size: 2.5rem; color: #2ecc71;'>✅ Resume Successfully Generated!</h1>
            <p style='font-size: 1.2rem; color: #555;'>Your polished, professional resume is ready for download.</p>
        </div>
    """, unsafe_allow_html=True)

    # 🎯 Download Button
    try:
        with open("user_data/generated_resume.pdf", "rb") as f:
            st.download_button("📥 Download My Resume", f, file_name="resume.pdf", use_container_width=True)
    except FileNotFoundError:
        st.error("Resume file not found. Please try generating it again.")

    st.markdown("---")

    # 💬 Chat with Bot Suggestion
    st.markdown("""
        <div style='text-align: center; margin-top: 2rem;'>
            <p style='font-size: 1rem; color: #888;'>Not satisfied yet? Want to make it even better?</p>
            <button disabled style='
                background-color: #2980b9;
                color: white;
                padding: 0.8rem 1.5rem;
                border-radius: 8px;
                border: none;
                font-size: 1rem;
                cursor: not-allowed;
            '>💬 Chat with AI Bot (Coming Soon)</button>
        </div>
    """, unsafe_allow_html=True)

    # 🔁 Start Over Button
    st.markdown("<hr style='margin-top: 3rem;'>", unsafe_allow_html=True)
    if st.button("🔄 Start Over"):
        st.session_state.clear()
        st.rerun()

