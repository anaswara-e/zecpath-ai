from parsers.resume_parser import parse_resume, save_cleaned_text


def test_resume_parsing():
    file_path = "data/resumes/resume1.txt"

    text = parse_resume(file_path)
    save_cleaned_text(text, "resume_cleaned")

    assert len(text) > 0