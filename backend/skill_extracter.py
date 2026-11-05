import re


# Canonical skill names and their alternative spellings
SKILL_ALIASES = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],

    "C": ["c programming"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "c sharp"],

    "SQL": ["sql", "structured query language"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo"],
    "SQLite": ["sqlite"],
    "Oracle": ["oracle database"],

    "Flask": ["flask"],
    "Django": ["django"],
    "FastAPI": ["fastapi", "fast api"],
    "Spring Boot": ["spring boot", "springboot"],
    "Spring Framework": ["spring framework"],

    "REST API": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "restful services"
    ],

    "GraphQL": ["graphql"],
    "Microservices": ["microservices", "micro services"],
    "JDBC": ["jdbc"],
    "Hibernate": ["hibernate"],
    "JPA": ["jpa", "java persistence api"],

    "Git": ["git"],
    "GitHub": ["github"],
    "GitLab": ["gitlab"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Linux": ["linux"],

    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "React": ["react", "react.js", "reactjs"],
    "Angular": ["angular"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "Express.js": ["express.js", "expressjs", "express"],

    "Machine Learning": [
        "machine learning",
        "ml"
    ],
    "Deep Learning": ["deep learning", "dl"],
    "Data Science": ["data science"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Generative AI": ["generative ai", "gen ai", "genai"],
    "Large Language Models": [
        "large language models",
        "large language model",
        "llms",
        "llm"
    ],
    "Prompt Engineering": ["prompt engineering"],

    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],
    "NumPy": ["numpy"],
    "Pandas": ["pandas"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "Scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "OpenCV": ["opencv", "open cv"],
    "YOLOv8": ["yolov8", "yolo v8"],

    "Apache Spark": ["apache spark", "spark"],
    "Hadoop": ["hadoop"],
    "Apache Kafka": ["apache kafka", "kafka"],
    "AWS": ["aws", "amazon web services"],
    "Microsoft Azure": ["microsoft azure", "azure"],
    "Google Cloud": ["google cloud", "gcp"],

    "Data Structures and Algorithms": [
        "data structures and algorithms",
        "data structures",
        "algorithms",
        "dsa"
    ],
    "Object-Oriented Programming": [
        "object-oriented programming",
        "object oriented programming",
        "oops",
        "oop"
    ],
    "Problem Solving": ["problem solving", "problem-solving"],
    "API Testing": ["api testing"],
    "Postman": ["postman"],
    "Agile": ["agile"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous deployment"]
}


def extract_skills(text):
    """
    Extract recognized technical skills from text.

    Returns canonical skill names without duplicates.
    Matching is case-insensitive and supports skill aliases.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    # Normalize text to lowercase
    text = text.lower()

    found_skills = []

    # Check every canonical skill and its aliases
    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            # Escape special regex characters in the alias
            escaped_alias = re.escape(alias.lower())

            # Allow flexible whitespace between words
            escaped_alias = escaped_alias.replace(r"\ ", r"\s+")

            # Require boundaries to avoid partial-word matches
            pattern = r"(?<!\w)" + escaped_alias + r"(?!\w)"

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills


if __name__ == "__main__":

    sample_text = """
    Developed backend applications using PYTHON and JavaScript.

    Used JS, PostgreSQL, RESTful APIs, Spring Boot,
    Docker, GitHub, and scikit learn.

    Familiar with Machine Learning and AWS.
    """

    skills = extract_skills(sample_text)

    print("Skills found:")

    for skill in skills:
        print("-", skill)
