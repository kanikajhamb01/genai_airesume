# 🧠 AI Resume Builder

The **AI Resume Builder** is an intelligent resume generation tool that allows users to interact with a chatbot using **text or voice** input to build an ATS-friendly resume. It collects user details step-by-step, analyzes GitHub profiles (optional), and generates a polished LaTeX resume based on selected templates.

---

## ✨ Features

- 🗣️ **Interactive Chatbot** for collecting resume details  
- 🧾 **Voice and Text Input** support  
- 🎓 Collects Education, Skills, Projects, Experience, etc.  
- 📂 Option to **upload existing resume** to extract information  
- 🌐 **GitHub Repo Analysis** to auto-generate project points  
- 📄 Generates **LaTeX resume** from selected templates  
- 📥 Resume available for **download as PDF**

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Web UI)
- **Backend:** Python (Chatbot, Resume logic)
- **Template Engine:** LaTeX
- **Voice Input:** `speech_recognition`
- **GitHub Analysis:** `PyGithub`

---

## 🚀 How to Run Locally

### 📦 Prerequisites

- Python 3.9+
- Git
- Internet connection for installing libraries

### 🖥️ Setup Instructions


````markdown
## 🚀 How to Run Locally

### 📦 Prerequisites

- Python 3.9+
- Git
- Internet connection for installing libraries

---

### 🖥️ Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/jyotisoni24/AI-Resume-Builder.git
cd AI-Resume-Builder
````

#### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
```

* For **Linux/macOS**:

  ```bash
  source venv/bin/activate
  ```

* For **Windows**:

  ```bash
  venv\Scripts\activate
  ```

#### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

#### 4. Run the App

```bash
streamlit run app.py
```

#### 5. Open in Your Browser

Go to:

```
http://localhost:8501
```

Once the app launches, you can start interacting with the chatbot to build your resume!