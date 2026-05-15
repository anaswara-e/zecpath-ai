import re
import time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor


@lru_cache(maxsize=1000)
def clean_text_cached(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\.\,\-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def process_resumes_parallel(resume_texts, process_function):
    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_function, text)
            for text in resume_texts
        ]

        for future in futures:
            results.append(future.result())

    return results


SKILLS = [
    "python",
    "java",
    "react",
    "node",
    "sql",
    "django",
    "machine learning",
    "autocad",
    "solidworks",
    "catia"
]

def fast_skill_extract(text):
    text = clean_text_cached(text)

    return [
        skill for skill in SKILLS
        if skill in text
    ]

# -------------------------------
# Skill Extraction with Confidence
# -------------------------------
def fast_skill_extract_with_confidence(text):
    text = clean_text_cached(text)

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append({
                "skill": skill,
                "confidence": 0.95
            })

    return found_skills

def batch_process(data, batch_size=10):

    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


def clean_noisy_resume(text):

    text = clean_text_cached(text)

    # remove repeated chars
    text = re.sub(r"(.)\1{2,}", r"\1", text)

    # remove excessive punctuation
    text = re.sub(r"[\.\,\-]{2,}", "", text)

    return text


def safe_execute(func, data):

    try:
        return func(data)

    except Exception as e:
        return {"error": str(e)}



def retry(func, data, retries=3):

    for attempt in range(retries):

        try:
            return func(data)

        except:
            time.sleep(1)

    return {"error": "Failed after retries"}