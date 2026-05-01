# Zecpath AI System

Zecpath is an AI-powered hiring platform designed to automate the recruitment process — from resume screening to final candidate selection.

---

## Features

* ATS Engine (Resume Screening & Matching)
* Screening AI (Automated candidate interaction)
* Interview AI (HR & Technical evaluation)
* Skill Extraction & Experience Analysis
* Final Scoring & Decision Engine

---

## Project Structure

```
zecpath-ai/
│
├── data/
│   ├── resumes/
│   ├── job_descriptions/
│   ├── cleaned/
│   ├── structured/
│   └── schemas/
│
├── parsers/
│   ├── resume_parser.py
│   ├── jd_parser.py
│   └── section_classifier.py
│
├── ats_engine/
│   ├── ats_scorer.py
│   ├── skill_extractor.py
│   └── experience_parser.py
│
├── screening_ai/
│   └── screening_engine.py
│
├── interview_ai/
│   └── interview_engine.py
│
├── scoring/
│   └── scoring_engine.py
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
├── tests/
│   ├── test_parser.py
│   ├── test_skill_extractor.py
│   └── test_experience_parser.py
│
├── main.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Progress Overview

### Day 3 – Environment Setup

* Project structure created
* Virtual environment setup
* Testing configured (pytest)

### Day 4 – Data Structuring

* Designed resume & job description schemas
* Created structured sample data

### Day 5 – Resume Parsing

* Extracted and cleaned resume text
* Supported PDF, DOCX, TXT formats

### Day 6 – JD Parsing

* Processed multiple job descriptions
* Extracted role, skills, experience

### Day 7 – Data Pipeline

* Designed AI data flow and storage structure
* Defined metadata standards

### Day 8 – Section Segmentation

* Identified resume sections (skills, education, experience)

### Day 9 – Skill Extraction

* Extracted technical & non-technical skills
* Added confidence scoring

### Day 10 – Experience Parsing

* Extracted company, duration, roles
* Calculated total experience
* Added relevance scoring

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Run Tests

```bash
pytest
```

---

## Author

Anaswara E
