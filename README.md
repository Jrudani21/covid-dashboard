# COVID-19 Global Dashboard

A real-time COVID-19 global statistics dashboard built with Streamlit and Plotly, powered by the [disease.sh](https://disease.sh) public API.

## Features

- Global KPIs: total cases, active, recovered, deaths, fatality rate
- 180-day trend chart (cases, deaths, recovered)
- Top 15 countries bar chart
- World choropleth map (cases per 1M population)
- Searchable country data table

## Run Locally

```bash
pip install -r requirements.txt
streamlit run covid_dashboard.py
```

Open http://localhost:8501 in your browser.
