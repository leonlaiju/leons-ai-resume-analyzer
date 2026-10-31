from flask import Flask, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
from resume_parser import extract_text_from_pdf
from skill_extracter import extract_skills
from resume_matcher import compare_skills
import os

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500"]
    }
})

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


@app.route("/")
def home():
    return "Leon's AI Resume Analyzer is running!"


@app.route("/upload", methods=["POST"])
def upload_resume():

    file = request.files["resume"]

    upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "uploads"
    )

    file_path = os.path.join(upload_folder, file.filename)

    file.save(file_path)

    text = extract_text_from_pdf(file_path)

    return text

@app.route("/job-description", methods=["POST"])
def job_description():

    data = request.get_json()

    job_description = data["job_description"]

    return job_description

@app.route("/extract-skills", methods=["POST"])
def extract_resume_skills():
    data = request.get_json()

    text = data["text"]

    skills = extract_skills(text)

    return {"skills": skills}

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    data = request.get_json()

    resume_text = data["resume_text"]
    job_description = data["job_description"]

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    result = compare_skills(resume_skills, job_skills)

    return result
@app.route("/analyze-pdf", methods=["POST"])
def analyze_pdf():

    # Check whether a resume was uploaded
    if "resume" not in request.files:
        return {"error": "Please upload a resume PDF"}, 400

    file = request.files["resume"]

    # Check whether a file was selected
    if file.filename == "":
        return {"error": "No file selected"}, 400

    # Check the file extension
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Please upload a PDF file"}, 400

    # Check the job description
    job_description = request.form.get("job_description", "")

    if not job_description.strip():
        return {"error": "Please provide a job description"}, 400

    try:
        # Create the uploads directory if it doesn't exist
        upload_folder = Path(__file__).resolve().parent.parent / "uploads"
        upload_folder.mkdir(parents=True, exist_ok=True)

        # Generate a safe, unique filename
        filename = secure_filename(file.filename)

        if not filename:
            return {"error": "Invalid filename"}, 400

        file_path = upload_folder / filename

        # Save the uploaded PDF
        file.save(file_path)

        # Extract text from the PDF
        resume_text = extract_text_from_pdf(str(file_path))

        # Check whether the PDF contains readable text
        if not resume_text.strip():
            return {
                "error": "No readable text found in the PDF. It may be scanned."
            }, 400

        # Extract skills from the resume and job description
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        # Compare the skills
        result = compare_skills(resume_skills, job_skills)

        # Return the analysis report
        return {
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "match_score": result["match_score"]
        }

    except Exception:
        app.logger.exception("Resume analysis failed")

        return {
            "error": "Unable to analyze this PDF. Please check the file and try again."
        }, 400



if __name__ == "__main__":
    app.run(debug=True)
