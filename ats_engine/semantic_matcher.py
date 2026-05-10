"""
semantic_matcher.py — lightweight version using TF-IDF + cosine similarity.
No model downloads, no GPU/RAM issues. Drop-in replacement for the
SentenceTransformer version.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ── Text preprocessing ────────────────────────────────────────────────────────

def preprocess(text: str) -> str:
    """Lowercase, remove punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ── Core similarity ───────────────────────────────────────────────────────────

def compute_tfidf_similarity(text1: str, text2: str) -> float:
    """Return cosine similarity (0–100) between two text strings."""
    t1 = preprocess(text1)
    t2 = preprocess(text2)

    if not t1 or not t2:
        return 0.0

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([t1, t2])
        score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        return round(float(score) * 100, 2)
    except Exception:
        return 0.0


# ── Project text helper ───────────────────────────────────────────────────────

def get_projects_text(resume: dict) -> str:
    projects = resume.get("projects", [])
    return " ".join(p.get("description", "") for p in projects)


# ── Main matching function ────────────────────────────────────────────────────

def match_resume_to_jd(resume: dict, jd: dict) -> dict:
    """
    Compare a resume dict against a JD dict and return similarity scores.

    resume dict keys used:
        skills      → list of skill strings
        experience  → list of experience dicts
        projects    → list of {"description": str}

    jd dict keys used:
        required_skills         → list of skill strings
        job_description_text    → full JD text string
    """
    jd_text = jd.get("job_description_text", "")

    # 1. Skills text similarity
    resume_skills_text = " ".join(resume.get("skills", []))
    jd_skills_text = " ".join(jd.get("required_skills", []))
    skill_sim = compute_tfidf_similarity(resume_skills_text, jd_skills_text)

    # 2. Projects / experience text vs full JD
    projects_text = get_projects_text(resume)
    project_sim = compute_tfidf_similarity(projects_text, jd_text)

    # 3. Weighted final similarity
    # Skills similarity carries more weight for ATS purposes
    final_sim = round((skill_sim * 0.6) + (project_sim * 0.4), 2)

    return {
        "skill_similarity": skill_sim,
        "project_similarity": project_sim,
        "final_similarity_score": final_sim
    }