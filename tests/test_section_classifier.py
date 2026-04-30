from parsers.section_classifier import detect_sections
import json


# ✅ Test with sample text
def test_section_detection_basic():

    text = """SKILLS
Python, SQL
EXPERIENCE
Worked at Infosys
EDUCATION
B.Tech Computer Science"""

    sections = detect_sections(text)

    print(sections)

    assert "skills" in sections
    assert "experience" in sections
    assert "education" in sections


# ✅ Test with real resume file
def test_section_detection_file():

    with open("data/resumes/resume1.txt", "r") as f:
        text = f.read()

    sections = detect_sections(text)

    # Save output
    with open("data/sections/resume1_sections.json", "w") as f:
        json.dump(sections, f, indent=4)

    assert "skills" in sections or "experience" in sections