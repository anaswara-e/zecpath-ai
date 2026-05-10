# tests/test_ranking_engine.py
# Import from rankingengine (no underscore) — matches your actual filename

from ats_engine.rankingengine import (
    rank_candidates,
    classify_candidate,
    apply_shortlisting,
    get_top_candidates,
    ranking_pipeline,
    generate_recruiter_output,
    THRESHOLDS
)

SAMPLE_CANDIDATES = [
    {"candidate_id": "C1", "final_score": 88},
    {"candidate_id": "C2", "final_score": 72},
    {"candidate_id": "C3", "final_score": 45},
    {"candidate_id": "C4", "final_score": 80},
]


def test_ranking_order():
    import copy
    ranked = rank_candidates(copy.deepcopy(SAMPLE_CANDIDATES))
    assert ranked[0]["candidate_id"] == "C1"
    assert ranked[1]["candidate_id"] == "C4"


def test_rank_assigned():
    import copy
    ranked = rank_candidates(copy.deepcopy(SAMPLE_CANDIDATES))
    for i, c in enumerate(ranked, start=1):
        assert c["rank"] == i


def test_classify_shortlisted():
    assert classify_candidate(THRESHOLDS["shortlist"]) == "Shortlisted"
    assert classify_candidate(100) == "Shortlisted"


def test_classify_review():
    assert classify_candidate(THRESHOLDS["review"]) == "Review"
    assert classify_candidate(60) == "Review"


def test_classify_rejected():
    assert classify_candidate(THRESHOLDS["review"] - 1) == "Rejected"
    assert classify_candidate(0) == "Rejected"


def test_apply_shortlisting():
    import copy
    ranked = rank_candidates(copy.deepcopy(SAMPLE_CANDIDATES))
    result = apply_shortlisting(ranked)
    statuses = {c["candidate_id"]: c["status"] for c in result}
    assert statuses["C1"] == "Shortlisted"
    assert statuses["C4"] == "Shortlisted"
    assert statuses["C2"] == "Review"
    assert statuses["C3"] == "Rejected"


def test_get_top_candidates():
    import copy
    ranked = apply_shortlisting(rank_candidates(copy.deepcopy(SAMPLE_CANDIDATES)))
    top = get_top_candidates(ranked, top_n=2)
    assert len(top) == 2
    assert top[0]["candidate_id"] == "C1"


def test_recruiter_output_structure():
    import copy
    ranked = apply_shortlisting(rank_candidates(copy.deepcopy(SAMPLE_CANDIDATES)))
    output = generate_recruiter_output("J456", ranked)
    assert "job_id" in output
    assert "summary" in output
    assert "top_candidates" in output
    summary = output["summary"]
    assert summary["total_candidates"] == 4
    assert summary["shortlisted"] == 2
    assert summary["review"] == 1
    assert summary["rejected"] == 1


def test_full_pipeline():
    import copy
    result = ranking_pipeline(copy.deepcopy(SAMPLE_CANDIDATES), job_id="J456", top_n=5)
    assert "ranked_list" in result
    assert "top_candidates" in result
    assert "recruiter_summary" in result
    assert result["ranked_list"][0]["rank"] == 1