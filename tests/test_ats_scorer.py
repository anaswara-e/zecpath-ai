from ats_engine.ats_scorer import calculate_ats_score

def test_ats_score():

    candidate = {
        "skill_score": 80,
        "experience_score": 70,
        "education_score": 60,
        "semantic_score": 75
    }

    score = calculate_ats_score(candidate)

    print(score)

    assert score > 0