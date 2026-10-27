import re


def extract_skills(text):

    skills_list = [
        "Python",
        "Java",
        "JavaScript",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Flask",
        "Django",
        "FastAPI",
        "Spring Boot",
        "REST API",
        "Git",
        "GitHub",
        "Machine Learning",
        "Deep Learning",
        "Data Science",
        "Data Analysis",
        "Power BI",
        "Tableau",
        "Excel",
        "AWS",
        "HTML",
        "CSS",
        "NumPy",
        "Pandas",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "OpenCV",
        "YOLOv8",
        "Docker",
        "Kubernetes",
        "Linux",
        "Apache Spark",
        "Hadoop",
        "Generative AI",
        "Large Language Models",
        "Prompt Engineering"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_list:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


if __name__ == "__main__":

    sample_text = """
    Javascript,PyTHon,Sql
    """

    skills = extract_skills(sample_text)

    print("Skills found:", skills)