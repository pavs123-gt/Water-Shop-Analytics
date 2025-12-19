import pandas as pd

tx = pd.read_csv("sample_transactions.csv")
customers = pd.read_csv("unique_customers.csv")

linked = tx[tx["customer_id"].isin(customers["customer_id"])]

print("Total transactions:", len(tx))
print("Linked transactions:", len(linked))

assert len(tx) == len(linked), " Unlinked transactions found"
print("All transactions are linked to recognized customers")
