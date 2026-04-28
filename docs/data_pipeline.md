# Zecpath AI Data Pipeline

## Overview

The AI data pipeline defines how data moves through the Zecpath system from candidate application to final hiring decision.

---

## Step-by-Step Flow

1. Resume Upload
   Candidate uploads resume (PDF/DOCX)

2. Resume Parsing (Day 5)
   Resume is converted into clean text
   Stored as structured candidate profile

3. Job Description Parsing (Day 6)
   Job descriptions are parsed into structured job requirements

4. ATS Matching
   Candidate skills are matched with job requirements
   ATS score is generated

5. Screening AI
   AI conducts voice screening
   Responses are stored and scored

6. Interview AI
   AI performs HR and technical interviews
   Scores and transcripts are generated

7. Behavior Analysis
   AI evaluates candidate behavior and integrity

8. Final Decision Engine
   All scores are combined
   Final decision is generated (Selected / Rejected / Hold)

---

## Output

Final structured candidate evaluation with:

* ATS score
* Interview scores
* Behavior score
* Final decision
