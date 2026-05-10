# ats_engine/ranking_engine.py
# Day 14 – Candidate Ranking & Shortlisting

# -------------------------------
# Threshold Configuration
# -------------------------------
THRESHOLDS = {
    "shortlist": 75,
    "review": 50
}


# -------------------------------
# Sort Candidates by Score
# -------------------------------
def rank_candidates(candidates):
    """
    Sort candidates in descending order of final_score and assign ranks.
    """
    ranked = sorted(
        candidates,
        key=lambda x: x.get("final_score", 0),
        reverse=True
    )
    for idx, candidate in enumerate(ranked, start=1):
        candidate["rank"] = idx
    return ranked


# -------------------------------
# Candidate Classification
# -------------------------------
def classify_candidate(score):
    if score >= THRESHOLDS["shortlist"]:
        return "Shortlisted"
    elif score >= THRESHOLDS["review"]:
        return "Review"
    else:
        return "Rejected"


# -------------------------------
# Apply Shortlisting Logic
# -------------------------------
def apply_shortlisting(candidates):
    for candidate in candidates:
        score = candidate.get("final_score", 0)
        candidate["status"] = classify_candidate(score)
    return candidates


# -------------------------------
# Top Candidate Selector
# -------------------------------
def get_top_candidates(candidates, top_n=5):
    """
    Return only Shortlisted candidates, up to top_n.
    Falls back to Review zone if no shortlisted candidates exist.
    """
    shortlisted = [c for c in candidates if c.get("status") == "Shortlisted"]
    if shortlisted:
        return shortlisted[:top_n]
    # fallback: return top_n overall if none shortlisted
    return candidates[:top_n]


# -------------------------------
# Recruiter-Friendly Summary
# -------------------------------
def generate_recruiter_output(job_id, candidates):
    """
    Produces a clean summary + top candidates for recruiter dashboards.
    """
    shortlisted = [c for c in candidates if c.get("status") == "Shortlisted"]
    review      = [c for c in candidates if c.get("status") == "Review"]
    rejected    = [c for c in candidates if c.get("status") == "Rejected"]

    top = shortlisted[:5] if shortlisted else candidates[:5]

    return {
        "job_id": job_id,
        "summary": {
            "total_candidates": len(candidates),
            "shortlisted": len(shortlisted),
            "review": len(review),
            "rejected": len(rejected)
        },
        "top_candidates": [
            {
                "candidate_id": c.get("candidate_id"),
                "score": c.get("final_score"),
                "status": c.get("status")
            }
            for c in top
        ]
    }


# -------------------------------
# Complete Pipeline
# -------------------------------
def ranking_pipeline(candidates, job_id="N/A", top_n=5):
    """
    Full pipeline:
      1. Rank by score
      2. Classify each candidate
      3. Extract top candidates
      4. Build recruiter-friendly output
    """
    ranked      = rank_candidates(candidates)
    shortlisted = apply_shortlisting(ranked)
    top         = get_top_candidates(shortlisted, top_n=top_n)
    recruiter   = generate_recruiter_output(job_id, shortlisted)

    return {
        "ranked_list":       shortlisted,
        "top_candidates":    top,
        "recruiter_summary": recruiter
    }