"""Run: python test_covid_data.py  (no network, no Streamlit)"""
from datetime import date

from covid_data import trend_window

h = {"cases": {"1/1/23": 1, "1/2/23": 3, "1/3/23": 6},
     "deaths": {"1/1/23": 0, "1/2/23": 1, "1/3/23": 2},
     "recovered": {"1/1/23": 0, "1/2/23": 0, "1/3/23": 0}}
w = trend_window(h, days=2)
assert w["dates"] == [date(2023, 1, 2), date(2023, 1, 3)], w
assert w["Cases"] == [3, 6] and w["Deaths"] == [1, 2]
assert "Recovered" not in w
print("ok")
