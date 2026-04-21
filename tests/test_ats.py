from ats_engine.ats import calculate_score

def test_ats_score():
    score = calculate_score(["python", "react"], ["python", "react", "node"])
    assert score > 0