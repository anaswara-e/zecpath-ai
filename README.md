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

## Day 5 – Resume Text Extraction Engine

In this phase, I built a resume parsing engine that converts resume files into clean text for AI processing.

### What was implemented:

* Extracted text from PDF, DOCX, and TXT files
* Cleaned and normalized resume text
* Removed unwanted symbols and formatting issues
* Converted text into a consistent lowercase format
* Saved cleaned output into structured files

### Files Created:

* parsers/resume_parser.py
* tests/test_parser.py

### Output:

* Cleaned resumes stored in → data/cleaned/

### Key Functionality:

* Multi-format support (.pdf, .docx, .txt)
* Automated test execution using pytest
* Structured output for further AI processing

---
## Day 6 – Job Description Parsing

- Built JD parser for Mechanical Engineering roles
- Processed 100+ job description files automatically
- Extracted role, skills, experience, and education
- Converted all JDs into structured JSON format


---
## Project Structure

```
zecpath-ai/
 ├── ats_engine/
 ├── screening_ai/
 ├── interview_ai/
 ├── scoring/
 ├── utils/
 ├── parsers/
 │    └── resume_parser.py
 ├── data/
 │    ├── resumes/
 │    ├── job_descriptions/
 │    ├── structured/
 │    ├── cleaned/
 │    ├── resume_schema.json
 │    ├── jd_schema.json
 │    ├── data_entities.md
 ├── tests/
 │    └── test_parser.py
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
