# api/api_schemas.py
# Day 16 — Pydantic V2 compatible schemas (no deprecated example= kwargs)

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


# ── Request Schemas ───────────────────────────────────────────────────────────

class ResumeUploadMeta(BaseModel):
    job_id:       str
    candidate_id: str

class ParseRequest(BaseModel):
    resume_id:    str
    candidate_id: Optional[str] = None

class JobCreateRequest(BaseModel):
    job_title:        str
    required_skills:  str
    responsibilities: Optional[str]  = ""
    requirements:     Optional[str]  = ""
    experience_range: Optional[dict] = {"min_years": 0, "max_years": 20}

class ScoreRequest(BaseModel):
    candidate_id: str
    job_id:       str

class ShortlistRequest(BaseModel):
    job_id:    str
    threshold: Optional[float] = 60.0
    top_n:     Optional[int]   = 5

class AsyncJobStartRequest(BaseModel):
    candidate_id: str
    job_id:       str


# ── Response Schemas ──────────────────────────────────────────────────────────

class UploadResponse(BaseModel):
    status:       str
    resume_id:    str
    candidate_id: str
    job_id:       str
    timestamp:    str

class ParsedProfile(BaseModel):
    skills:            List[str]
    total_skills:      int
    experience:        List[Dict[str, Any]]
    total_years:       float
    experience_blocks: int

class ParseResponse(BaseModel):
    status:         str
    candidate_id:   str
    resume_id:      str
    parsed_profile: ParsedProfile
    timestamp:      str

class JobCreateResponse(BaseModel):
    status:           str
    job_id:           str
    job_title:        str
    extracted_skills: List[str]
    timestamp:        str

class ScoreBreakdown(BaseModel):
    skills:     float
    experience: float
    education:  float
    semantic:   float

class ScoreResponse(BaseModel):
    status:       str
    candidate_id: str
    job_id:       str
    final_score:  float
    decision:     str
    breakdown:    ScoreBreakdown
    timestamp:    str

class CandidateSummary(BaseModel):
    candidate_id:     str
    rank:             int
    score:            float
    normalized_score: float
    fair_score:       float
    status:           str
    bias_warnings:    int

class ShortlistResponse(BaseModel):
    status:           str
    job_id:           str
    total_candidates: int
    shortlisted:      int
    review:           int
    rejected:         int
    candidates:       List[CandidateSummary]
    timestamp:        str

class AsyncJobResponse(BaseModel):
    job_id:    str
    status:    str
    timestamp: str

class AsyncJobStatus(BaseModel):
    job_id:     str
    status:     str
    result_url: Optional[str] = None
    error:      Optional[str] = None
    created_at: str

class ErrorResponse(BaseModel):
    status:     str = "error"
    error_code: str
    message:    str
    timestamp:  str


# ── Error codes reference ─────────────────────────────────────────────────────

ERROR_CODES = {
    "INVALID_INPUT":  "Missing or invalid request data",
    "NOT_FOUND":      "Requested resource does not exist",
    "PROCESSING_ERR": "AI engine processing failure",
    "SERVER_ERROR":   "Internal system error",
    "AUTH_ERROR":     "Authentication/authorization failure",
}