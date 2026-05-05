from ats_engine.semantic_matcher import compute_similarity

def test_similarity():

    text1 = "Python developer"
    text2 = "Backend engineer using Python"

    score = compute_similarity(text1, text2)

    print("Similarity:", score)

    assert score > 0.5