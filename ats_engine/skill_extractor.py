import re

# -------------------------------
# Skill Dictionary - EXPANDED with AI/ML + Software skills
# -------------------------------
SKILL_DB = {

    # Programming
    "python": ["python", "py"],
    "c++": ["c++", "cpp"],
    "matlab": ["matlab"],
    "r": [" r ", "r programming"],
    "java": ["java"],
    "sql": ["sql"],

    # AI / ML Frameworks  ← ADDED (was completely missing before)
    "machine_learning": ["machine learning", "ml", "supervised learning", "unsupervised learning",
                          "supervised", "unsupervised", "reinforcement learning"],
    "deep_learning": ["deep learning", "dl", "neural network", "neural networks"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"],
    "scikit_learn": ["scikit learn", "sklearn", "scikit-learn"],
    "keras": ["keras"],
    "nlp": ["nlp", "natural language processing"],
    "computer_vision": ["computer vision", "cv", "image processing"],
    "data_analysis": ["data analysis", "data analytics", "statistical analysis", "statistics"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "iot": ["iot", "internet of things"],
    "predictive_maintenance": ["predictive maintenance", "predictive analytics"],
    "automation": ["automation", "automated"],
    "ai": ["artificial intelligence", " ai ", "ai/ml"],
    "mlops": ["mlops", "ml pipeline", "machine learning pipeline"],

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
    "product_design": ["product design"],
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
    "dfma": ["dfma", "design for manufacturing and assembly"],
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
    "problem_solving": ["problem solving", "analytical thinking"],
    "innovation": ["innovation", "creativity"],
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
    text = re.sub(r"[^a-z0-9\s\+\&]", " ", text)  # keep + and & for skills like c++ and gd&t
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------------------------------
# Extract Skills - improved matching
# -------------------------------
def extract_skills(text):
    cleaned = clean_text(text)
    found_skills = set()

    for skill, variants in SKILL_DB.items():
        for variant in variants:
            variant_clean = variant.strip()
            # word boundary match using spaces (handles multi-word phrases too)
            padded_text = f" {cleaned} "
            padded_variant = f" {variant_clean} "
            if padded_variant in padded_text:
                found_skills.add(skill)
                break

    # Skill stacks
    for stack, skills in SKILL_STACKS.items():
        if stack in cleaned:
            for s in skills:
                found_skills.add(s)

    return list(found_skills)

# -------------------------------
# Skill Extraction with Confidence
# -------------------------------

def extract_skills_with_confidence(text):
    """
    Extract skills with confidence scores
    """

    skills = extract_skills(text)

    result = []

    for skill in skills:
        result.append({
            "skill": skill,
            "confidence": 0.95
        })

    return result

# -------------------------------
# Confidence Score
# -------------------------------
def calculate_confidence(skill, text):
    text_lower = text.lower()
    variants = SKILL_DB.get(skill, [skill])

    count = sum(text_lower.count(v) for v in variants)

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