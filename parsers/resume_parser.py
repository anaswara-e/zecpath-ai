import os
import re

try:
    import docx
except:
    docx = None

try:
    from PyPDF2 import PdfReader
except:
    PdfReader = None

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_docx(file_path):
    if not docx:
        raise ImportError("python-docx not installed")

    doc = docx.Document(file_path)
    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return "\n".join(text)

def read_pdf(file_path):
    if not PdfReader:
        raise ImportError("PyPDF2 not installed")

    reader = PdfReader(file_path)
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)

def clean_text(text):
    text = text.lower()

    text = re.sub(r"[•●▪■►]", " ", text)

    text = re.sub(r"[^a-z0-9\s\.\,\-]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def extract_text(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    if file_path.endswith(".txt"):
        text = read_txt(file_path)

    elif file_path.endswith(".docx"):
        text = read_docx(file_path)

    elif file_path.endswith(".pdf"):
        text = read_pdf(file_path)

    else:
        raise ValueError("Unsupported file format")

    cleaned = clean_text(text)

    return cleaned