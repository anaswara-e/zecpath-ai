import re

# Mechanical Engineering Skills Database
SKILLS_DB = [
    "autocad", "solidworks", "catia",
    "ansys", "manufacturing",
    "thermodynamics", "design",
    "production", "quality control",
    "maintenance", "mechanical"
]


# Clean and normalize text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = " ".join(text.split())
    return text


# Extract role
def extract_role(text):
    roles = [
        "mechanical engineer",
        "design engineer",
        "production engineer",
        "maintenance engineer",
        "quality engineer"
    ]

    for role in roles:
        if role in text:
            return role

    return "mechanical engineer"  # default


# Extract skills
def extract_skills(text):
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))  # remove duplicates


# Extract experience
def extract_experience(text):
    match = re.search(r"(\d+\+?\s*years?)", text)

    if match:
        return match.group(1)

    return "not specified"


# Extract education
def extract_education(text):
    education_keywords = [
        "btech", "b.e", "mtech",
        "diploma", "degree"
    ]

    for edu in education_keywords:
        if edu in text:
            return edu

    return "not specified"


# MAIN FUNCTION (used by test file)
def parse_jd(text):
    text = clean_text(text)

    result = {
        "role": extract_role(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text)
    }

    return result