# ats_engine/ats_scorer.py
# Task 13 — Enhanced ATS Scorer
# Output format matches screenshot exactly

from datetime import datetime

# ── Default Weights ───────────────────────────────────────────────────────────
DEFAULT_WEIGHTS = {
    "skills":     0.30,
    "experience": 0.35,
    "education":  0.10,
    "semantic":   0.25
}

SHORTLIST_THRESHOLD = 60.0
AUTO_REJECT_THRESHOLD = 30.0
SCORER_VERSION = "v1.0.0"


# ── Normalize ─────────────────────────────────────────────────────────────────
def normalize(score):
    return (score / 100.0) if score else 0.0


# ── Weight redistribution when a dimension is missing ─────────────────────────
def redistribute_weights(weights, availability):
    lost   = sum(v for k, v in weights.items() if not availability.get(k, True))
    avail  = {k: v for k, v in weights.items() if availability.get(k, True)}
    total  = sum(avail.values())
    result = {}
    for k, v in weights.items():
        if not availability.get(k, True):
            result[k] = 0.0
        else:
            result[k] = v + (v / total) * lost if total else 0.0
    return result


# ── Must-have skills check ────────────────────────────────────────────────────
def check_must_haves(resume_skills, skill_list):
    """
    skill_list: list of dicts like {"name": "Python", "importance": "Must-have"}
    resume_skills: list of skill name strings
    """
    must_haves = [s["name"] for s in skill_list if s.get("importance") == "Must-have"]
    resume_set = set(s.lower() for s in resume_skills)
    matched    = [s for s in must_haves if s.lower() in resume_set]
    missing    = [s for s in must_haves if s.lower() not in resume_set]
    return {
        "total_must_haves":    len(must_haves),
        "must_haves_matched":  len(matched),
        "must_haves_missing":  missing,
        "hard_reject":         len(missing) > 0
    }


# ── Skill scoring with importance weighting ───────────────────────────────────
def score_skills_detailed(resume_skills, skill_list):
    """
    Must-have match = +10 pts each
    Nice-to-have miss = -3 pts each
    Returns 0-100 score + detail breakdown
    """
    resume_set = set(s.lower() for s in resume_skills)

    matched_skills  = []
    missing_skills  = []
    points          = 0
    max_points      = 0

    for item in skill_list:
        name       = item["name"]
        importance = item.get("importance", "Nice-to-have")

        if importance == "Must-have":
            max_points += 10
            if name.lower() in resume_set:
                points += 10
                matched_skills.append({"skill": name, "importance": importance, "points": 10})
            else:
                missing_skills.append({"skill": name, "importance": importance, "penalty": -5})
        else:  # Nice-to-have
            if name.lower() in resume_set:
                points += 5
                matched_skills.append({"skill": name, "importance": importance, "points": 5})
            else:
                points -= 3
                missing_skills.append({"skill": name, "importance": importance, "penalty": -3})

    # Normalise to 0-100
    base = max_points if max_points > 0 else 1
    raw_score = max(0, min(100, (points / base) * 100))

    match_rate = round(len(matched_skills) / len(skill_list) * 100, 1) if skill_list else 0

    return round(raw_score, 1), {
        "matched_skills":        matched_skills,
        "missing_skills":        missing_skills,
        "total_candidate_skills": len(resume_skills),
        "total_jd_skills":       len(skill_list),
        "match_rate":            match_rate
    }


# ── Experience scoring ────────────────────────────────────────────────────────
def score_experience_detailed(total_years, exp_range, experiences):
    min_y = exp_range.get("min_years", 0)
    max_y = exp_range.get("max_years", 99)

    if total_years >= min_y and total_years <= max_y:
        exp_score = 100
    elif total_years < min_y:
        exp_score = max(0, (total_years / min_y) * 100)
    else:
        exp_score = max(70, 100 - (total_years - max_y) * 5)

    return round(exp_score, 1), {
        "total_years":     round(total_years, 1),
        "required_range":  exp_range,
        "trajectory":      "upward",
        "gaps":            0,
        "overlaps":        0,
        "recommendation":  "STRONG_MATCH" if exp_score >= 80 else "MODERATE_MATCH"
    }


# ── Education scoring ─────────────────────────────────────────────────────────
def score_education_detailed(education_data):
    """
    education_data: dict with keys like degree, level, institution, cgpa
    """
    score = 60  # baseline

    level = education_data.get("level", "").lower()
    if "masters" in level or "m.tech" in level or "mtech" in level:
        score += 20
    elif "bachelors" in level or "b.tech" in level or "btech" in level or "b.e" in level:
        score += 10

    tier = education_data.get("institution_tier", "")
    if tier == "Tier-1":
        score += 10
    elif tier == "Tier-2":
        score += 5

    cgpa = education_data.get("cgpa", 0) or 0
    if cgpa >= 8.5:
        score += 10
    elif cgpa >= 7.5:
        score += 5

    return round(min(score, 100), 1)


# ── Main ATS Score Calculator ─────────────────────────────────────────────────
def calculate_ats_score(candidate, weights=None):
    """
    candidate keys:
        skill_score, experience_score, education_score, semantic_score  (0-100 each)
        resume_skills     → list of skill strings
        must_have_skills  → list of {"name":..., "importance":...} dicts
        candidate_id      → string

    Returns full structured result matching JSON + screenshot format.
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS.copy()

    # ── Availability ──────────────────────────────────────────────────────────
    availability = {
        "skills":     candidate.get("skill_score")     is not None,
        "experience": candidate.get("experience_score") is not None,
        "education":  candidate.get("education_score")  is not None,
        "semantic":   candidate.get("semantic_score")   is not None,
    }

    raw = {
        "skills":     candidate.get("skill_score",      0) or 0,
        "experience": candidate.get("experience_score", 0) or 0,
        "education":  candidate.get("education_score",  0) or 0,
        "semantic":   candidate.get("semantic_score",   0) or 0,
    }

    weight_redistributed = not all(availability.values())
    adj_weights = redistribute_weights(weights, availability) if weight_redistributed else weights.copy()

    # ── Compute weighted total ────────────────────────────────────────────────
    final_score = 0.0
    dimensions  = {}

    for dim in ["skills", "experience", "education", "semantic"]:
        score    = raw[dim]
        eff_w    = adj_weights[dim]
        final_score += normalize(score) * eff_w

        dimensions[dim] = {
            "score":          round(score, 1),
            "weight":         round(weights[dim], 2),
            "adjusted_weight": round(eff_w, 3),
            "available":      availability[dim],
        }

    final_score = round(final_score * 100, 1)

    # ── Must-have check ───────────────────────────────────────────────────────
    skill_list   = candidate.get("must_have_skills", [])
    resume_skills = candidate.get("resume_skills", [])
    must_have    = check_must_haves(resume_skills, skill_list)

    # ── Decision ──────────────────────────────────────────────────────────────
    if must_have["hard_reject"] or final_score < AUTO_REJECT_THRESHOLD:
        decision = "REJECTED"
        reason   = (
            f"Missing must-have skills "
            f"({must_have['must_haves_matched']}/{must_have['total_must_haves']} matched)"
            if must_have["hard_reject"]
            else f"Score {final_score} below auto-reject threshold {AUTO_REJECT_THRESHOLD}"
        )
    elif final_score >= SHORTLIST_THRESHOLD:
        decision = "SHORTLISTED"
        reason   = f"Score {final_score} meets threshold {SHORTLIST_THRESHOLD}"
    else:
        decision = "REVIEW"
        reason   = f"Score {final_score} below shortlist threshold {SHORTLIST_THRESHOLD}"

    confidence = round(final_score / 100, 4)

    return {
        "ats_score":       final_score,
        "decision":        decision,
        "decision_reason": reason,
        "confidence":      confidence,
        "dimension_scores": dimensions,
        "must_have_check": must_have,
        "scoring_config": {
            "weights":    {k: round(v, 3) for k, v in weights.items()},
            "thresholds": {
                "minimum_score": SHORTLIST_THRESHOLD,
                "auto_reject":   AUTO_REJECT_THRESHOLD
            }
        },
        "weight_redistributed":  weight_redistributed,
        "adjusted_weights":      {k: round(v, 3) for k, v in adj_weights.items()},
        "metadata": {
            "scored_at":                  datetime.now().isoformat(),
            "scorer_version":             SCORER_VERSION,
            "dimensions_available":       sum(1 for v in availability.values() if v),
            "weight_redistribution_applied": weight_redistributed
        }
    }


# ── Pretty Printer — matches screenshot exactly ───────────────────────────────
def print_ats_result(result):
    print(f"\nATS Score:   {result['ats_score']}/100")
    print(f"Decision:    {result['decision']}")
    print(f"Reason:      {result['decision_reason']}")
    print(f"Confidence:  {result['confidence']}")

    print(f"\nDimension scores:")
    for dim, d in result["dimension_scores"].items():
        print(
            f"  {dim:<12} "
            f"score={d['score']:<6} "
            f"weight={d['weight']:<6} "
            f"adjusted={d['adjusted_weight']:<8} "
            f"available={d['available']}"
        )

    mh = result["must_have_check"]
    if mh["total_must_haves"] > 0:
        print(f"\nMust-have check:")
        print(f"  Matched: {mh['must_haves_matched']}/{mh['total_must_haves']}")
        print(f"  Hard reject: {mh['hard_reject']}")

    if result["weight_redistributed"]:
        print(f"\nWeight redistribution: True")
        for dim, w in result["adjusted_weights"].items():
            avail = result["dimension_scores"][dim]["available"]
            print(f"  {dim:<12} available={avail}  adjusted_weight={w:.3f}")


# ── Backward-compatible wrapper for main.py ───────────────────────────────────
def generate_candidate_score(candidate, weights=None):
    result = calculate_ats_score(candidate, weights)
    # keep old keys so main.py / ranking_engine still work
    result["final_score"] = result["ats_score"]
    result["breakdown"]   = {
        "skill_score":      candidate.get("skill_score",      0),
        "experience_score": candidate.get("experience_score", 0),
        "education_score":  candidate.get("education_score",  0),
        "semantic_score":   candidate.get("semantic_score",   0),
    }
    return result