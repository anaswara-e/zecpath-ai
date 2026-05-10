# tests/test_fairness_engine.py
# Day 15 — Tests for Fairness, Normalization & Bias Reduction

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ats_engine.fairness_engine import (
    normalize_scores,
    mask_sensitive_data,
    reduce_keyword_bias,
    generate_fair_score,
    evaluate_bias_indicators,
    apply_fairness_pipeline,
)
from parsers.normalization import normalize_resume_text, normalize_jd_text


# ── Test 1: Score Normalization ───────────────────────────────────────────────
def test_normalization():
    candidates = [
        {"candidate_id": "C1", "final_score": 50},
        {"candidate_id": "C2", "final_score": 100}
    ]
    result = normalize_scores(candidates)
    assert result[0]["normalized_score"] == 0.0,   "Min score should normalize to 0"
    assert result[1]["normalized_score"] == 100.0, "Max score should normalize to 100"
    print("PASS  test_normalization")


def test_normalization_equal_scores():
    candidates = [
        {"candidate_id": "C1", "final_score": 75},
        {"candidate_id": "C2", "final_score": 75}
    ]
    result = normalize_scores(candidates)
    assert result[0]["normalized_score"] == 100.0
    print("PASS  test_normalization_equal_scores")


# ── Test 2: Sensitive Data Masking ───────────────────────────────────────────
def test_mask_sensitive_data():
    candidate = {
        "candidate_id": "C1",
        "name":         "Arjun Nair",
        "gender":       "Male",
        "location":     "Bangalore",
        "final_score":  82
    }
    masked = mask_sensitive_data(candidate)
    assert masked["name"]     == "MASKED"
    assert masked["gender"]   == "MASKED"
    assert masked["location"] == "MASKED"
    assert masked["candidate_id"] == "C1"       # non-sensitive kept
    assert masked["final_score"]  == 82          # score kept
    print("PASS  test_mask_sensitive_data")


# ── Test 3: Keyword Bias Reduction ───────────────────────────────────────────
def test_reduce_keyword_bias():
    # High skill, low semantic → blended down
    score = reduce_keyword_bias(skill_score=90, semantic_score=40)
    assert score == round(0.6 * 40 + 0.4 * 90, 2)
    print(f"PASS  test_reduce_keyword_bias  → fair={score}")


def test_reduce_keyword_bias_equal():
    score = reduce_keyword_bias(skill_score=70, semantic_score=70)
    assert score == 70.0
    print(f"PASS  test_reduce_keyword_bias_equal  → fair={score}")


# ── Test 4: Fair Score Generator ─────────────────────────────────────────────
def test_generate_fair_score():
    candidate = {
        "candidate_id": "C1",
        "final_score":  85,
        "breakdown": {
            "skill_score":    80,
            "semantic_score": 60
        }
    }
    result = generate_fair_score(candidate)
    assert "fair_score" in result
    expected = round(0.6 * 60 + 0.4 * 80, 2)
    assert result["fair_score"] == expected
    print(f"PASS  test_generate_fair_score  → fair={result['fair_score']}")


# ── Test 5: Bias Indicator Evaluation ────────────────────────────────────────
def test_evaluate_bias_indicators_keyword():
    candidate = {
        "final_score": 85,
        "fair_score":  70,
        "breakdown": {
            "skill_score":      90,
            "semantic_score":   40,   # gap > 30 → KEYWORD_BIAS
            "education_score":  70,
            "experience_score": 80
        }
    }
    warnings = evaluate_bias_indicators(candidate)
    types = [w["type"] for w in warnings]
    assert "KEYWORD_BIAS" in types
    print(f"PASS  test_evaluate_bias_indicators_keyword  → {types}")


def test_evaluate_bias_no_warnings():
    candidate = {
        "final_score": 78,
        "fair_score":  76,
        "breakdown": {
            "skill_score":      75,
            "semantic_score":   70,
            "education_score":  80,
            "experience_score": 85
        }
    }
    warnings = evaluate_bias_indicators(candidate)
    assert warnings == []
    print("PASS  test_evaluate_bias_no_warnings")


# ── Test 6: Resume Text Normalization ────────────────────────────────────────
def test_normalize_resume_text():
    raw = "Professional Experience: Python, Machine Learning. Work Experience in AI"
    normalized = normalize_resume_text(raw)
    assert "experience" in normalized
    assert "professional experience" not in normalized
    assert "work experience" not in normalized
    print(f"PASS  test_normalize_resume_text")


def test_normalize_jd_text():
    jd = "Academic Background: B.Tech in Mechanical. Skill Set: AutoCAD, SolidWorks"
    normalized = normalize_jd_text(jd)
    assert "education" in normalized
    assert "skills" in normalized
    print(f"PASS  test_normalize_jd_text")


# ── Test 7: Full Pipeline ─────────────────────────────────────────────────────
def test_full_fairness_pipeline():
    candidates = [
        {
            "candidate_id": "C1",
            "final_score":  88,
            "name":         "Arjun",
            "location":     "Bangalore",
            "breakdown": {
                "skill_score":      85,
                "semantic_score":   70,
                "education_score":  90,
                "experience_score": 100
            }
        },
        {
            "candidate_id": "C2",
            "final_score":  72,
            "name":         "Priya",
            "location":     "Mumbai",
            "breakdown": {
                "skill_score":      65,
                "semantic_score":   60,
                "education_score":  75,
                "experience_score": 85
            }
        },
        {
            "candidate_id": "C3",
            "final_score":  45,
            "name":         "Rahul",
            "location":     "Chennai",
            "breakdown": {
                "skill_score":      40,
                "semantic_score":   35,
                "education_score":  60,
                "experience_score": 50
            }
        }
    ]

    result = apply_fairness_pipeline(candidates)

    for c in result:
        assert "normalized_score" in c
        assert "fair_score"       in c
        assert "masked_profile"   in c
        assert "bias_warnings"    in c

    # Highest final score → normalized = 100
    top = max(result, key=lambda x: x["final_score"])
    assert top["normalized_score"] == 100.0

    # Lowest final score → normalized = 0
    bot = min(result, key=lambda x: x["final_score"])
    assert bot["normalized_score"] == 0.0

    print("PASS  test_full_fairness_pipeline")
    print("\nFull pipeline output sample:")
    from ats_engine.fairness_engine import print_fairness_result
    print_fairness_result(result[0])


# ── Run all ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("Day 15 — Fairness & Bias Reduction Tests")
    print("=" * 55)
    test_normalization()
    test_normalization_equal_scores()
    test_mask_sensitive_data()
    test_reduce_keyword_bias()
    test_reduce_keyword_bias_equal()
    test_generate_fair_score()
    test_evaluate_bias_indicators_keyword()
    test_evaluate_bias_no_warnings()
    test_normalize_resume_text()
    test_normalize_jd_text()
    test_full_fairness_pipeline()
    print("\nAll Day 15 tests passed!")