from ats_engine.experience_parser import *

def test_full_experience():

    text = """
    ABC Tech (2021–2024)
    Software Engineer
    XYZ Ltd (2019–2021)
    Intern
    """

    exp = extract_experience_blocks(text)
    roles = extract_roles(text)
    total = calculate_total_experience(exp)
    gaps = detect_gaps(exp)
    overlaps = detect_overlaps(exp)
    relevance = calculate_relevance(roles, "engineer")

    assert total > 0