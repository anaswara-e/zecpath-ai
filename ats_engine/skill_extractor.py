import re

# Skill Dictionary (Mechanical + Common)
SKILL_DB = {
    "python": ["python", "py"],
    "sql": ["sql", "mysql"],
    "excel": ["excel", "ms excel"],
    "communication": ["communication", "communication skills"],
    "leadership": ["leadership", "team leadership"],

    # Mechanical Skills
    "autocad": ["autocad"],
    "solidworks": ["solidworks"],
    "ansys": ["ansys"],
    "catia": ["catia"],
    "matlab": ["matlab"],
    "thermodynamics": ["thermodynamics"],
    "manufacturing": ["manufacturing"],
    "mechanical design": ["mechanical design", "design engineering"]
}

# Skill Stacks (optional simple)

SKILL_STACKS = {
    "design_tools": ["autocad", "solidworks", "catia"],
}

# Clean Text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text

# Extract Skills

def extract_skills(text):
    text = clean_text(text)
    found_skills = []

    # Check normal skills
    for skill, variants in SKILL_DB.items():
        for variant in variants:
            if variant in text:
                found_skills.append(skill)
                break

    # Check stacks
    for stack, skills in SKILL_STACKS.items():
        if stack in text:
            found_skills.extend(skills)

    return list(set(found_skills))  # remove duplicates

# Confidence Score

def calculate_confidence(skill, text):
    text = text.lower()
    count = text.count(skill)

    if count >= 3:
        return 0.9
    elif count == 2:
        return 0.8
    elif count == 1:
        return 0.7
    else:
        return 0.0

# Final Output

def extract_skills_with_confidence(text):
    skills = extract_skills(text)

    results = []
    for skill in skills:
        confidence = calculate_confidence(skill, text)

        results.append({
            "skill": skill,
            "confidence": round(confidence, 2)
        })

    return results