from ats_engine.ats_accuracy import evaluate_accuracy


def test_ats_accuracy():

    ai_results = [
        "Shortlisted",
        "Shortlisted",
        "Rejected",
        "Shortlisted",
        "Rejected",
        "Shortlisted",
        "Rejected",
        "Shortlisted"
    ]

    hr_results = [
        "Shortlisted",
        "Shortlisted",
        "Rejected",
        "Shortlisted",
        "Rejected",
        "Shortlisted",
        "Rejected",
        "Shortlisted"
]
    result = evaluate_accuracy(ai_results, hr_results)

    print("\n===== ATS Accuracy Report =====")
    print(f"TP = {result['TP']}")
    print(f"FP = {result['FP']}")
    print(f"FN = {result['FN']}")
    print(f"TN = {result['TN']}")

    print(f"\nPrecision = {result['Precision']}%")
    print(f"Recall = {result['Recall']}%")
    print(f"Accuracy = {result['Accuracy']}%")
    print(f"F1 Score = {result['F1 Score']}%")

    assert result["Accuracy"] >= 70