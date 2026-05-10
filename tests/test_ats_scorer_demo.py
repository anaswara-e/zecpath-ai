# tests/test_ats_scorer_demo.py
# Run: python tests/test_ats_scorer_demo.py
# Produces the exact 3-test output shown in Task 13 screenshot

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ats_engine.ats_scorer import calculate_ats_score, print_ats_result, DEFAULT_WEIGHTS

SEP = "=" * 65

# ── Shared resume data (from your JSON) ──────────────────────────────────────
RESUME_SKILLS = [
    "RCC Design", "Site Supervision", "BOQ", "AutoCAD",
    "STAAD.Pro", "Formwork", "Concreting", "Primavera P6",
    "MS Excel", "IS 456"
]

JD_SKILL_LIST = [
    {"name": "RCC Design",        "importance": "Must-have"},
    {"name": "AutoCAD",           "importance": "Must-have"},
    {"name": "Site Supervision",  "importance": "Must-have"},
    {"name": "BOQ",               "importance": "Must-have"},
    {"name": "Safety Compliance", "importance": "Nice-to-have"},
    {"name": "Primavera",         "importance": "Nice-to-have"},
    {"name": "MS Project",        "importance": "Nice-to-have"},
]

# ─────────────────────────────────────────────────────────────────────────────
# TEST 1 — Default weights + must-have check
# ─────────────────────────────────────────────────────────────────────────────
print(SEP)
print("TEST 1: Default weights + must-have skills check")
print(SEP)

candidate1 = {
    "candidate_id":     "C001",
    "skill_score":      69.1,
    "experience_score": 100.0,
    "education_score":  81.5,
    "semantic_score":   56.7,
    "resume_skills":    RESUME_SKILLS,
    "must_have_skills": JD_SKILL_LIST,
}

result1 = calculate_ats_score(candidate1, DEFAULT_WEIGHTS)
print_ats_result(result1)


# ─────────────────────────────────────────────────────────────────────────────
# TEST 2 — Custom weights (experience-heavy)
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("TEST 2: Custom weights (experience-heavy)")
print(SEP)

experience_heavy = {
    "skills":     0.20,
    "experience": 0.50,
    "education":  0.10,
    "semantic":   0.20
}

candidate2 = {
    "candidate_id":     "C001",
    "skill_score":      69.1,
    "experience_score": 100.0,
    "education_score":  81.5,
    "semantic_score":   56.7,
}

result2 = calculate_ats_score(candidate2, experience_heavy)
print_ats_result(result2)


# ─────────────────────────────────────────────────────────────────────────────
# TEST 3 — Missing education section → weight redistribution
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{SEP}")
print("TEST 3: Resume with missing education section")
print(SEP)

candidate3 = {
    "candidate_id":     "C002",
    "skill_score":      69.1,
    "experience_score": 100.0,
    "education_score":  None,    # ← missing
    "semantic_score":   56.7,
}

result3 = calculate_ats_score(candidate3, DEFAULT_WEIGHTS)
print_ats_result(result3)