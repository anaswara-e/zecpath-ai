# Zecpath AI System

This project is part of an AI-powered hiring platform that automates the recruitment process using AI.

---

## Features

* ATS Engine (Resume Screening)
* Screening AI (Voice-based interaction)
* Interview AI (HR & Technical)
* Scoring System

---

## Day 3 – Environment Setup

* Created modular project structure
* Setup Python virtual environment
* Configured basic testing using pytest
* Organized folders for AI modules

---

## Day 4 – Data Understanding & Structuring

I analyzed sample resumes and job descriptions to understand hiring data.
Based on that, I created structured JSON schemas for candidate profiles
and job profiles, along with a sample structured resume for AI processing.

### Files Created:

* data/resume_schema.json
* data/jd_schema.json
* data/data_entities.md
* data/structured/sample_resume.json

### Data Added:

* Sample resumes → data/resumes/
* Job descriptions → data/job_descriptions/

---

## Project Structure

```
zecpath-ai/
 ├── ats_engine/
 ├── screening_ai/
 ├── interview_ai/
 ├── scoring/
 ├── utils/
 ├── data/
 │    ├── resumes/
 │    ├── job_descriptions/
 │    ├── structured/
 │    ├── resume_schema.json
 │    ├── jd_schema.json
 │    ├── data_entities.md
 ├── tests/
 ├── main.py
 ├── config.py
 └── README.md
```

---

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

---

## Run Tests

```
pytest
```

---

## Author

Anaswara E
