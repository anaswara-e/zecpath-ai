import re

DEGREE_MAP = {
    "btech": "B.Tech",
    "b.tech": "B.Tech",
    "b e": "B.Tech",
    "b.e": "B.Tech",
    "mtech": "M.Tech",
    "m.tech": "M.Tech",
    "diploma": "Diploma",
    "iti": "ITI",
    "mba": "MBA"
}

FIELDS = {
    "mechanical": "Mechanical Engineering",
    "production": "Production Engineering",
    "manufacturing": "Manufacturing Engineering",
    "thermal": "Thermal Engineering",
    "automobile": "Automobile Engineering",
    "mechatronics": "Mechatronics Engineering"
}

CERT_CATEGORIES = {
    "autocad": "Design",
    "solidworks": "Design",
    "catia": "Design",
    "ansys": "Simulation",
    "matlab": "Simulation",
    "cnc": "Manufacturing",
    "quality": "Quality",
    "six sigma": "Quality",
    "lean": "Manufacturing",
    "python": "Programming",
    "aws": "Cloud"
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\.]", " ", text)
    return text



def extract_education(text):
    text = clean_text(text)
    education = []


    year_match = re.findall(r"(20\d{2})", text)
    year = year_match[0] if year_match else None

  
    field = "Not Specified"
    for key, value in FIELDS.items():
        if key in text:
            field = value
            break


    for key, value in DEGREE_MAP.items():
        if key in text:
            education.append({
                "degree": value,
                "field": field,
                "institution": "Not Extracted",
                "year": year
            })

    return education


def extract_certifications(text):
    text = clean_text(text)
    certs = []

    for keyword, category in CERT_CATEGORIES.items():
        if keyword in text:
            certs.append({
                "name": keyword.title(),
                "category": category
            })

    return certs


def calculate_education_relevance(candidate_degree, required_degree):

    if not candidate_degree or not required_degree:
        return 0

    candidate_degree = candidate_degree.lower()
    required_degree = required_degree.lower()

    if candidate_degree == required_degree:
        return 1.0
    elif candidate_degree in ["m.tech"] and required_degree in ["b.tech"]:
        return 0.8
    else:
        return 0.5


def calculate_certification_relevance(certifications, job_skills):

    score = 0

    for cert in certifications:
        if cert["category"].lower() in [s.lower() for s in job_skills]:
            score += 1

    if len(certifications) == 0:
        return 0

    return round((score / len(certifications)) * 100, 2)