import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set(style="whitegrid")

# Load data
visit_counts = pd.read_csv("customer_visit_counts.csv")
new_customers = pd.read_csv("new_customers.csv")
returning_customers = pd.read_csv("returning_customers.csv")
visit_log = pd.read_csv("visit_log.csv")

# Convert entry_time to datetime
visit_log["entry_time"] = pd.to_datetime(visit_log["entry_time"])

# -----------------------------
# 1️⃣ Pie Chart: New vs Returning Customers
# -----------------------------
labels = ['New Customers', 'Returning Customers']
sizes = [len(new_customers), len(returning_customers)]
colors = ['#66b3ff','#ff9999']

plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title("New vs Returning Customers")
plt.savefig("pie_new_vs_returning.png")
plt.close()
print("✅ Pie chart saved: pie_new_vs_returning.png")

# -----------------------------
# 2️⃣ Bar Chart: Top 10 Customers by Visit Count
# -----------------------------
top_customers = visit_counts.sort_values(by="visit_count", ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(x="customer_id", y="visit_count", data=top_customers, palette="viridis")
plt.title("Top 10 Customers by Visit Count")
plt.ylabel("Number of Visits")
plt.xlabel("Customer ID")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("bar_top_customers.png")
plt.close()
print("✅ Bar chart saved: bar_top_customers.png")

# -----------------------------
# 3️⃣ Daily Visits Line Chart
# -----------------------------
visit_log["date"] = visit_log["entry_time"].dt.date
daily_visits = visit_log.groupby("date").size().reset_index(name="visit_count")
plt.figure(figsize=(10,5))
sns.lineplot(x="date", y="visit_count", data=daily_visits, marker="o")
plt.title("Daily Visits")
plt.ylabel("Number of Visits")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("line_daily_visits.png")
plt.close()
print("✅ Line chart saved: line_daily_visits.png")

# -----------------------------
# 4️⃣ Optional: Visits per Hour (Peak Hour)
# -----------------------------
visit_log["hour"] = visit_log["entry_time"].dt.hour
hourly_visits = visit_log.groupby("hour").size().reset_index(name="visit_count")
plt.figure(figsize=(10,5))
sns.barplot(x="hour", y="visit_count", data=hourly_visits, palette="coolwarm")
plt.title("Visits per Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Visits")
plt.savefig("bar_visits_per_hour.png")
plt.close()
print(" Bar chart saved: bar_visits_per_hour.png")

print(" All analytics charts generated successfully!")
