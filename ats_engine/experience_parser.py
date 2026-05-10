import re
from datetime import datetime

CURRENT_YEAR = datetime.now().year


# ────────────────────────────────────────────────────────────────────────────
# Extract Experience Blocks
#
# Root cause of old code failing:
#   extract_text() flattens the resume into a single line / removes real \n
#   so patterns using ^ line-anchors never match.
#
# Fix: use \b word-boundary patterns that work on ANY text format.
# ────────────────────────────────────────────────────────────────────────────
def extract_experience_blocks(text):
    experiences = []

    # ── Pattern A: YYYY – YYYY  or  YYYY – Present  (works anywhere in text) ──
    pattern_year = r"\b(\d{4})\s*[-–—]\s*(\d{4}|[Pp]resent)\b"
    for match in re.finditer(pattern_year, text):
        start_year = int(match.group(1))
        end_raw = match.group(2)
        end_year = CURRENT_YEAR if end_raw.lower() == "present" else int(end_raw)

        if 1970 <= start_year <= CURRENT_YEAR and start_year <= end_year <= CURRENT_YEAR + 1:
            experiences.append({
                "company": "Unknown",
                "start_year": start_year,
                "end_year": end_year,
                "duration_years": max(end_year - start_year, 0)
            })

    # ── Pattern B: "X months" internship / short stints ──
    pattern_months = r"\b(\d+)\s*months?\b"
    for match in re.finditer(pattern_months, text, re.IGNORECASE):
        months = int(match.group(1))
        if 1 <= months <= 24:
            experiences.append({
                "company": "Internship",
                "start_year": CURRENT_YEAR,
                "end_year": CURRENT_YEAR,
                "duration_years": round(months / 12, 2)
            })

    # ── Deduplicate by (start_year, end_year) ──
    seen = set()
    unique = []
    for exp in experiences:
        key = (exp["start_year"], exp["end_year"])
        if key not in seen:
            seen.add(key)
            unique.append(exp)

    return unique


# ────────────────────────────────────────────────────────────────────────────
# Calculate Total Experience (years)
# Uses timeline SPAN to avoid double-counting overlapping roles.
# ────────────────────────────────────────────────────────────────────────────
def calculate_total_experience(experiences):
    if not experiences:
        return 0

    real_exp = [e for e in experiences if e["company"] != "Internship"]
    internship_frac = sum(
        e["duration_years"] for e in experiences if e["company"] == "Internship"
    )

    if real_exp:
        earliest = min(e["start_year"] for e in real_exp)
        latest = max(e["end_year"] for e in real_exp)
        total = max(latest - earliest, 0) + internship_frac
    else:
        total = internship_frac

    return round(total, 2)


# ────────────────────────────────────────────────────────────────────────────
# Extract Roles
# ────────────────────────────────────────────────────────────────────────────
ROLES = [
    "developer", "engineer", "manager", "analyst", "intern",
    "architect", "consultant", "designer", "lead", "scientist",
    "technician", "inspector", "planner", "operator"
]

def extract_roles(text):
    text_lower = text.lower()
    return list({role for role in ROLES if role in text_lower})


# ────────────────────────────────────────────────────────────────────────────
# Detect Gaps
# ────────────────────────────────────────────────────────────────────────────
def detect_gaps(experiences):
    gaps = []
    sorted_exp = sorted(
        [e for e in experiences if e["company"] != "Internship"],
        key=lambda x: x["start_year"]
    )
    for i in range(1, len(sorted_exp)):
        prev_end = sorted_exp[i - 1]["end_year"]
        curr_start = sorted_exp[i]["start_year"]
        if curr_start > prev_end:
            gaps.append({
                "gap_years": curr_start - prev_end,
                "between": f"{prev_end}-{curr_start}"
            })
    return gaps


# ────────────────────────────────────────────────────────────────────────────
# Detect Overlaps
# ────────────────────────────────────────────────────────────────────────────
def detect_overlaps(experiences):
    overlaps = []
    for i in range(len(experiences)):
        for j in range(i + 1, len(experiences)):
            if experiences[i]["end_year"] > experiences[j]["start_year"]:
                overlaps.append((experiences[i], experiences[j]))
    return overlaps


# ────────────────────────────────────────────────────────────────────────────
# Role Relevance Score
# ────────────────────────────────────────────────────────────────────────────
ROLE_SIMILARITY = {
    "developer": ["engineer", "programmer", "architect"],
    "engineer": ["developer", "designer", "scientist", "technician"],
    "analyst": ["scientist", "inspector", "planner"],
    "manager": ["lead", "consultant"],
}

def calculate_relevance(candidate_roles, job_role):
    if not candidate_roles:
        return 0
    score = sum(
        1 if role == job_role else 0.7 if role in ROLE_SIMILARITY.get(job_role, []) else 0
        for role in candidate_roles
    )
    return round((score / len(candidate_roles)) * 100, 2)