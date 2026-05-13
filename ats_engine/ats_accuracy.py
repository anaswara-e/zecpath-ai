def evaluate_accuracy(ai_results, hr_results):

    tp = fp = fn = tn = 0

    for ai, hr in zip(ai_results, hr_results):

        if ai == "Shortlisted" and hr == "Shortlisted":
            tp += 1

        elif ai == "Shortlisted" and hr == "Rejected":
            fp += 1

        elif ai == "Rejected" and hr == "Shortlisted":
            fn += 1

        else:
            tn += 1

    precision = round((tp / (tp + fp)) * 100, 2)
    recall = round((tp / (tp + fn)) * 100, 2)
    accuracy = round(((tp + tn) / len(ai_results)) * 100, 2)

    f1 = round(
        2 * ((precision * recall) / (precision + recall)),
        2
    )

    return {
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "Precision": precision,
        "Recall": recall,
        "Accuracy": accuracy,
        "F1 Score": f1
    }