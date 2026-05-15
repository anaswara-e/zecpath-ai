from ats_engine.optimized_engine import (
    process_resumes_parallel,
    fast_skill_extract,
    clean_noisy_resume,
    batch_process
)

# Sample resumes
resumes = [
    "Python developer!!! with Django---- experience",
    "React developer..... Node.js expert",
    "Java SQL engineer@@@@",
]

# Step 1: Clean resumes
cleaned_resumes = [clean_noisy_resume(r) for r in resumes]

print("\n===== CLEANED RESUMES =====")
for r in cleaned_resumes:
    print(r)

# Step 2: Parallel skill extraction
results = process_resumes_parallel(
    cleaned_resumes,
    fast_skill_extract
)

print("\n===== SKILL EXTRACTION =====")
for idx, skills in enumerate(results, start=1):
    print(f"Resume {idx}: {skills}")

# Step 3: Batch processing demo
print("\n===== BATCH PROCESSING =====")
for batch in batch_process(cleaned_resumes, batch_size=2):
    print(batch)

print("\nOptimization pipeline completed successfully.")