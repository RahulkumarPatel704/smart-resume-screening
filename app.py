from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

from resume_parser import extract_resume_text
from analyser import analyse_resume


app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None

    if request.method == "POST":

        resume = request.files.get("resume")
        job_description = request.form.get("job_description", "")

        # Check resume
        if not resume or resume.filename == "":
            error = "Please upload a resume."

        elif not allowed_file(resume.filename):
            error = "Only PDF and DOCX files are allowed."

        # Check job description
        elif not job_description.strip():
            error = "Please enter a job description."

        else:

            filename = secure_filename(resume.filename)

            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            try:
                # Save resume
                resume.save(file_path)

                # Extract resume text
                resume_text = extract_resume_text(file_path)

                # Analyse resume
                result = analyse_resume(
                    resume_text,
                    job_description
                )

            except Exception as e:
                error = f"Something went wrong: {str(e)}"

    return render_template(
        "index.html",
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)