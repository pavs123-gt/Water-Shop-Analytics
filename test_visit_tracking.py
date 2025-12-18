import pandas as pd

# Load the validation CSV
df = pd.read_csv("visit_validation.csv")

# Convert times to datetime
df["entry_time"] = pd.to_datetime(df["entry_time"], errors="coerce")
df["exit_time"] = pd.to_datetime(df["exit_time"], errors="coerce")

#  Count visits per customer
visit_counts = df["customer_id"].value_counts()
print("Total visits per customer:")
print(visit_counts)

#  Identify repeat visitors (more than 1 visit)
repeat_visitors = visit_counts[visit_counts > 1]
print("\nRepeat visitors:")
print(repeat_visitors)

#  Check duration_seconds sanity
print("\nDuration statistics (seconds):")
print(df["duration_seconds"].describe())

# Save test output to CSV
visit_counts.to_csv("test_visit_counts.csv")
repeat_visitors.to_csv("test_repeat_visitors.csv")

print("\n  Visit tracking test completed")
print("Output saved as 'test_visit_counts.csv' and 'test_repeat_visitors.csv'")
