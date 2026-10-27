def extract_skills(text):

    skills_list = [
        "Python",
        "Java",
        "SQL",
        "MySQL",
        "Flask",
        "Django",
        "Spring Boot",
        "REST API",
        "Git",
        "GitHub",
        "Machine Learning",
        "Deep Learning",
        "Power BI",
        "AWS",
        "HTML",
        "CSS",
        "JavaScript",
        "NumPy",
        "Pandas",
        "TensorFlow",
        "PyTorch"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills
if __name__ == "__main__":

    sample_text = """
    I know Python, Java, SQL, Flask and Spring Boot.
    I have used Git and MySQL.
    """

    skills = extract_skills(sample_text)

    print("Skills found:", skills)