import os
import PyPDF2

def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    return text

def load_all_jds(folder_path):
    jds = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            role_name = file.replace(".pdf", "")
            full_path = os.path.join(folder_path, file)

            jd = {
                "job_title": role_name,
                "required_skills": [],
                "job_description_text": extract_text_from_pdf(full_path)
            }

            jds.append(jd)

    return jds