import pandas as pd
import streamlit as st

from load_data import load_data

csv_file = "Activities-26-01-19.csv"
df = load_data(csv_file)

st.header("Activity Metrics Over Time")

col1, col2 = st.columns(2)

with col1:
    activities = ["Löpning", "Cykling"]
    activity = st.pills("Activity", activities, default=activities[0])

# Filter for activity
activity_df = df[df["Aktivitetstyp"] == activity].copy()
activity_df["Datum"] = pd.to_datetime(activity_df["Datum"])

# Create tabs for different metrics
with col2:
    metrics = ["Distans", "Tid", "Total stigning"]
    metric = st.pills("Metric", metrics, default=metrics[0])

activity_df["Tid"] = activity_df["Tid"].dt.total_seconds() / 60  # minutes

# Create tabs for different resolutions
tab_day, tab_week, tab_month, tab_year = st.tabs(["Day", "Week", "Month", "Year"])


def plot_metric(period_freq, fmt, tab_label):
    """Aggregate chosen metric and plot bar chart with proper x-axis formatting."""
    temp_df = activity_df.copy()
    temp_df["Period"] = (
        temp_df["Datum"].dt.to_period(period_freq).apply(lambda p: p.start_time)
    )

    # Aggregate
    agg_df = (
        temp_df.groupby("Period", as_index=False)[metric].sum().sort_values("Period")
    )

    # Convert period to string for clean x-axis
    agg_df["PeriodStr"] = agg_df["Period"].dt.strftime(fmt)
    print(agg_df["PeriodStr"])

    with tab_label:
        st.bar_chart(agg_df.set_index("PeriodStr")[metric])


# Plot each tab
plot_metric("D", "%Y-%m-%d", tab_day)  # Day
plot_metric("W", "%Y-%W", tab_week)  # Week
plot_metric("M", "%Y-%m", tab_month)  # Month
plot_metric("Y", "%Y", tab_year)  # Year
