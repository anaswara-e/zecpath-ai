# main.py — Full ATS pipeline
# Day 15 update: fairness pipeline + normalization integrated

import os
import json

from parsers.resume_parser        import extract_text
from parsers.normalization        import normalize_resume_text, normalize_jd_text   # Day 15
from ats_engine.optimized_engine import fast_skill_extract
from ats_engine.experience_parser import extract_experience_blocks, calculate_total_experience
from ats_engine.semantic_matcher  import match_resume_to_jd
from ats_engine.ats_scorer        import generate_candidate_score
from ats_engine.rankingengine     import ranking_pipeline
from ats_engine.fairness_engine   import apply_fairness_pipeline, print_fairness_result  # Day 15


resume_folder = "data/resumes"
jd_folder     = "data/job_descriptions"


def score_experience(total_years):
    if total_years >= 6:   return 100
    elif total_years >= 4: return 85
    elif total_years >= 2: return 70
    elif total_years >= 1: return 50
    else:                  return 20


def score_skills(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    matched   = set(resume_skills) & set(jd_skills)
    precision = len(matched) / len(jd_skills)
    union     = set(resume_skills) | set(jd_skills)
    jaccard   = len(matched) / len(union) if union else 0
    return round(((precision + jaccard) / 2) * 100, 2)


# ── Pre-load all resumes once ─────────────────────────────────────────────────
print("Loading and normalizing resumes...")
all_resumes = {}

for resume_file in os.listdir(resume_folder):
    if not resume_file.endswith(".txt"):
        continue

    resume_path = os.path.join(resume_folder, resume_file)
    raw_text    = extract_text(resume_path)

    # Day 15 — normalize before extracting skills/experience
    norm_text     = normalize_resume_text(raw_text)

    resume_skills = fast_skill_extract(norm_text)
    resume_exp    = extract_experience_blocks(norm_text)
    total_years   = calculate_total_experience(resume_exp)

    all_resumes[resume_file] = {
        "text":        norm_text,
        "raw_text":    raw_text,
        "skills":      resume_skills,
        "experience":  resume_exp,
        "total_years": total_years,
        "projects":    [{"description": norm_text}]
    }

print(f"  Loaded {len(all_resumes)} resumes.\n")


# ── Main loop — per JD ────────────────────────────────────────────────────────
for jd_file in os.listdir(jd_folder):
    if not jd_file.lower().endswith(".txt"):
        continue

    jd_path = os.path.join(jd_folder, jd_file)
    with open(jd_path, "r", encoding="utf-8") as f:
        raw_jd = f.read()

    # Day 15 — normalize JD text too
    jd_text   = normalize_jd_text(raw_jd)
    jd_skills = fast_skill_extract(jd_text)
    jd = {
        "job_title":            jd_file.replace(".txt", ""),
        "required_skills":      jd_skills,
        "job_description_text": jd_text
    }

    candidates_for_jd = []   # reset for each JD

    for resume_file, resume in all_resumes.items():

        match_result    = match_resume_to_jd(resume, jd)
        semantic_score  = match_result["final_similarity_score"]

        skill_score      = score_skills(resume["skills"], jd_skills)
        experience_score = score_experience(resume["total_years"])
        education_score  = 70

        candidate_raw = {
            "candidate_id":     resume_file,
            "skill_score":      skill_score,
            "experience_score": experience_score,
            "education_score":  education_score,
            "semantic_score":   semantic_score,
            "resume_skills":    resume["skills"],
        }

        scored = generate_candidate_score(candidate_raw)

        candidates_for_jd.append({
            "candidate_id": resume_file,
            "final_score":  scored["final_score"],
            "breakdown":    scored["breakdown"]
        })

    # ── Day 14: Rank ──────────────────────────────────────────────────────────
    job_id = jd_file.replace(".txt", "")
    result = ranking_pipeline(candidates_for_jd, job_id=job_id, top_n=5)

    # ── Day 15: Apply fairness pipeline to ranked list ────────────────────────
    fair_candidates = apply_fairness_pipeline(result["ranked_list"])
    result["ranked_list"] = fair_candidates

    # ── Print output ──────────────────────────────────────────────────────────
    print("=" * 60)
    print(f"JOB: {job_id}")
    print("=" * 60)

    summary = result["recruiter_summary"]["summary"]
    print(f"  Total Candidates : {summary['total_candidates']}")
    print(f"  Shortlisted      : {summary['shortlisted']}")
    print(f"  Review           : {summary['review']}")
    print(f"  Rejected         : {summary['rejected']}")

    print("\n  Ranked List (with Fairness):")
    for c in result["ranked_list"]:
        warn_count = len(c.get("bias_warnings", []))
        print(
            f"    #{c['rank']:03d}  {c['candidate_id']:<35} "
            f"Score:{c['final_score']:5.1f}  "
            f"Norm:{c.get('normalized_score',0):5.1f}  "
            f"Fair:{c.get('fair_score',0):5.1f}  "
            f"[{c['status']}]"
            + (f"  ⚠ {warn_count} bias warning(s)" if warn_count else "")
        )

    print("\n  Top Shortlisted:")
    for c in result["top_candidates"]:
        print(f"    * {c['candidate_id']}  ->  {c['final_score']}%  [{c['status']}]")

    # Save JSON
    os.makedirs("data/outputs", exist_ok=True)
    out_path = f"data/outputs/{job_id}_ranking.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"\n  Saved -> {out_path}\n")