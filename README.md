# 🧠 CV Tutor – AI-Powered Resume & JD Analyzer

CV Tutor is a smart AI-based web application that enhances job applications for candidates and streamlines the recruitment process for HR teams. It compares resumes with job descriptions, suggests improvements, and automates key hiring workflows.

---

## ✨ Features

### 👨‍💼 For Candidates:

- 🔢 **Percentage Match**  
  Calculates how closely the resume aligns with the provided job description.

- 🔍 **Missing Skills Detection**  
  Identifies essential skills listed in the job description but not found in the resume.

- 💡 **Improvement Suggestions**  
  Provides actionable advice on how to tailor the resume to better fit the job description.

- ❓ **Question Generation**  
  Generates potential interview questions based on both the resume and job description to help the candidate prepare.

---
![Test Resume Result](https://github.com/anonhossain/cv_project/blob/main/screenshots/12%20Test%20resume%20result.PNG)

### 🧑‍💻 For HR Teams:

- 📊 **CV Sorting by Match %**  
  Automatically sorts multiple resumes against a single job description based on compatibility scores.

![Sort CV](https://github.com/anonhossain/cv_project/blob/main/screenshots/5.%20Analyze%20CV.PNG)

- 📥 **Resume Data Extraction**  
  Extracts candidate details like:
  - Full Name
  - Email
  - Phone Number
  - Reference Emails & Phone Numbers  
  Saves this information in an organized Excel sheet.

![Extract Info](https://github.com/anonhossain/cv_project/blob/main/screenshots/6.Extract%20info.PNG)

- 📧 **Email Automation**  
  Automatically sends emails to selected candidates using customizable templates.

![Send Email](https://github.com/anonhossain/cv_project/blob/main/screenshots/9.2.PNG)
----
![Received Email](https://github.com/anonhossain/cv_project/blob/main/screenshots/9.3.PNG)

- 📄 **Interview Question Generation**  
  Generates a tailored set of viva questions for each candidate and saves them in a `.docx` file.

![Generate Multiple Questions](https://github.com/anonhossain/cv_project/blob/main/screenshots/11%20Generate%20Question%20Output.PNG)
----
![Each Question File](https://github.com/anonhossain/cv_project/blob/main/screenshots/7.Generate%20Q.PNG)

## 🖼️ Screenshots

### 📌 Landing Page
![Landing Page](https://raw.githubusercontent.com/anonhossain/cv_tutor/main/screenshot/Landing%20Page.png)

### 📌 Dashboard & Main Features
![Dashboard](https://raw.githubusercontent.com/anonhossain/cv_tutor/main/screenshot/Dashboard.png)

---

## 🚀 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **AI/NLP:** Gemini, Redex
- **File Handling:** `python-docx`, `openpyxl`, `pdfplumber`
- **Automation:** SMTP, Email Templates

---

## 🔧 Setup Instructions

```bash
git clone https://github.com/anonhossain/cv_tutor.git
cd cv_tutor
pip install -r requirements.txt
python main.py
