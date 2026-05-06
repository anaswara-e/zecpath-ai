DEFAULT_WEIGHTS = {
    "skills": 0.35,
    "experience": 0.25,
    "education": 0.15,
    "semantic": 0.25
}


def normalize(score):
    return score / 100 if score else 0


def calculate_ats_score(candidate, weights=DEFAULT_WEIGHTS):

    skill_score = normalize(candidate.get("skill_score", 0))
    exp_score = normalize(candidate.get("experience_score", 0))
    edu_score = normalize(candidate.get("education_score", 0))
    semantic_score = normalize(candidate.get("semantic_score", 0))

    final_score = (
        weights["skills"] * skill_score +
        weights["experience"] * exp_score +
        weights["education"] * edu_score +
        weights["semantic"] * semantic_score
    )

    return round(final_score * 100, 2)


def generate_candidate_score(candidate):

    final_score = calculate_ats_score(candidate)

    return {
        "candidate_id": candidate.get("candidate_id"),
        "final_score": final_score,
        "breakdown": {
            "skill_score": candidate.get("skill_score", 0),
            "experience_score": candidate.get("experience_score", 0),
            "education_score": candidate.get("education_score", 0),
            "semantic_score": candidate.get("semantic_score", 0)
        }
    }