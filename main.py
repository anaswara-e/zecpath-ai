import os

from parsers.resume_parser import extract_text
from ats_engine.skill_extractor import extract_skills
from ats_engine.experience_parser import extract_experience_blocks
from ats_engine.semantic_matcher import match_resume_to_jd
from ats_engine.ats_scorer import generate_candidate_score


resume_folder = "data/resumes"
jd_folder = "data/job_descriptions"


for resume_file in os.listdir(resume_folder):

    if resume_file.endswith(".txt"):

        print("\n==============================")
        print(f"Resume: {resume_file}")
        print("Top 3 Matches:")
        print("==============================")

        resume_path = os.path.join(resume_folder, resume_file)

        # Extract resume data
        resume_text = extract_text(resume_path)
        resume_skills = extract_skills(resume_text)
        resume_exp = extract_experience_blocks(resume_text)

        resume = {
            "skills": resume_skills,
            "experience": resume_exp,
            "projects": [{"description": resume_text}]
        }

        results = []

        # Loop through all JDs
        for jd_file in os.listdir(jd_folder):

            if jd_file.lower().endswith(".txt"):

                jd_path = os.path.join(jd_folder, jd_file)

                with open(jd_path, "r", encoding="utf-8") as f:
                    jd_text = f.read()

                jd_skills = extract_skills(jd_text)

                jd = {
                    "job_title": jd_file.replace(".txt", ""),
                    "required_skills": jd_skills,
                    "job_description_text": jd_text
                }

                # Semantic score
                match_result = match_resume_to_jd(resume, jd)
                semantic_score = match_result["final_similarity_score"]

                # Skill score
                matched_skills = set(resume_skills).intersection(set(jd_skills))

                if len(jd_skills) > 0:
                    skill_score = (len(matched_skills) / len(jd_skills)) * 100
                else:
                    skill_score = 0

                # Experience score (simple logic)
                experience_score = min(len(resume_exp) * 20, 100)

                # Education score (static for now)
                education_score = 70

                candidate = {
                    "candidate_id": resume_file,
                    "skill_score": skill_score,
                    "experience_score": experience_score,
                    "education_score": education_score,
                    "semantic_score": semantic_score
                }

                final_result = generate_candidate_score(candidate)

                results.append({
                    "job": jd_file,
                    "final_score": round(final_result["final_score"], 2)
                })

        # Sort results
        results = sorted(results, key=lambda x: x["final_score"], reverse=True)

        # Print ONLY TOP 3
        for r in results[:3]:
            print(f"{r['job']} → {r['final_score']}%")