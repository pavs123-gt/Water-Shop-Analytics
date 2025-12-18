import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(page_title="Water Shop Analytics", layout="wide")
st.title(" Water Shop Analytics Dashboard")
st.subheader("Integrated Analytics – All CSV outputs")
st.success("Dashboard loaded successfully ")

# 1️ Can Analytics
cans_per_customer = pd.read_csv("test_cans_per_customer.csv")
cans_per_day = pd.read_csv("test_cans_per_day.csv")

st.markdown("### Total Cans per Customer")
st.dataframe(cans_per_customer)

st.markdown("### Total Cans per Day")
st.dataframe(cans_per_day)

# Plot total cans per day
fig1, ax1 = plt.subplots(figsize=(10,4))
ax1.plot(
    pd.to_datetime(cans_per_day["date"]),
    cans_per_day["can_size"],
    marker="o"
)
ax1.set_title("Daily Can Fill Trend")
ax1.set_xlabel("Date")
ax1.set_ylabel("Total Cans")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)


