from skill_extracter import SKILL_ALIASES
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def normalize_skill(skill):

    skill = skill.strip().lower()

    for canonical, aliases in SKILL_ALIASES.items():

        all_names = [canonical] + aliases

        for name in all_names:

            if skill == name.lower():
                return canonical

    return skill.title()
SKILL_CATEGORIES = {
    "Programming": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#"
    ],

    "Backend Development": [
        "Flask", "Django", "FastAPI", "Spring Boot",
        "Spring Framework", "REST API", "Microservices"
    ],

    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB",
        "SQLite", "Oracle", "JPA", "Hibernate"
    ],

    "Data Science and AI": [
        "Machine Learning", "Deep Learning", "Data Science",
        "Data Analysis", "Generative AI", "TensorFlow",
        "PyTorch", "Scikit-learn", "Pandas", "NumPy"
    ],

    "Data Visualization": [
        "Power BI", "Tableau", "Matplotlib", "Seaborn", "Excel"
    ],

    "Cloud and DevOps": [
        "AWS", "Microsoft Azure", "Google Cloud",
        "Docker", "Kubernetes", "CI/CD", "Linux"
    ],

    "Development Tools": [
        "Git", "GitHub", "GitLab", "Postman", "API Testing"
    ]
}
def generate_recommendations(missing_skills):

    recommendations = {}

    for skill in missing_skills:

        category_found = False

        for category, skills in SKILL_CATEGORIES.items():

            if skill in skills:

                if category not in recommendations:
                    recommendations[category] = []

                recommendations[category].append(skill)

                category_found = True
                break

        if not category_found:

            if "Other Skills" not in recommendations:
                recommendations["Other Skills"] = []

            recommendations["Other Skills"].append(skill)

    return recommendations
def calculate_text_similarity(resume_text, job_description):

    # Convert text into numerical vectors
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform([
        resume_text,
        job_description
    ])

    # Calculate cosine similarity
    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    # Convert score into percentage
    similarity_score = similarity[0][0] * 100

    return round(similarity_score, 2)
def compare_skills(resume_skills, job_skills):

    # Handle empty or invalid inputs
    resume_skills = resume_skills if isinstance(resume_skills, list) else []
    job_skills = job_skills if isinstance(job_skills, list) else []

    # Normalize resume skills
    resume_skill_map = set()

    for skill in resume_skills:

        if isinstance(skill, str) and skill.strip():
            resume_skill_map.add(normalize_skill(skill))

    # Normalize job skills and remove duplicates
    unique_job_skills = []

    for skill in job_skills:

        if isinstance(skill, str) and skill.strip():

            normalized_skill = normalize_skill(skill)

            if normalized_skill not in unique_job_skills:
                unique_job_skills.append(normalized_skill)

    matched_skills = []
    missing_skills = []

    # Compare skills
    for skill in unique_job_skills:

        if skill in resume_skill_map:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Calculate match score
    total_job_skills = len(unique_job_skills)

    if total_job_skills > 0:
        match_score = (len(matched_skills) / total_job_skills) * 100
    else:
        match_score = 0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(match_score, 2),
        "total_required_skills": total_job_skills,
        "matched_skills_count": len(matched_skills),
        "missing_skills_count": len(missing_skills),
        "recommendations": missing_skills.copy(),
        "recommendation_categories": generate_recommendations(missing_skills)
    }

if __name__ == "__main__":

    resume_text = """
    I have experience in Python, Java, SQL and Flask.
    I have worked on REST API development and MySQL databases.
    """

    job_description = """
    We are looking for a Python developer.
    Knowledge of SQL, Flask, REST API development
    and database management is required.
    """

    score = calculate_text_similarity(
        resume_text,
        job_description
    )

    print("Text Similarity Score:", score, "%")