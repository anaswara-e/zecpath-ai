import re
from datetime import datetime

def extract_experience_blocks(text):
    pattern = r"([A-Za-z\s]+)\s*\((\d{4})\s*[-–]\s*(\d{4}|Present)\)"
    matches = re.findall(pattern, text)

    experiences = []

    for match in matches:
        company = match[0].strip()
        start_year = int(match[1])

        if match[2].lower() == "present":
            end_year = datetime.now().year
        else:
            end_year = int(match[2])

        duration = end_year - start_year

        experiences.append({
            "company": company,
            "start_year": start_year,
            "end_year": end_year,
            "duration_years": duration
        })

    return experiences


def extract_roles(text):
    roles = ["developer", "engineer", "manager", "analyst", "intern"]
    found_roles = []

    for role in roles:
        if role in text.lower():
            found_roles.append(role)

    return list(set(found_roles))


def calculate_total_experience(experiences):
    return sum([exp["duration_years"] for exp in experiences])


def detect_gaps(experiences):
    gaps = []

    sorted_exp = sorted(experiences, key=lambda x: x["start_year"])

    for i in range(1, len(sorted_exp)):
        prev_end = sorted_exp[i - 1]["end_year"]
        curr_start = sorted_exp[i]["start_year"]

        if curr_start > prev_end:
            gaps.append({
                "gap_years": curr_start - prev_end,
                "between": f"{prev_end}-{curr_start}"
            })

    return gaps

def detect_overlaps(experiences):
    overlaps = []

    for i in range(len(experiences)):
        for j in range(i + 1, len(experiences)):
            if experiences[i]["end_year"] > experiences[j]["start_year"]:
                overlaps.append((experiences[i], experiences[j]))

    return overlaps

ROLE_SIMILARITY = {
    "developer": ["engineer", "programmer"],
    "engineer": ["developer"],
    "analyst": ["data analyst", "business analyst"],
    "manager": ["team lead", "project manager"]
}


def calculate_relevance(candidate_roles, job_role):
    score = 0

    for role in candidate_roles:
        if role == job_role:
            score += 1
        elif role in ROLE_SIMILARITY.get(job_role, []):
            score += 0.7

    if len(candidate_roles) == 0:
        return 0

    return round((score / len(candidate_roles)) * 100, 2)