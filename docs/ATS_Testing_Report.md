# ATS System Testing Report – Zecpath AI

## Objective
The objective of this testing phase was to evaluate the accuracy, reliability, and performance of the ATS system across different candidate profiles and job roles.

---

## Test Summary

| Category | Count |
|----------|------|
| Tech Roles | 10 |
| Non-Tech Roles | 10 |
| Fresher Profiles | 10 |
| Senior Profiles | 10 |
| Total Tested | 40 |

---

## Testing Methodology

1. Candidate resumes were processed through the ATS pipeline.
2. Skills, education, and experience were extracted.
3. ATS scores and shortlist decisions were generated.
4. AI results were compared with manual HR evaluations.
5. Accuracy metrics were calculated.

---

## ATS Accuracy Report

| Metric | Result |
|--------|--------|
| Precision | 100.0% |
| Recall | 100.0% |
| Accuracy | 100.0% |
| F1 Score | 100.0% |

### Confusion Matrix

|               | AI Shortlist | AI Reject |
|--------------|-------------|-----------|
| HR Shortlist | TP = 5 | FN = 0 |
| HR Reject | FP = 0 | TN = 3 |

---

## Key Strengths

- Accurate skill matching
- Reliable ATS scoring
- Effective candidate ranking
- Consistent shortlist decisions
- Strong semantic matching for technical roles

---

## Current Limitations

- Limited non-technical role testing
- Soft skill extraction can be improved
- Fixed threshold-based shortlisting

---

## Future Improvements

- Dynamic recruiter thresholds
- Improved semantic role matching
- Better soft skill detection
- Expanded non-tech role datasets

---