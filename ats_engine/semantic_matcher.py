from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')


# -------------------------------
# Convert text → embedding
# -------------------------------
def get_embedding(text):
    return model.encode(text)


# -------------------------------
# Similarity between 2 texts
# -------------------------------
def compute_similarity(text1, text2):

    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)

    score = cosine_similarity([emb1], [emb2])[0][0]

    return round(float(score), 4)


# -------------------------------
# Resume ↔ JD Matching
# -------------------------------
def match_resume_to_jd(resume, jd):

    results = {}

    # Skills
    resume_skills = " ".join(resume.get("skills", []))
    jd_skills = " ".join(jd.get("required_skills", []))
    results["skills_similarity"] = compute_similarity(resume_skills, jd_skills)

    # Experience
    resume_roles = " ".join([exp["role"] for exp in resume.get("experience", [])])
    jd_role = jd.get("job_title", "")
    results["experience_similarity"] = compute_similarity(resume_roles, jd_role)

    # Projects
    resume_projects = " ".join([p["description"] for p in resume.get("projects", [])])
    jd_desc = jd.get("job_description_text", "")
    results["project_similarity"] = compute_similarity(resume_projects, jd_desc)

    # Final score
    final_score = (
        0.4 * results["skills_similarity"] +
        0.3 * results["experience_similarity"] +
        0.3 * results["project_similarity"]
    )

    results["final_similarity_score"] = round(final_score * 100, 2)

    return results


# -------------------------------
# Classification
# -------------------------------
def classify_match(score):

    if score >= 85:
        return "Strong Match"
    elif score >= 65:
        return "Moderate Match"
    else:
        return "Weak Match"