# tests/test_api.py
# Day 16 — API Tests using FastAPI TestClient

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.main_api import app
import io

client = TestClient(app)
SEP = "=" * 55

# ── shared state across tests ─────────────────────────────────────────────────
state = {}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"
    print("PASS  GET  /health")


def test_home():
    r = client.get("/")
    assert r.status_code == 200
    assert "Zecpath" in r.json()["message"]
    print("PASS  GET  /")


def test_create_job():
    r = client.post("/jobs/create", json={
        "job_title":        "AI/ML Mechanical Engineer",
        "required_skills":  "python machine learning tensorflow data analysis iot",
        "responsibilities": "develop ml models analyze sensor data",
        "requirements":     "btech mechanical 2-6 years experience"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "success"
    assert "job_id" in data
    state["job_id"] = data["job_id"]
    print(f"PASS  POST /jobs/create  → job_id={state['job_id']}")


def test_upload_resume():
    # Create a minimal in-memory resume text file
    resume_text = b"""NAME: Arun Krishnan
SKILLS
python machine learning tensorflow data analysis iot predictive maintenance
EXPERIENCE
AI Engineer
GE Digital India
2020 - Present
- Developed ML models for predictive maintenance
EDUCATION
Bachelor of Technology in Mechanical Engineering
NIT Karnataka 2016-2020
"""
    r = client.post(
        "/resume/upload",
        files={"file": ("test_resume.txt", io.BytesIO(resume_text), "text/plain")},
        data={"job_id": state.get("job_id", "J000"), "candidate_id": "C_TEST"}
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "success"
    assert "resume_id" in data
    state["resume_id"] = data["resume_id"]
    print(f"PASS  POST /resume/upload  → resume_id={state['resume_id']}")


def test_upload_invalid_type():
    r = client.post(
        "/resume/upload",
        files={"file": ("bad.exe", io.BytesIO(b"test"), "application/octet-stream")},
        data={"job_id": "J000", "candidate_id": "C000"}
    )
    data = r.json()
    assert data["error_code"] == "INVALID_INPUT"
    print("PASS  POST /resume/upload  invalid file → INVALID_INPUT")


def test_parse_resume():
    r = client.post("/resume/parse", json={
        "resume_id":    state["resume_id"],
        "candidate_id": "C_TEST"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "completed"
    assert "parsed_profile" in data
    assert "skills" in data["parsed_profile"]
    # Store candidate_id as resume_id for scoring
    state["candidate_id"] = state["resume_id"]
    print(f"PASS  POST /resume/parse  → "
          f"skills={data['parsed_profile']['total_skills']} "
          f"exp={data['parsed_profile']['total_years']}yrs")


def test_parse_not_found():
    r = client.post("/resume/parse", json={"resume_id": "R_FAKE"})
    data = r.json()
    assert data["error_code"] == "NOT_FOUND"
    print("PASS  POST /resume/parse  invalid id → NOT_FOUND")


def test_ats_score():
    r = client.post("/ats/score", json={
        "candidate_id": state["candidate_id"],
        "job_id":       state["job_id"]
    })
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "success"
    assert "final_score" in data
    assert "breakdown" in data
    state["final_score"] = data["final_score"]
    print(f"PASS  POST /ats/score  → score={data['final_score']}  decision={data['decision']}")


def test_ats_score_not_found():
    r = client.post("/ats/score", json={
        "candidate_id": "C_FAKE",
        "job_id":       state["job_id"]
    })
    data = r.json()
    assert data["error_code"] == "NOT_FOUND"
    print("PASS  POST /ats/score  invalid candidate → NOT_FOUND")


def test_shortlist():
    r = client.post("/ats/shortlist", json={
        "job_id":    state["job_id"],
        "threshold": 60.0,
        "top_n":     5
    })
    assert r.status_code == 200
    data = r.json()
    assert "total_candidates" in data
    assert "candidates" in data
    assert len(data["candidates"]) >= 1
    c = data["candidates"][0]
    assert "normalized_score" in c
    assert "fair_score"       in c
    assert "bias_warnings"    in c
    print(f"PASS  POST /ats/shortlist  → "
          f"total={data['total_candidates']} "
          f"shortlisted={data['shortlisted']}")


def test_async_job():
    r = client.post("/jobs/start", json={
        "candidate_id": state["candidate_id"],
        "job_id":       state["job_id"]
    })
    assert r.status_code == 200
    data = r.json()
    assert "job_id" in data
    async_id = data["job_id"]

    # Check status (TestClient runs bg tasks synchronously)
    r2 = client.get(f"/jobs/status/{async_id}")
    assert r2.status_code == 200
    status_data = r2.json()
    assert status_data["status"] in ["queued", "processing", "completed"]
    print(f"PASS  POST /jobs/start + GET /jobs/status  → status={status_data['status']}")


def test_get_result():
    r = client.get(f"/ats/result/{state['candidate_id']}/{state['job_id']}")
    assert r.status_code == 200
    data = r.json()
    assert "final_score" in data
    print(f"PASS  GET  /ats/result  → score={data['final_score']}")


if __name__ == "__main__":
    print(SEP)
    print("Day 16 — ATS API Tests")
    print(SEP)
    test_health()
    test_home()
    test_create_job()
    test_upload_resume()
    test_upload_invalid_type()
    test_parse_resume()
    test_parse_not_found()
    test_ats_score()
    test_ats_score_not_found()
    test_shortlist()
    test_async_job()
    test_get_result()
    print(f"\n{SEP}")
    print("All Day 16 API tests passed!")
    print(SEP)