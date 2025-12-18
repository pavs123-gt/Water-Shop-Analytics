import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

st.set_page_config(page_title="Water Shop Analytics", layout="wide")

st.title("💧 Water Shop Analytics Dashboard")
st.subheader("Auto Analytics – No Login Required")
st.success("Dashboard loaded successfully ✅")

# --------------------------------------------------
# Automatically detect ALL CSV files
# --------------------------------------------------
csv_files = [f for f in os.listdir(".") if f.endswith(".csv")]

if not csv_files:
    st.write("No data files found.")
else:
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)

            # Clean data
            df.dropna(how="all", inplace=True)
            df.dropna(axis=1, how="all", inplace=True)
            df.reset_index(drop=True, inplace=True)

            if df.empty:
                continue  # silently skip empty CSVs

            st.markdown("---")
            st.subheader(f"📄 {csv_file}")

            # Safe display (NO Streamlit JS error)
            if df.shape[0] == 1 or df.shape[1] == 1:
                st.table(df)
            else:
                st.dataframe(df, use_container_width=True)

            
            # Auto Charts (if possible)
            
            if "date" in df.columns and "visit_count" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df = df.dropna(subset=["date"])

                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(df["date"], df["visit_count"], marker="o")
                ax.set_title("Visits Trend")
                ax.set_xlabel("Date")
                ax.set_ylabel("Visits")
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)

            if "customer_id" in df.columns and "visit_count" in df.columns:
                st.bar_chart(df.set_index("customer_id")["visit_count"])

        except Exception:
            # Skip problematic CSV silently
            continue
