# ats_engine/fairness_engine.py
# Day 15 — Fairness, Normalization & Bias Reduction
# Connected to: ats_scorer.py, skill_extractor.py, rankingengine.py

import re

# ── Score Normalization (min-max across candidate pool) ───────────────────────
def normalize_scores(candidate_scores):
    """
    Apply min-max normalization across all candidates.
    Adds 'normalized_score' field to each candidate dict.
    Works with output from generate_candidate_score() in ats_scorer.py
    """
    if not candidate_scores:
        return candidate_scores

    scores = [c.get("final_score", 0) for c in candidate_scores]
    min_score = min(scores)
    max_score = max(scores)

    if max_score == min_score:
        # All candidates have same score — give everyone 100
        for c in candidate_scores:
            c["normalized_score"] = 100.0
        return candidate_scores

    for c in candidate_scores:
        raw = c.get("final_score", 0)
        c["normalized_score"] = round(
            ((raw - min_score) / (max_score - min_score)) * 100, 2
        )
    return candidate_scores


# ── Sensitive Data Masking ────────────────────────────────────────────────────
SENSITIVE_FIELDS = ["name", "gender", "age", "photo", "location", "address",
                    "phone", "email", "nationality", "religion", "marital_status"]

def mask_sensitive_data(candidate):
    """
    Remove or mask non-essential personal attributes to prevent bias.
    Candidate dict comes from parsed resume data.
    """
    masked = candidate.copy()
    for field in SENSITIVE_FIELDS:
        if field in masked:
            masked[field] = "MASKED"
    masked["masked_profile"] = {
        "name":     candidate.get("name",     "MASKED"),
        "gender":   candidate.get("gender",   "MASKED"),
        "age":      candidate.get("age",      "MASKED"),
        "location": candidate.get("location", "MASKED"),
        "photo":    candidate.get("photo",    "MASKED"),
    }
    return masked


# ── Keyword Bias Reduction ────────────────────────────────────────────────────
def reduce_keyword_bias(skill_score, semantic_score):
    """
    Blend keyword matching (skill_score) with semantic understanding.
    Reduces over-dependence on exact keyword hits.
    Uses scores from skill_extractor.py and semantic_matcher.py.
    """
    adjusted = (0.6 * semantic_score) + (0.4 * skill_score)
    return round(adjusted, 2)


# ── Education Prestige Bias Reduction ────────────────────────────────────────
def reduce_education_bias(education_score, base_cap=85.0):
    """
    Cap education score to avoid over-rewarding institution prestige.
    Education score comes from ats_scorer.py dimension_scores.
    """
    return round(min(education_score, base_cap), 2)


# ── Experience Gap Penalty Reduction ─────────────────────────────────────────
def reduce_gap_penalty(experience_score, gap_years):
    """
    Reduce harsh penalties for career gaps (e.g. maternity, illness).
    Only apply a soft penalty: 2 points per gap year, max -10 points.
    """
    penalty = min(gap_years * 2, 10)
    return round(max(experience_score - penalty, 0), 2)


# ── Fair Candidate Score Generator ───────────────────────────────────────────
def generate_fair_score(candidate):
    """
    Generate a bias-reduced composite score.
    Uses skill_score and semantic_score from ats_scorer.py breakdown.
    Adds 'fair_score' field to the candidate dict.
    """
    skill_score    = candidate.get("skill_score",    0) or \
                     candidate.get("breakdown", {}).get("skill_score", 0)
    semantic_score = candidate.get("semantic_score", 0) or \
                     candidate.get("breakdown", {}).get("semantic_score", 0)

    fair_score = reduce_keyword_bias(skill_score, semantic_score)
    candidate["fair_score"] = fair_score
    return candidate


# ── Bias Indicators Evaluator ─────────────────────────────────────────────────
def evaluate_bias_indicators(candidate):
    """
    Check for known bias patterns in the candidate's score breakdown.
    Returns a list of bias warnings for recruiter transparency.
    """
    warnings = []
    breakdown = candidate.get("breakdown", {})

    skill_score    = breakdown.get("skill_score",      0)
    semantic_score = breakdown.get("semantic_score",   0)
    edu_score      = breakdown.get("education_score",  0)
    exp_score      = breakdown.get("experience_score", 0)
    final_score    = candidate.get("final_score",      0)
    fair_score     = candidate.get("fair_score",       final_score)

    # Keyword over-dependence
    if skill_score > 0 and semantic_score > 0:
        gap = abs(skill_score - semantic_score)
        if gap > 30:
            warnings.append({
                "type":    "KEYWORD_BIAS",
                "detail":  f"Skill score ({skill_score}) differs from semantic "
                           f"score ({semantic_score}) by {gap:.1f} points — "
                           "possible keyword over-matching."
            })

    # Education prestige bias
    if edu_score > 85:
        warnings.append({
            "type":   "EDUCATION_PRESTIGE_BIAS",
            "detail": f"Education score ({edu_score}) is very high — "
                      "may over-reward institution prestige."
        })

    # Fair score vs final score divergence
    score_diff = abs(final_score - fair_score)
    if score_diff > 15:
        warnings.append({
            "type":   "SCORE_DIVERGENCE",
            "detail": f"Final score ({final_score}) and fair score "
                      f"({fair_score}) differ by {score_diff:.1f} — "
                      "review scoring weights."
        })

    return warnings


# ── Full Fairness Pipeline ────────────────────────────────────────────────────
def apply_fairness_pipeline(candidates):
    """
    Run the complete Day 15 fairness pipeline on a list of candidates.
    Each candidate should be output from generate_candidate_score() + ranking.

    Steps:
      1. Normalize scores across the pool
      2. Generate fair (bias-reduced) scores
      3. Mask sensitive fields
      4. Evaluate bias indicators

    Returns enriched candidate list ready for recruiter output.
    """
    # Step 1 — Normalize
    candidates = normalize_scores(candidates)

    for c in candidates:
        # Step 2 — Fair score
        c = generate_fair_score(c)

        # Step 3 — Bias indicators
        c["bias_warnings"] = evaluate_bias_indicators(c)

        # Step 4 — Mask sensitive data (non-destructive)
        c["masked_profile"] = {
            "name":     c.get("name",     "MASKED"),
            "gender":   c.get("gender",   "MASKED"),
            "age":      c.get("age",      "MASKED"),
            "location": c.get("location", "MASKED"),
        }

    return candidates


# ── Pretty Print Fairness Result ──────────────────────────────────────────────
def print_fairness_result(candidate):
    print(f"\nCandidate     : {candidate.get('candidate_id', 'N/A')}")
    print(f"Final Score   : {candidate.get('final_score', 0)}")
    print(f"Normalized    : {candidate.get('normalized_score', 'N/A')}")
    print(f"Fair Score    : {candidate.get('fair_score', 'N/A')}")

    print("Masked Profile:")
    for k, v in candidate.get("masked_profile", {}).items():
        print(f"  {k:<10}: {v}")

    warnings = candidate.get("bias_warnings", [])
    if warnings:
        print("Bias Warnings:")
        for w in warnings:
            print(f"  [{w['type']}] {w['detail']}")
    else:
        print("Bias Warnings : None detected")