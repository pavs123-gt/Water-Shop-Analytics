import pandas as pd

df = pd.read_csv("recognition_results.csv")

total = len(df)
unique_customers = df["customer_id"].nunique()

print("Total recognitions:", total)
print("Unique customers:", unique_customers)

if "similarity" in df.columns:
    print("Average similarity:", df["similarity"].mean())
    print("Min similarity:", df["similarity"].min())
    print("Max similarity:", df["similarity"].max())
