import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="COVID-19 Global Dashboard", layout="wide", page_icon="🦠")

st.title("🦠 COVID-19 Global Dashboard")
st.caption(f"Data sourced from disease.sh · Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@st.cache_data(ttl=600)
def fetch_global():
    return requests.get("https://disease.sh/v3/covid-19/all").json()

@st.cache_data(ttl=600)
def fetch_historical():
    return requests.get("https://disease.sh/v3/covid-19/historical/all?lastdays=180").json()

@st.cache_data(ttl=600)
def fetch_countries():
    return requests.get("https://disease.sh/v3/covid-19/countries?sort=cases").json()

with st.spinner("Fetching live data..."):
    global_data = fetch_global()
    historical = fetch_historical()
    countries = fetch_countries()

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
st.subheader("Global Trend (Last 180 Days)")

dates = list(historical["cases"].keys())
cases_vals = list(historical["cases"].values())
deaths_vals = list(historical["deaths"].values())
recovered_vals = list(historical["recovered"].values())

trend_df = pd.DataFrame({
    "Date": pd.to_datetime(dates),
    "Cases": cases_vals,
    "Deaths": deaths_vals,
    "Recovered": recovered_vals,
})

metric = st.selectbox("Select metric", ["Cases", "Deaths", "Recovered"])
fig = px.area(
    trend_df,
    x="Date",
    y=metric,
    color_discrete_map={"Cases": "#1f77b4", "Deaths": "#d62728", "Recovered": "#2ca02c"},
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
