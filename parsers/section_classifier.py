import re

# Section keywords
SECTION_KEYWORDS = {
    "skills": ["skills", "technical skills", "skill set"],
    "experience": ["experience", "work experience", "professional experience"],
    "education": ["education", "academic background", "qualification"],
    "certifications": ["certifications", "certificates"],
    "projects": ["projects"],
    "summary": ["summary", "profile", "objective"]
}

# Clean text
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text

# Main function
def detect_sections(text):
    lines = text.split("\n")
    sections = {}
    current_section = "other"

    for line in lines:
        clean_line = normalize_text(line.strip())

        found_section = None
        for section, keywords in SECTION_KEYWORDS.items():
            if any(keyword in clean_line for keyword in keywords):
                found_section = section
                break

        if found_section:
            current_section = found_section
            sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(line.strip())

    return sections