# COVID-19 Daily Increments Dashboard

Interactive dashboard built from my 2020 notebook analysis
(`../notebooks/covid-cases-czechia.ipynb`). It ranks countries by their average
daily new COVID-19 cases per 100k inhabitants and lets you compare trajectories.

**Stack:** Python · Streamlit · Plotly · pandas
**Data:** [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19) (live) + UN population data (`populations.csv`)

## What it shows
- **KPIs** — a chosen country's global rank, daily cases/100k, absolute daily average
- **Ranking** — top-N countries by daily new cases per 100k, with one country highlighted
- **Trajectories** — N-day smoothed per-100k curves for any set of countries
- **Data table** — sortable, with CSV export

## Interactive controls
Averaging window (N days), as-of date, number of countries, minimum population
filter, highlighted country, and the trajectory country picker.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (free, public)
Push this `dashboard/` folder to a GitHub repo, then point
[share.streamlit.io](https://share.streamlit.io) at `app.py`. No secrets or
database needed — the JHU CSV is fetched live and cached for 6 hours.

## Note
The data is historical (the JHU feed stopped updating in March 2023), so the
dashboard is a showcase of the analysis and engineering, not a live tracker.
