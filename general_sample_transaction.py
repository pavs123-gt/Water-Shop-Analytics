import pandas as pd
import random
from datetime import datetime, timedelta

# Load your customer IDs
customers = pd.read_csv("unique_customers.csv")["customer_id"].tolist()

# Generate 100 sample transactions
num_transactions = 100
transactions = []

start_time = datetime(2025, 12, 14, 9, 0, 0)

for i in range(num_transactions):
    customer_id = random.choice(customers)
    timestamp = start_time + timedelta(minutes=random.randint(0, 480))  # 8 hours of operation
    payment_mode = random.choice(["Cash", "UPI", "Coins"])
    can_size = random.choice(["10L", "20L"])
    amount = 10 if can_size == "10L" else 20
    status = random.choices(["Paid", "Unpaid"], weights=[0.9, 0.1])[0]
    
    transactions.append({
        "transaction_id": f"T{i+1:03d}",
        "customer_id": customer_id,
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "payment_mode": payment_mode,
        "can_size": can_size,
        "amount": amount,
        "status": status
    })

# Save to CSV
df = pd.DataFrame(transactions)
df.to_csv("sample_transactions.csv", index=False)
print("✅ Sample transaction data generated: sample_transactions.csv")
