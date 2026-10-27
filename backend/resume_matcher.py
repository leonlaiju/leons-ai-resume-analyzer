def compare_skills(resume_skills, job_skills):

    matched_skills = []
    missing_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(job_skills) > 0:
        match_score = (len(matched_skills) / len(job_skills)) * 100
    else:
        match_score = 0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(match_score, 2)
    }
if __name__ == "__main__":

    resume_skills = ["Python", "Java", "SQL", "Flask", "Git"]

    job_skills = ["Python", "Flask", "SQL", "AWS", "Django"]

    result = compare_skills(resume_skills, job_skills)

    print(result)