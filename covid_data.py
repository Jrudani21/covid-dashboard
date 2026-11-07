# Copyright (c) 2026 Janak Rudani. All rights reserved.
# Provenance: Jrudani21/covid-dashboard/covid_data.py 1f6a0f1f2f11866a
"""Fetch and shape disease.sh data. No Streamlit here, so it can be tested alone."""
from datetime import datetime

import requests

BASE = "https://disease.sh/v3/covid-19/"


def get_json(path, timeout=15):
    """GET one endpoint. Raises requests.RequestException on any failure."""
    r = requests.get(BASE + path, timeout=timeout)
    r.raise_for_status()
    return r.json()


def parse_day(s):
    return datetime.strptime(s, "%m/%d/%y").date()


def trend_window(historical, days=180):
    """Last `days` entries of the cases and deaths series, plus the feed's own last date.

    The window is taken from the series itself, so if the feed stops, the dates show it.
    Recovered is left out: the feed reports 0 for it after Sep 2022.
    """
    dates = list(historical["cases"])[-days:]
    return {
        "dates": [parse_day(d) for d in dates],
        "Cases": [historical["cases"][d] for d in dates],
        "Deaths": [historical["deaths"][d] for d in dates],
    }
