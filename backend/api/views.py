from email.mime.text import MIMEText
from io import BytesIO
import smtplib
from flask import jsonify
import pandas as pd
from typing import List, Optional
from fastapi import APIRouter, Form, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from WappSender import WappSender
from EmailSender import EmailSender

from dotenv import load_dotenv
from user import LoginRequest, RegisterRequest, UserOut, UserIn, UserUpdate
from dbhelper import DBhelper  # Make sure to import DBhelper
from gimini import Gemini, GeminiHR, GeminiHR_Generate_questions, ResumeExtractor
import re
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import shutil
import os

app = FastAPI()

# Define the directories where files will be saved
RESUME_DIRECTORY = "C:\\xampp\\htdocs\\login_signup\\uploads\\Candidate\\CV"
JOB_DESC_DIRECTORY = "C:\\xampp\\htdocs\\login_signup\\uploads\\Candidate\\JD"
HR_RESUME_DIRECTORY = "C:\\xampp\\htdocs\\login_signup\\uploads\\HR\\CV"
HR_JOB_DESC_DIRECTORY = "C:\\xampp\\htdocs\\login_signup\\uploads\\HR\\JD"
VIDEO_RESUME_DIRECTORY = "C:\\xampp\\htdocs\\login_signup\\uploads\\HR\\video_file"


# Ensure directories exist
os.makedirs(RESUME_DIRECTORY, exist_ok=True)
os.makedirs(JOB_DESC_DIRECTORY, exist_ok=True)

# Initialize the database helper
db = DBhelper()
gim = Gemini()
geminiHR = GeminiHR()
ResumeExtractor = ResumeExtractor()
api = APIRouter(prefix="/api")

@api.post("/login")
def login(request: LoginRequest):
    data = db.search(request.username, request.password)

    if not data:
        raise HTTPException(status_code=401, detail="Incorrect email, phone number, or username/password")

    return {"message": "Login successful", "user": {"id": data[0][0], "name": f"{data[0][1]} {data[0][2]}", "role": data[0][7]}}


@api.post("/api/register")
def register_user(user: RegisterRequest):
    # Check if the username or email already exists
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (user.username, user.email))
    existing_user = cursor.fetchone()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Register the new user
    user_id = db.register_user(
        user.first_name, 
        user.last_name, 
        user.username, 
        user.phone, 
        user.email, 
        user.password, 
        user.role
    )

    if user_id:
        return {"message": "User registered successfully!"}
    else:
        raise HTTPException(status_code=500, detail="User registration failed")

@api.get("/hello")
def hello():
    return {"message": "Hello, Anon!"}

@api.get("/users",)
def get_users():
    db = DBhelper()
    db.mycursor.execute("SELECT * FROM users")
    users = db.mycursor.fetchall()
    return users

@api.get("/info")
def dashboardinfo():
    db = DBhelper()
    db.mycursor.execute("SELECT * FROM users")
    users = db.mycursor.fetchall()
    candidate = 0
    admin = 0
    hr = 0
    for user in users:
        if user[7] == 'Candidate':
            candidate += 1
        if user[7] == 'Admin':
            admin += 1
        if user[7] == 'HR':
            hr += 1
    
    return {"candidate": candidate, "admin": admin, "hr": hr}

@api.get("/users/delete/{user_id}")
def delete_user(user_id: int):
    db = DBhelper()
    db.mycursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.conn.commit()
    return {"message": "User deleted successfully!"}


@api.patch("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate):
    # Check if the user exists before updating
    db.mycursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    existing_user = db.mycursor.fetchone()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user information
    update_query = """
    UPDATE users 
    SET first_name = %s, last_name = %s, username = %s, phone = %s, email = %s, role = %s
    WHERE id = %s
    """
    db.mycursor.execute(
        update_query, 
        (user.first_name, user.last_name, user.username, user.phone, user.email, user.role, user_id)
    )
    db.conn.commit()

    return UserOut(
        id=user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone=user.phone,
        email=user.email,
        role=user.role
    )
#Google API
# view.py
# This one works
@api.get("/analyze_resume/")
async def analyze_resume():
    gimini_response = gim.process_resume()
    return {"response": gimini_response}

@api.post("/upload_files/")
async def upload_files(
    job_desc: str = Form(...), 
    resume: UploadFile = File(...),  
    action: str = Form(...)
):
    # Save the job description as a text file
    job_desc_path = os.path.join(JOB_DESC_DIRECTORY, "jd.txt")
    with open(job_desc_path, "w") as jd_file:
        jd_file.write(job_desc)

    # Save the resume PDF asynchronously
    resume_path = os.path.join(RESUME_DIRECTORY, "resume.pdf")
    with open(resume_path, "wb") as buffer:
        buffer.write(await resume.read())

    # Process the resume based on the action provided
    try:
        job_description = load_job_description(job_desc_path)
        resume_text = extract_text_from_pdf(resume_path)
        response = process_resume(job_description, resume_text, action)
        return {"response": response}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"File not found: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Example placeholder functions (implement these with your AI model integration)
def load_job_description(job_desc_file):
    with open(job_desc_file, "r") as file:
        return file.read()

def extract_text_from_pdf(resume_file):
    # Implement PDF text extraction logic here
    return "Extracted text from resume"

def process_resume(job_description, resume_text, action):
    # Implement your resume processing logic here
    return f"Processed {action} on resume"

@app.post("/upload_files/")
async def upload_files(job_desc: str = Form(...), resume: UploadFile = File(...)):
    # Ensure directories exist
    os.makedirs(RESUME_DIRECTORY, exist_ok=True)
    os.makedirs(JOB_DESC_DIRECTORY, exist_ok=True)
    
    # Save the job description as a text file
    job_desc_path = os.path.join(JOB_DESC_DIRECTORY, "jd.txt")
    with open(job_desc_path, "w") as jd_file:
        jd_file.write(job_desc)

    # Save the resume PDF
    resume_path = os.path.join(RESUME_DIRECTORY, "resume.pdf")
    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    return {"message": "Files uploaded successfully"}

def generate_questions():
    # Add question generation logic here
    return "Questions generated successfully."

@app.post("/analyze_resume/")
async def analyze_resume():
    try:
        # Call the Gemini process_resume method
        analysis_result = Gemini.process_resume()
        return {"analysis": analysis_result}
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Files not found. Upload files first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to save job description
@app.post("/upload/job-description")
async def upload_job_description(description: str = Form(...)):
    os.makedirs(JOB_DESC_DIRECTORY, exist_ok=True)
    jd_path = os.path.join(JOB_DESC_DIRECTORY, "jd.txt")
    
    with open(jd_path, "w") as jd_file:
        jd_file.write(description)
    
    return JSONResponse(content={"message": "Job description saved successfully", "path": jd_path})

# Endpoint to upload resume PDF
@app.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    os.makedirs(RESUME_DIRECTORY, exist_ok=True)
    destination_path = os.path.join(RESUME_DIRECTORY, file.filename)
    
    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return JSONResponse(content={"message": "Resume uploaded successfully", "path": destination_path})

@app.post("/upload_hr_resume/")
async def upload_resume(file: UploadFile):
    """Upload resume file."""
    if not os.path.exists(GeminiHR.RESUME_HR_DIRECTORY):
        os.makedirs(GeminiHR.RESUME_HR_DIRECTORY)

    file_path = os.path.join(GeminiHR.RESUME_HR_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Resume uploaded successfully", "file_path": file_path}

@api.get("/analyze_resume_hr/")
async def analyze_resume_hr():
    gimini_response = GeminiHR.process_resume()
    return {"response": gimini_response}

@app.post("/analyze_resume_hr/")
async def analyze_resume():
    try:
        # Call the Gemini process_resume method
        analysis_result = GeminiHR.process_resume()
        return {"analysis": analysis_result}
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Files not found. Upload files first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api.get("/get_resume_filenames/")
async def get_resume_filenames():
    try:
        # Get a list of all files in the directory
        filenames = [f for f in os.listdir(HR_RESUME_DIRECTORY) if os.path.isfile(os.path.join(HR_RESUME_DIRECTORY, f))]
        return {"filenames": filenames}
    except Exception as e:
        return {"error": str(e)} 
      
@api.post("/extract_resume_info/")
async def get_resume_info(fileNames: List[str]):
    result = ResumeExtractor.extract_resume_info(fileNames)
    return result

# -----------------
UPLOAD_DIR = "../../uploads/HR/CV"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@api.post("/hr-submit-resume")
async def hr_submit_resume(
    job_desc: str = Form(...), 
    resumes: list[UploadFile] = File(...)
):
    """
    Handle form submission: save resumes as PDFs and job description as a text file.
    """
    # Save job description
    job_desc_path = os.path.join(HR_JOB_DESC_DIRECTORY, "jd.txt")
    with open(job_desc_path, "w", encoding="utf-8") as f:
        f.write(job_desc)

    # Save resumes
    saved_files = []
    for r in resumes:
        if r.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail=f"File '{r.filename}' is not a PDF.")

        file_path = os.path.join(HR_RESUME_DIRECTORY, r.filename)
        with open(file_path, "wb") as f:
            f.write(await r.read())
        saved_files.append(r.filename)

    gimini_response = GeminiHR.process_resume()
    return {"response": gimini_response}


@api.post("/video_resume_upload")
async def video_resume_upload(video_resumes: list[UploadFile] = File(...)):
    """
    Handle video resume uploads.
    """
    saved_videos = []
    for vr in video_resumes:
        if not vr.content_type.startswith("video/"):
            raise HTTPException(status_code=400, detail=f"File '{vr.filename}' is not a video file.")

        # Save the video file
        video_path = os.path.join(VIDEO_RESUME_DIRECTORY, vr.filename)
        with open(video_path, "wb") as f:
            f.write(await vr.read())
        saved_videos.append(vr.filename)

    return {"message": "Video resumes uploaded successfully.", "saved_files": saved_videos}


@api.post("/get_excel_columns/")
async def get_excel_columns(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename.lower()
        if filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(contents))
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(BytesIO(contents))
        else:
            raise ValueError("Unsupported file type. Only Excel and CSV are supported.")
        
        columns = list(df.columns)
        return {"columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@api.post("/send_emails/")
async def send_emails(
    subject: str = Form(...),
    email_col: str = Form(...),
    email_message: str = Form(...),
    file: UploadFile = Form(...)
):
    try:
        sender = EmailSender(subject, email_col, email_message, file)
        await sender.send_bulk_emails()
        return {"message": "Emails sent successfully!"}
    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An error occurred: {str(e)}"})

@api.get("/generate_hr_questions")
def generate_hr_questions():
    OUTPUT_DIR = GeminiHR_Generate_questions.OUTPUT_DIR

    # Clear previous output files if needed
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Process all resumes and generate .docx and .pdf files
    GeminiHR_Generate_questions.process_resumes()

    # Collect generated file names
    generated_files = [
        file for file in os.listdir(OUTPUT_DIR)
        if file.endswith('.pdf') or file.endswith('.docx')
    ]

    return JSONResponse(content={"generated_files": generated_files}, status_code=200)