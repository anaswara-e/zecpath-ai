# parsers/normalization.py
# Day 15 — Resume Text Normalization
# Used BEFORE skill_extractor.py and semantic_matcher.py to standardize input

import re

# ── Section heading aliases → standard names ──────────────────────────────────
HEADING_REPLACEMENTS = {
    "professional experience": "experience",
    "work experience":         "experience",
    "employment history":      "experience",
    "career history":          "experience",
    "job history":             "experience",

    "academic background":     "education",
    "educational background":  "education",
    "academic qualifications": "education",
    "qualifications":          "education",

    "skill set":               "skills",
    "technical skills":        "skills",
    "core competencies":       "skills",
    "key skills":              "skills",
    "areas of expertise":      "skills",

    "certifications":          "certifications",
    "certificates":            "certifications",

    "projects":                "projects",
    "key projects":            "projects",
    "project experience":      "projects",

    "summary":                 "summary",
    "professional summary":    "summary",
    "career objective":        "summary",
    "objective":               "summary",
}

# ── Degree alias normalization ────────────────────────────────────────────────
DEGREE_REPLACEMENTS = {
    "b.tech":  "bachelor of technology",
    "b.e.":    "bachelor of engineering",
    "be":      "bachelor of engineering",
    "btech":   "bachelor of technology",
    "m.tech":  "master of technology",
    "mtech":   "master of technology",
    "m.e.":    "master of engineering",
    "mba":     "master of business administration",
    "phd":     "doctor of philosophy",
    "ph.d":    "doctor of philosophy",
}


# ── Main normalization function ───────────────────────────────────────────────
def normalize_resume_text(text):
    """
    Standardize raw resume text before passing to parsers.
    Called by main.py before extract_skills() and extract_experience_blocks().

    Steps:
      1. Lowercase
      2. Remove special characters (keep . , - for dates/degrees)
      3. Normalize whitespace
      4. Standardize section headings
      5. Standardize degree names
    """
    # Step 1 — lowercase
    text = text.lower()

    # Step 2 — remove special chars (keep . , - / & + for skills/dates)
    text = re.sub(r"[^a-z0-9\s\.\,\-\/\&\+]", " ", text)

    # Step 3 — normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Step 4 — standardize section headings
    for alias, standard in HEADING_REPLACEMENTS.items():
        text = text.replace(alias, standard)

    # Step 5 — standardize degree names
    for alias, standard in DEGREE_REPLACEMENTS.items():
        # whole word match
        text = re.sub(rf"\b{re.escape(alias)}\b", standard, text)

    return text.strip()


# ── Normalize a full candidate dict ───────────────────────────────────────────
def normalize_candidate(candidate):
    """
    Normalize all text fields in a candidate dict.
    Pass the raw parsed resume dict through this before scoring.
    """
    normalized = candidate.copy()

    text_fields = ["raw_text", "summary", "skills_text",
                   "experience_text", "education_text", "projects_text"]

    for field in text_fields:
        if field in normalized and isinstance(normalized[field], str):
            normalized[field] = normalize_resume_text(normalized[field])

    # Normalize skill list items
    if "skills" in normalized and isinstance(normalized["skills"], list):
        normalized["skills"] = [s.lower().strip() for s in normalized["skills"]]

    return normalized


# ── Normalize JD text ─────────────────────────────────────────────────────────
def normalize_jd_text(text):
    """
    Same normalization applied to Job Description text.
    Ensures resume and JD are on equal footing before matching.
    """
    return normalize_resume_text(text)