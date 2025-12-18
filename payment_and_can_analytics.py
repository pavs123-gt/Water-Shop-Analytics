import pandas as pd

# 1️⃣ Read your CSV and prepare analytics (your previous code)
df = pd.read_csv('sample_transactions.csv')
df['can_size'] = pd.to_numeric(df['can_size'].str.replace('L','', regex=False), errors='coerce')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['Date'] = pd.to_datetime(df['timestamp']).dt.date

total_spend = df.groupby('customer_id')['amount'].sum().reset_index()
total_spend.rename(columns={'amount':'TotalSpend'}, inplace=True)

paid_unpaid_counts = df['status'].value_counts()
cans_per_customer = df.groupby('customer_id')['can_size'].sum().reset_index()
cans_per_day = df.groupby('Date')['can_size'].sum().reset_index()
payment_summary = df['payment_mode'].value_counts()

# 2️⃣ Save analytics to Excel
with pd.ExcelWriter('analytics_report.xlsx') as writer:
    total_spend.to_excel(writer, sheet_name='Total_Spend', index=False)
    paid_unpaid_counts.to_frame().to_excel(writer, sheet_name='Paid_vs_Unpaid', index=True)
    cans_per_customer.to_excel(writer, sheet_name='Cans_per_Customer', index=False)
    cans_per_day.to_excel(writer, sheet_name='Cans_per_Day', index=False)
    payment_summary.to_frame().to_excel(writer, sheet_name='Payment_Modes', index=True)

print("Analytics saved successfully to 'analytics_report.xlsx'.")

# Now add the plotting code
import matplotlib.pyplot as plt

plt.figure(figsize=(14,6))  # Make the figure wider

# Bar chart
plt.bar(total_spend['customer_id'], total_spend['TotalSpend'], color='skyblue')

# Rotate X-axis labels and align them
plt.xticks(rotation=45, ha='right')

# Add axis labels and title
plt.xlabel('Customer ID')
plt.ylabel('Total Spend')
plt.title('Total Spend per Customer')

# Add grid lines for readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust layout to prevent clipping of labels
plt.tight_layout()

# Save chart as PNG
plt.savefig('total_spend_per_customer.png')
plt.close()

df['timestamp'] = pd.to_datetime(df['timestamp'])  # already partially done before
df['Hour'] = df['timestamp'].dt.hour  # for traffic analysis

# 1 First and last customer per day
first_last_customers = df.sort_values('timestamp').groupby('Date').agg(
    First_Customer=('customer_id', 'first'),
    First_Time=('timestamp', 'first'),
    Last_Customer=('customer_id', 'last'),
    Last_Time=('timestamp', 'last')
).reset_index()

print("\nFirst and Last Customer per Day:")
print(first_last_customers)

# 2️ Peak and low-traffic hours
traffic_per_hour = df.groupby('Hour').size().reset_index(name='Customer_Count')
peak_hour = traffic_per_hour.loc[traffic_per_hour['Customer_Count'].idxmax()]
low_hour = traffic_per_hour.loc[traffic_per_hour['Customer_Count'].idxmin()]

print("\nCustomer Traffic per Hour:")
print(traffic_per_hour)
print(f"\nPeak Hour: {peak_hour['Hour']} with {peak_hour['Customer_Count']} customers")
print(f"Low Hour: {low_hour['Hour']} with {low_hour['Customer_Count']} customers")

# Save shop activity insights to Excel
with pd.ExcelWriter('shop_activity_insights.xlsx') as writer:
    first_last_customers.to_excel(writer, sheet_name='First_Last_Customers', index=False)
    traffic_per_hour.to_excel(writer, sheet_name='Traffic_per_Hour', index=False)

print("\nShop activity insights saved to 'shop_activity_insights.xlsx'.")






