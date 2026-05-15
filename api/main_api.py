from fastapi.middleware.cors import CORSMiddleware
from api.api_schemas import (
    ParseRequest,
    ScoreRequest,
    ShortlistRequest,
    JobCreateRequest,
    AsyncJobStartRequest,
)

from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
import uuid
import os
import shutil
import logging
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parsers.resume_parser import extract_text
from parsers.normalization import normalize_resume_text, normalize_jd_text
from ats_engine.optimized_engine import fast_skill_extract
from ats_engine.experience_parser import extract_experience_blocks, calculate_total_experience
from ats_engine.semantic_matcher import match_resume_to_jd
from ats_engine.ats_scorer import generate_candidate_score
from ats_engine.rankingengine import ranking_pipeline
from ats_engine.fairness_engine import apply_fairness_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zecpath_ats")

app = FastAPI(
    title="Zecpath ATS API",
    version="1.0.0",
    description="AI Powered ATS System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Stores ────────────────────────────────────────────────────────────────────
resume_store        = {}   # resume_id  → resume data
job_store           = {}   # job_id     → jd data
score_store         = {}   # (candidate_id, job_id) → score result
job_queue           = {}   # async_job_id → status
candidate_resume_map = {}  # candidate_id → resume_id

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def timestamp():
    return datetime.utcnow().isoformat() + "Z"

def error_response(code, message, status_code=400):
    return JSONResponse(
        status_code=status_code,
        content={
            "status":     "error",
            "error_code": code,
            "message":    message,
            "timestamp":  timestamp()
        }
    )

def score_experience(total_years):
    if total_years >= 6:   return 100
    elif total_years >= 4: return 85
    elif total_years >= 2: return 70
    elif total_years >= 1: return 50
    return 20

def score_skills(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    matched   = set(resume_skills) & set(jd_skills)
    precision = len(matched) / len(jd_skills)
    union     = set(resume_skills) | set(jd_skills)
    jaccard   = len(matched) / len(union) if union else 0
    return round(((precision + jaccard) / 2) * 100, 2)

def _resolve_resume(candidate_id: str):
    """
    FIX: Accept EITHER a candidate_id (from candidate_resume_map)
    OR a resume_id directly (starting with R).
    This makes the API work whether the test passes C_TEST or R3A2B1C4.
    """
    # Direct resume_id lookup
    if candidate_id in resume_store:
        return candidate_id, resume_store[candidate_id]
    # candidate_id → resume_id lookup
    if candidate_id in candidate_resume_map:
        rid = candidate_resume_map[candidate_id]
        if rid in resume_store:
            return rid, resume_store[rid]
    return None, None

# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/")
@app.get("/api/v1/")
def home():
    return {
        "message":   "Zecpath ATS API Running",
        "version":   "1.0.0",
        "timestamp": timestamp()
    }

# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health")
@app.get("/api/v1/health")
def health():
    return {
        "status":          "healthy",
        "resumes_loaded":  len(resume_store),
        "jobs_loaded":     len(job_store),
        "scores_computed": len(score_store),
        "async_jobs":      len(job_queue),
        "timestamp":       timestamp()
    }

# ── Resume Upload ─────────────────────────────────────────────────────────────
@app.post("/resume/upload")
@app.post("/api/v1/resume/upload")
async def upload_resume(
    file:         UploadFile = File(...),
    job_id:       str = "J000",
    candidate_id: str = "C000"
):
    allowed = [".pdf", ".txt", ".docx"]
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in allowed:
        return error_response("INVALID_INPUT", f"Unsupported file type {ext}")

    resume_id = "R" + str(uuid.uuid4())[:8].upper()
    save_path = os.path.join(UPLOAD_DIR, f"{resume_id}{ext}")

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    resume_store[resume_id] = {
        "resume_id":    resume_id,
        "candidate_id": candidate_id,
        "job_id":       job_id,
        "file_path":    save_path,
        "parsed":       False
    }

    # FIX: map BOTH candidate_id AND resume_id so either can be used in /ats/score
    candidate_resume_map[candidate_id] = resume_id
    candidate_resume_map[resume_id]    = resume_id   # ← self-mapping for direct lookup

    logger.info(f"Uploaded: resume_id={resume_id} candidate_id={candidate_id}")

    return {
        "status":       "success",
        "resume_id":    resume_id,
        "candidate_id": candidate_id,
        "job_id":       job_id,
        "timestamp":    timestamp()
    }

# ── Resume Parse ──────────────────────────────────────────────────────────────
@app.post("/resume/parse")
@app.post("/api/v1/resume/parse")
def parse_resume(req: ParseRequest):
    if req.resume_id not in resume_store:
        return error_response("NOT_FOUND", "Resume not found", 404)

    resume   = resume_store[req.resume_id]
    raw_text = extract_text(resume["file_path"])
    norm_text = normalize_resume_text(raw_text)
    skills    = fast_skill_extract(norm_text)
    experience = extract_experience_blocks(norm_text)
    total_years = calculate_total_experience(experience)

    resume.update({
        "parsed":     True,
        "skills":     skills,
        "experience": experience,
        "total_years": total_years,
        "norm_text":  norm_text,
        "projects":   [{"description": norm_text}]
    })

    logger.info(f"Parsed: resume_id={req.resume_id} skills={len(skills)} exp={total_years}yrs")

    return {
        "status":       "completed",
        "resume_id":    req.resume_id,
        "candidate_id": resume["candidate_id"],
        "parsed_profile": {
            "skills":      skills,
            "total_skills": len(skills),
            "total_years":  total_years,
            "experience":   experience,
            "experience_blocks": len(experience)
        },
        "timestamp": timestamp()
    }

# ── Job Create ────────────────────────────────────────────────────────────────
@app.post("/jobs/create")
@app.post("/api/v1/jobs/create")
def create_job(req: JobCreateRequest):
    job_id   = "J" + str(uuid.uuid4())[:8].upper()
    jd_text  = normalize_jd_text(f"{req.job_title} {req.required_skills}")
    jd_skills = fast_skill_extract(jd_text)

    job_store[job_id] = {
        "job_id":          job_id,
        "job_title":       req.job_title,
        "required_skills": jd_skills,
        "jd_text":         jd_text
    }

    logger.info(f"Job created: job_id={job_id} skills={len(jd_skills)}")

    return {
        "status":           "success",
        "job_id":           job_id,
        "job_title":        req.job_title,
        "extracted_skills": jd_skills,
        "timestamp":        timestamp()
    }

# ── ATS Score ─────────────────────────────────────────────────────────────────
@app.post("/ats/score")
@app.post("/api/v1/ats/score")
def ats_score(req: ScoreRequest):

    # FIX: use _resolve_resume so resume_id OR candidate_id both work
    resume_id, resume = _resolve_resume(req.candidate_id)

    if resume is None:
        return error_response("NOT_FOUND",
            f"Candidate '{req.candidate_id}' not found. "
            "Upload and parse resume first.", 404)

    if req.job_id not in job_store:
        return error_response("NOT_FOUND",
            f"Job '{req.job_id}' not found. Create job first.", 404)

    if not resume.get("parsed"):
        return error_response("INVALID_INPUT",
            "Resume not parsed yet. Call /resume/parse first.")

    jd = job_store[req.job_id]

    try:
        skill_score      = score_skills(resume.get("skills", []),
                                        jd.get("required_skills", []))
        experience_score = score_experience(resume.get("total_years", 0))
        education_score  = 70

        resume_obj = {
            "skills":     resume.get("skills", []),
            "experience": resume.get("experience", []),
            "projects":   resume.get("projects", [{"description": ""}])
        }
        match_result   = match_resume_to_jd(resume_obj, jd)
        semantic_score = match_result["final_similarity_score"]

        scored = generate_candidate_score({
            "candidate_id":     req.candidate_id,
            "skill_score":      skill_score,
            "experience_score": experience_score,
            "education_score":  education_score,
            "semantic_score":   semantic_score
        })

        result = {
            "candidate_id": req.candidate_id,
            "job_id":       req.job_id,
            "final_score":  scored["final_score"],
            "decision":     scored.get("decision", "REVIEW"),
            "breakdown": {
                "skills":     skill_score,
                "experience": experience_score,
                "education":  education_score,
                "semantic":   semantic_score
            }
        }

        # FIX: store under req.candidate_id (whatever was passed in)
        score_store[(req.candidate_id, req.job_id)] = result

        logger.info(f"Scored: candidate={req.candidate_id} job={req.job_id} "
                    f"score={scored['final_score']}")

        return {"status": "success", **result, "timestamp": timestamp()}

    except Exception as e:
        logger.error(f"Scoring error: {e}")
        return error_response("PROCESSING_ERR", str(e), 500)

# ── Shortlist ─────────────────────────────────────────────────────────────────
@app.post("/ats/shortlist")
@app.post("/api/v1/ats/shortlist")
def ats_shortlist(req: ShortlistRequest):
    if req.job_id not in job_store:
        return error_response("NOT_FOUND", f"Job '{req.job_id}' not found.", 404)

    # Gather all scored candidates for this job
    candidates = []
    for (cid, jid), score in score_store.items():
        if jid == req.job_id:
            candidates.append({
                "candidate_id": cid,
                "final_score":  score["final_score"],
                "breakdown":    score.get("breakdown", {})
            })

    if not candidates:
        return error_response("NOT_FOUND",
            "No scored candidates for this job. Call /ats/score first.", 404)

    # Day 14 — rank
    result     = ranking_pipeline(candidates, job_id=req.job_id, top_n=req.top_n)
    # Day 15 — fairness
    fair_list  = apply_fairness_pipeline(result["ranked_list"])
    summary    = result["recruiter_summary"]["summary"]

    logger.info(f"Shortlist: job={req.job_id} total={summary['total_candidates']} "
                f"shortlisted={summary['shortlisted']}")

    return {
        "status":           "success",
        "job_id":           req.job_id,
        "total_candidates": summary["total_candidates"],
        "shortlisted":      summary["shortlisted"],
        "review":           summary["review"],
        "rejected":         summary["rejected"],
        "candidates": [
            {
                "candidate_id":    c["candidate_id"],
                "rank":            c["rank"],
                "score":           c["final_score"],
                "normalized_score": c.get("normalized_score", 0),
                "fair_score":      c.get("fair_score", 0),
                "status":          c["status"],
                "bias_warnings":   len(c.get("bias_warnings", []))
            }
            for c in fair_list
        ],
        "timestamp": timestamp()
    }

# ── Async Jobs ────────────────────────────────────────────────────────────────
@app.post("/jobs/start")
@app.post("/api/v1/jobs/start")
def start_async_job(req: AsyncJobStartRequest, bg: BackgroundTasks):
    async_id = "JOB" + str(uuid.uuid4())[:6].upper()
    job_queue[async_id] = {
        "job_id":     async_id,
        "status":     "processing",
        "created_at": timestamp()
    }
    return {"job_id": async_id, "status": "processing", "timestamp": timestamp()}

@app.get("/jobs/status/{async_job_id}")
@app.get("/api/v1/jobs/status/{async_job_id}")
def job_status(async_job_id: str):
    if async_job_id not in job_queue:
        return error_response("NOT_FOUND", "Job not found", 404)
    return job_queue[async_job_id]

# ── Result ────────────────────────────────────────────────────────────────────
@app.get("/ats/result/{candidate_id}/{job_id}")
@app.get("/api/v1/ats/result/{candidate_id}/{job_id}")
def get_result(candidate_id: str, job_id: str):
    key = (candidate_id, job_id)
    if key not in score_store:
        return error_response("NOT_FOUND",
            f"No result for candidate={candidate_id} job={job_id}. "
            "Call /ats/score first.", 404)
    result = score_store[key]
    return {
        "status":       "success",
        "candidate_id": candidate_id,
        "job_id":       job_id,
        "final_score":  result["final_score"],
        "decision":     result.get("decision", "REVIEW"),
        "breakdown":    result.get("breakdown", {}),
        "timestamp":    timestamp()
    }