import re


# Define section keywords
SECTION_KEYWORDS = {
    "skills": ["skills", "technical skills"],
    "experience": ["experience", "work experience", "employment"],
    "education": ["education", "academic"],
    "projects": ["projects"],
    "certifications": ["certifications", "certificates"]
}


def clean_text(text):
    text = text.lower()
    return text


def split_sections(text):
    text = clean_text(text)

    sections = {}
    current_section = "other"
    sections[current_section] = ""

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        # check if line is a heading
        for section, keywords in SECTION_KEYWORDS.items():
            if any(keyword in line for keyword in keywords):
                current_section = section
                if current_section not in sections:
                    sections[current_section] = ""
                break

        sections[current_section] += " " + line

    return sections