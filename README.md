# COVID-19 Global Dashboard – Real-Time Pandemic Tracker

A live pandemic statistics application built with Streamlit and Plotly, connected to the disease.sh public API. The dashboard surfaces global and country-level COVID-19 metrics through five interactive views, refreshed every 10 minutes via Streamlit's caching layer.

## Dashboard Views

- **Global KPIs**: Total cases, active cases, recoveries, deaths, and a calculated case fatality rate derived directly from the live global endpoint
- **Trend Analysis**: Area chart of cases or deaths over the trailing 180 entries of the historical feed. The title shows the real date range; the feed currently ends in March 2023, so the page says so instead of implying it is current
- **Country Rankings**: Top 15 by total cases (color = deaths) and top 15 by cases per million for countries with 1M or more people
- **Choropleth Map**: Cases per million population across all countries on a yellow-to-red gradient, making per-capita burden visible at a glance
- **Data Explorer**: Searchable, filterable table covering all countries with absolute and per-capita metrics

## Key Design Decisions

- **10-minute cache interval** on all API calls keeps the UI responsive while limiting redundant network requests
- **Dark chart template** across all Plotly figures keeps the visual language consistent with a data-analyst aesthetic
- **Cases per million** (not raw counts) in the choropleth normalizes for population size — a more honest comparison across large and small nations
- **Modular fetch functions** isolate global, historical, and country endpoints so each view loads and caches independently

## Results

Live data from disease.sh · 180-day historical window · 200+ countries on the choropleth · sub-second chart renders with cached data

## Technical Stack

| Layer | Tools |
|---|---|
| Web interface | Streamlit |
| Visualizations | Plotly |
| Data manipulation | pandas |
| API calls | requests |

## Run Locally

```bash
pip install -r requirements.txt
streamlit run covid_dashboard.py
```

Open http://localhost:8501 in your browser.
