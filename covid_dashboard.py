# Copyright (c) 2026 Janak Rudani. All rights reserved.
# Provenance: Jrudani21/covid-dashboard/covid_dashboard.py 82873b2fa59b7790
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

from covid_data import get_json, trend_window

st.set_page_config(page_title="COVID-19 Global Dashboard", layout="wide", page_icon="🦠")

st.title("🦠 COVID-19 Global Dashboard")

@st.cache_data(ttl=600)
def fetch(path):
    return get_json(path)

try:
    with st.spinner("Fetching data..."):
        global_data = fetch("all")
        historical = fetch("historical/all?lastdays=all")
        countries = fetch("countries?sort=cases")
except requests.RequestException as e:
    st.error(f"Could not load data from disease.sh: {e}")
    st.stop()

trend = trend_window(historical)
if not trend["dates"]:
    st.error("The historical series is empty.")
    st.stop()
last_day = trend["dates"][-1]
st.caption(f"Data from disease.sh. The historical series ends on {last_day:%d %b %Y}; the totals below are the API's latest.")

# --- Global KPIs ---
st.subheader("Global Overview")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Cases", f"{global_data['cases']:,}")
c2.metric("Active Cases", f"{global_data['active']:,}")
c3.metric("Recovered", f"{global_data['recovered']:,}")
c4.metric("Deaths", f"{global_data['deaths']:,}")
c5.metric("Case Fatality Rate", f"{global_data['deaths']/global_data['cases']*100:.2f}%")

st.divider()

# --- Historical trend ---
st.subheader(f"Global Trend ({trend['dates'][0]:%d %b %Y} to {last_day:%d %b %Y})")

trend_df = pd.DataFrame({
    "Date": pd.to_datetime(trend["dates"]),
    "Cases": trend["Cases"],
    "Deaths": trend["Deaths"],
})

metric = st.selectbox("Select metric", ["Cases", "Deaths"])
fig = px.area(
    trend_df,
    x="Date",
    y=metric,
    color_discrete_map={"Cases": "#1f77b4", "Deaths": "#d62728"},
    template="plotly_dark",
)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Top countries ---
st.subheader("Top 15 Countries by Cases")

country_df = pd.DataFrame([{
    "Country": c["country"],
    "Cases": c["cases"],
    "Deaths": c["deaths"],
    "Recovered": c.get("recovered", 0),
    "Active": c["active"],
    "Deaths/1M pop": c.get("deathsPerOneMillion", 0),
    "Cases/1M pop": c.get("casesPerOneMillion", 0),
} for c in countries])

top15 = country_df.head(15)

fig2 = px.bar(
    top15,
    x="Cases",
    y="Country",
    orientation="h",
    color="Deaths",
    color_continuous_scale="Reds",
    template="plotly_dark",
    labels={"Cases": "Total Cases", "Country": ""},
)
fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=420, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Top 15 Countries by Cases per Million (population 1M or more)")
per_m = country_df.merge(
    pd.DataFrame([{"Country": c["country"], "Population": c.get("population") or 0} for c in countries]),
    on="Country",
)
per_m = per_m[per_m["Population"] >= 1_000_000].nlargest(15, "Cases/1M pop")
fig2b = px.bar(
    per_m, x="Cases/1M pop", y="Country", orientation="h",
    template="plotly_dark", labels={"Cases/1M pop": "Cases per 1M", "Country": ""},
)
fig2b.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=420, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig2b, use_container_width=True)

st.divider()

# --- World map ---
st.subheader("World Map — Cases per 1M Population")

map_df = country_df.copy()
fig3 = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    color="Cases/1M pop",
    color_continuous_scale="YlOrRd",
    template="plotly_dark",
    labels={"Cases/1M pop": "Cases per 1M"},
)
fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=420)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- Country data table ---
st.subheader("All Countries — Searchable Table")
search = st.text_input("Search country", "")
filtered = country_df[country_df["Country"].str.contains(search, case=False)] if search else country_df
st.dataframe(filtered.reset_index(drop=True), use_container_width=True, height=400)
