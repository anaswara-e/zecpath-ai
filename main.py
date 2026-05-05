import os

from parsers.resume_parser import extract_text
from ats_engine.skill_extractor import extract_skills
from ats_engine.experience_parser import extract_experience_blocks
from ats_engine.semantic_matcher import match_resume_to_jd



resume_folder = "data/resumes"
jd_folder = "data/job_descriptions"



for resume_file in os.listdir(resume_folder):

    if resume_file.endswith(".txt"):

        print("\n==============================")
        print(f"Processing Resume: {resume_file}")
        print("==============================")

        resume_path = os.path.join(resume_folder, resume_file)

        
        resume_text = extract_text(resume_path)

        
        resume = {
            "skills": extract_skills(resume_text),
            "experience": extract_experience_blocks(resume_text),
            "projects": [{"description": resume_text}]
        }

        results = []

        
        for jd_file in os.listdir(jd_folder):

            if jd_file.endswith(".txt"):

                jd_path = os.path.join(jd_folder, jd_file)

                with open(jd_path, "r", encoding="utf-8") as f:
                    jd_text = f.read()

                jd = {
                    "job_title": "Mechanical Engineer",
                    "required_skills": ["cad", "solidworks", "manufacturing"],
                    "job_description_text": jd_text
                }

                match_result = match_resume_to_jd(resume, jd)

                results.append({
                    "job": jd_file,
                    "score": match_result["final_similarity_score"]
                })

        
        results = sorted(results, key=lambda x: x["score"], reverse=True)

        

        for r in results[:3]:
            print(f"{r['job']} → {r['score']}%")