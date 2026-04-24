import pdfplumber
from docx import Document
import re


# ---------------- PDF ----------------
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


# ---------------- DOCX ----------------
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


# ---------------- TXT ----------------
def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------- CLEAN TEXT ----------------
def clean_text(text):
    # remove new lines
    text = text.replace("\n", " ")

    # remove extra spaces
    text = " ".join(text.split())

    # remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # convert to lowercase
    text = text.lower()

    return text


# ---------------- MAIN PARSER ----------------
def parse_resume(file_path):
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)

    elif file_path.endswith(".txt"):
        raw_text = extract_text_from_txt(file_path)

    else:
        raise ValueError("Unsupported file format")

    cleaned = clean_text(raw_text)
    return cleaned


# ---------------- SAVE CLEANED OUTPUT ----------------
def save_cleaned_text(text, filename):
    with open(f"data/cleaned/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(text)