import re

# -------------------------------
# Skill Dictionary (Mechanical + Programming + Soft Skills)
# -------------------------------
SKILL_DB = {

    # Programming (⚠️ ADDED FIX)
    "python": ["python", "py"],
    "c++": ["c++", "cpp"],
    "matlab": ["matlab"],

    # CAD & Design
    "cad": ["cad"],
    "solidworks": ["solidworks"],
    "autocad": ["autocad"],
    "catia": ["catia"],
    "nx": ["nx", "siemens nx"],
    "creo": ["creo", "proe", "pro engineer"],
    "fusion360": ["fusion 360"],
    "ansys": ["ansys"],
    "abaqus": ["abaqus"],

    # Core Mechanical
    "product_design": ["product design", "design"],
    "mechanical_design": ["mechanical design"],
    "machine_design": ["machine design"],
    "design_engineering": ["design engineering"],

    # Manufacturing
    "manufacturing": ["manufacturing"],
    "production": ["production"],
    "fabrication": ["fabrication"],
    "machining": ["machining"],
    "casting": ["casting"],
    "forging": ["forging"],
    "cnc": ["cnc", "cnc machining"],
    "3d_printing": ["3d printing", "additive manufacturing"],

    # Analysis & Simulation
    "fea": ["fea", "finite element analysis"],
    "cfd": ["cfd", "computational fluid dynamics"],
    "simulation": ["simulation"],
    "thermal_analysis": ["thermal analysis"],

    # Materials
    "materials": ["materials", "material science"],
    "material_selection": ["material selection"],
    "metallurgy": ["metallurgy"],

    # Product Lifecycle
    "plm": ["plm", "product lifecycle management"],
    "bom": ["bom", "bill of materials"],
    "dfma": ["dfma", "design for manufacturing"],
    "dfm": ["dfm"],
    "dfa": ["dfa"],

    # Testing & Validation
    "prototyping": ["prototyping"],
    "testing": ["testing", "product testing"],
    "validation": ["validation", "design validation"],
    "quality": ["quality", "quality control"],

    # Tools & Documentation
    "technical_drawing": ["technical drawing"],
    "gdandt": ["gd&t", "geometric dimensioning and tolerancing"],
    "documentation": ["documentation", "technical documentation"],

    # Soft Skills
    "communication": ["communication"],
    "teamwork": ["teamwork", "team collaboration"],
    "problem_solving": ["problem solving"],
    "innovation": ["innovation", "creativity"]
}

# -------------------------------
# Skill Stacks
# -------------------------------
SKILL_STACKS = {
    "design_tools": ["autocad", "solidworks", "catia"],
}

# -------------------------------
# Clean Text
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------------
# Extract Skills (FIXED MATCHING)
# -------------------------------
def extract_skills(text):
    text = clean_text(text)
    found_skills = []

    for skill, variants in SKILL_DB.items():
        for variant in variants:
            # ✅ STRONG WORD MATCH (FIX)
            if f" {variant} " in f" {text} ":
                found_skills.append(skill)
                break

    # Skill stacks
    for stack, skills in SKILL_STACKS.items():
        if stack in text:
            found_skills.extend(skills)

    return list(set(found_skills))


# -------------------------------
# Confidence Score
# -------------------------------
def calculate_confidence(skill, text):
    text = text.lower()

    # check all variants instead of only main skill name
    variants = SKILL_DB.get(skill, [skill])

    count = 0
    for v in variants:
        count += text.count(v)

    if count >= 3:
        return 0.9
    elif count == 2:
        return 0.8
    elif count == 1:
        return 0.7
    else:
        return 0.0


# -------------------------------
# Final Output
# -------------------------------
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