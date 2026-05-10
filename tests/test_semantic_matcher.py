# tests/test_semantic_matcher.py

from ats_engine.semantic_matcher import compute_tfidf_similarity, match_resume_to_jd


def test_similar_texts():
    score = compute_tfidf_similarity("python machine learning", "python machine learning")
    assert score == 100.0


def test_different_texts():
    score = compute_tfidf_similarity("python machine learning", "solidworks cad design")
    assert score < 50


def test_empty_text():
    score = compute_tfidf_similarity("", "python")
    assert score == 0.0


def test_match_resume_to_jd():
    resume = {
        "skills": ["python", "machine_learning"],
        "projects": [{"description": "Built ML model for predictive maintenance"}]
    }
    jd = {
        "required_skills": ["python", "machine_learning", "data_analysis"],
        "job_description_text": "Looking for python developer with machine learning skills"
    }
    result = match_resume_to_jd(resume, jd)
    assert "skill_similarity" in result
    assert "project_similarity" in result
    assert "final_similarity_score" in result
    assert result["final_similarity_score"] >= 0