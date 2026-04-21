def calculate_score(candidate_skills, required_skills):
    match = set(candidate_skills) & set(required_skills)
    return (len(match) / len(required_skills)) * 100
