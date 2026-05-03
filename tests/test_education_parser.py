from parsers.education_parser import extract_education, extract_certifications
import json


def test_education_basic():

    text = "B.Tech Mechanical Engineering 2021"

    result = extract_education(text)

    assert len(result) > 0
    assert result[0]["degree"] == "B.Tech"


def test_certifications():

    text = "AutoCAD SolidWorks CNC Six Sigma"

    certs = extract_certifications(text)

    assert len(certs) > 0


def test_education_from_resume():

    with open("data/resumes/resume1.txt", "r") as f:
        text = f.read()

    edu = extract_education(text)
    certs = extract_certifications(text)

    with open("data/education/resume1_education.json", "w") as f:
        json.dump({
            "education": edu,
            "certifications": certs
        }, f, indent=4)

    assert len(edu) > 0 or len(certs) > 0