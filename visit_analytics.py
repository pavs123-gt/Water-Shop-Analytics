import pandas as pd

# Load visit data
visit_df = pd.read_csv("visit_log.csv")

# Convert entry_time to datetime
visit_df["entry_time"] = pd.to_datetime(visit_df["entry_time"])

# -----------------------------
# 1️⃣ Visits per Day
# -----------------------------
visit_df["date"] = visit_df["entry_time"].dt.date
daily_visits = visit_df.groupby("date").size()

# -----------------------------
# 2️⃣ Visits per Month
# -----------------------------
visit_df["month"] = visit_df["entry_time"].dt.to_period("M")
monthly_visits = visit_df.groupby("month").size()

# -----------------------------
# 3️⃣ Visits per Quarter
# -----------------------------
visit_df["quarter"] = visit_df["entry_time"].dt.to_period("Q")
quarterly_visits = visit_df.groupby("quarter").size()

# -----------------------------
# 4️⃣ Repeat Visits (by track_id)
# -----------------------------
repeat_visits = visit_df["track_id"].value_counts()
repeat_visits = repeat_visits[repeat_visits > 1]

# -----------------------------
# SAVE RESULTS
# -----------------------------
daily_visits.to_csv("daily_visits.csv", header=["visit_count"])
monthly_visits.to_csv("monthly_visits.csv", header=["visit_count"])
quarterly_visits.to_csv("quarterly_visits.csv", header=["visit_count"])
repeat_visits.to_csv("repeat_visits.csv", header=["repeat_count"])

# -----------------------------
# PRINT SUMMARY
# -----------------------------
print("✅ VISIT ANALYTICS COMPLETED")
print("Total visits:", len(visit_df))
print("Repeat visitors:", len(repeat_visits))
print("Files generated:")
print("- daily_visits.csv")
print("- monthly_visits.csv")
print("- quarterly_visits.csv")
print("- repeat_visits.csv")
