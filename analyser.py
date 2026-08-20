import re


# Technical skills supported by our resume screening system
TECHNICAL_SKILLS = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "flask",
    "django",
    "sql",
    "mysql",
    "mongodb",
    "machine learning",
    "deep learning",
    "data science",
    "artificial intelligence",
    "git",
    "github",
    "docker",
    "react",
    "node.js",
    "c++",
    "c",
    "data structures",
    "algorithms",
    "rest api",
    "aws",
    "azure",
    "ibm cloud"
]


def clean_text(text):
    """Clean and normalize text."""

    text = text.lower()

    # Replace special characters with spaces
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def skill_found(skill, text):
    """Check whether a complete skill exists in the text."""

    skill = skill.lower()

    # Special handling for skills containing symbols
    if skill in ["c", "c++", "node.js"]:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
    else:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"

    return re.search(pattern, text) is not None


def analyse_resume(resume_text, job_description):

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    matched_keywords = []
    missing_keywords = []

    # Find only skills mentioned in the job description
    required_skills = []

    for skill in TECHNICAL_SKILLS:

        if skill_found(skill, job_description):
            required_skills.append(skill)

    # Compare resume with required skills
    for skill in required_skills:

        if skill_found(skill, resume_text):
            matched_keywords.append(skill)
        else:
            missing_keywords.append(skill)

    # Calculate score
    total_skills = len(required_skills)

    if total_skills > 0:
        score = (len(matched_keywords) / total_skills) * 100
    else:
        score = 0

    # Compatibility message
    if score >= 80:
        message = "Excellent match! Your resume strongly matches the job requirements."

    elif score >= 60:
        message = "Good match! Your resume matches many of the required skills."

    elif score >= 40:
        message = "Moderate match. Consider adding more relevant skills."

    else:
        message = "Low match. Your resume needs more skills related to this job."

    # Improvement suggestions
    suggestions = []

    for skill in missing_keywords:
        suggestions.append(
            f"Consider adding {skill} if you have relevant experience."
        )

    return {
        "score": round(score, 2),
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "message": message,
        "suggestions": suggestions,
        "total_required": total_skills
    }


# Test the analyzer directly
if __name__ == "__main__":

    resume = """
    Python developer with experience in Flask,
    HTML, CSS, JavaScript and SQL.
    """

    job = """
    Looking for a Python developer with Flask,
    JavaScript, HTML, CSS, SQL and Machine Learning skills.
    """

    result = analyse_resume(resume, job)

    print("\n===== SMART RESUME ANALYSIS =====")

    print("Match Score:", result["score"], "%")

    print("\nMatched Skills:")
    for skill in result["matched_keywords"]:
        print("✓", skill)

    print("\nMissing Skills:")
    for skill in result["missing_keywords"]:
        print("!", skill)

    print("\nMessage:")
    print(result["message"])