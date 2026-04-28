# Storage Structure Design

## Data Storage Types

### 1. Raw Data

* Resumes → data/resumes/
* Job Descriptions → data/job_descriptions/

### 2. Processed Data

* Cleaned resumes → data/cleaned/
* Structured JD → data/structured_jd/

### 3. AI Outputs

* ATS scores → data/ats_scores/
* Screening reports → data/screening/
* Interview results → data/interviews/

---

## Database Design (Conceptual)

Candidate Table:

* candidate_id
* name
* email

Job Table:

* job_id
* role
* requirements

Scores Table:

* candidate_id
* job_id
* ats_score
* interview_score
* final_score
