from parsers.resume_parser import extract_text
from parsers.section_classifier import detect_sections


def test_resume_parsing():

    file_path = "data/resumes/resume1.txt"

    text = extract_text(file_path)

    print(text)

    assert len(text) > 0


def test_section_detection():

    file_path = "data/resumes/resume1.txt"

    text = extract_text(file_path)

    sections = detect_sections(text)

    print(sections)

    assert "skills" in sections or "experience" in sections