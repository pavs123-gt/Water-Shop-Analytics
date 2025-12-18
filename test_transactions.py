import pandas as pd

# Load transaction data
transactions = pd.read_csv("sample_transactions.csv")

# Ensure timestamp is datetime
transactions["timestamp"] = pd.to_datetime(transactions["timestamp"], errors="coerce")

# 1️⃣ Total spend per customer
total_spent = transactions.groupby("customer_id")["amount"].sum().reset_index()
total_spent.rename(columns={"amount": "total_spent"}, inplace=True)
total_spent.to_csv("test_total_spent.csv", index=False)

# 2️⃣ Payment mode summary
payment_summary = transactions["payment_mode"].value_counts().reset_index()
payment_summary.columns = ["payment_mode", "count"]
payment_summary.to_csv("test_payment_summary.csv", index=False)

# 3️⃣ Unpaid transactions
unpaid = transactions[transactions["status"]=="Unpaid"]
unpaid.to_csv("test_unpaid.csv", index=False)

# 4️⃣ Repeat defaulters
repeat_defaulters = unpaid.groupby("customer_id").size().reset_index(name="unpaid_count")
repeat_defaulters = repeat_defaulters[repeat_defaulters["unpaid_count"] > 1]
repeat_defaulters.to_csv("test_repeat_defaulters.csv", index=False)

print("✅ Transaction validation completed. Outputs:")
print("- test_total_spent.csv")
print("- test_payment_summary.csv")
print("- test_unpaid.csv")
print("- test_repeat_defaulters.csv")
