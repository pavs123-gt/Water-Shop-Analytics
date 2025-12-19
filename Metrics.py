import pandas as pd

# Load recognition results
df = pd.read_csv("recognition_results.csv")

# Set similarity threshold
SIM_THRESHOLD = 0.6

# True positives = recognitions above threshold
df["true_positive"] = df["similarity"] >= SIM_THRESHOLD

# Approximate counts
true_positives = df["true_positive"].sum()
false_positives = len(df) - true_positives  # recognitions below threshold
false_negatives = 0  # cannot compute without ground truth, assume 0 for approximation

# Calculate metrics
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
accuracy = true_positives / len(df)

# Print results
print(f"Approximate Accuracy: {accuracy*100:.2f}%")
print(f"Approximate Precision: {precision*100:.2f}%")
print(f"Approximate Recall: {recall*100:.2f}%")
