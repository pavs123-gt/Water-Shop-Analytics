import pandas as pd

df = pd.read_csv("sample_transactions.csv")

# FIX can_size (10L → 10)
df["can_size"] = df["can_size"].str.replace("L", "", regex=False).astype(int)

df["date"] = pd.to_datetime(df["timestamp"]).dt.date

# Recalculate correctly
cans_per_customer = df.groupby("customer_id")["can_size"].sum().reset_index()
cans_per_customer.to_csv("test_cans_per_customer.csv", index=False)

cans_per_day = df.groupby("date")["can_size"].sum().reset_index()
cans_per_day.to_csv("test_cans_per_day.csv", index=False)

print(" Can analytics fixed and saved")
