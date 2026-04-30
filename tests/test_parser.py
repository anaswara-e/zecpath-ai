from parsers.resume_parser import parse_resume, save_cleaned_text


def test_resume_parsing():
    file_path = "data/resumes/resume1.txt"

    text = parse_resume(file_path)
    save_cleaned_text(text, "resume_cleaned")

    assert len(text) > 0

from parsers.resume_parser import parse_resume
from parsers.section_parser import split_sections


def test_section_detection():

    file_path = "data/resumes/resume1.txt"  # change if needed

    text = parse_resume(file_path)

    sections = split_sections(text)

    print(sections)

    assert "skills" in sections or "experience" in sections