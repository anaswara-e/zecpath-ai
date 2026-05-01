from ats_engine.skill_extractor import extract_skills_with_confidence
import json


# ✅ Test with simple text
def test_skill_extraction_basic():

    text = "Python AutoCAD SolidWorks communication leadership"

    skills = extract_skills_with_confidence(text)

    print(skills)

    assert len(skills) > 0
    assert any(s["skill"] == "python" for s in skills)


# ✅ Test with real resume file
def test_skill_extraction_resume():

    with open("data/resumes/resume1.txt", "r") as f:
        text = f.read()

    skills = extract_skills_with_confidence(text)

    # save output
    with open("data/skills/resume1_skills.json", "w") as f:
        json.dump(skills, f, indent=4)

    print(skills)

    assert len(skills) > 0