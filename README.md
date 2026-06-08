# COVID-19 Data Analysis

Personal COVID-19 data-analytics and charting work (2020–2023), mostly focused on
Czechia, using JHU CSSE global data plus Czech Ministry of Health (ÚZIS) datasets.

## 🔗 Live showcase

| | Link |
|---|---|
| 📄 **Analysis report** (code + narrative + charts) | https://josefrichter.github.io/covid-analysis/ |
| 📊 **Interactive dashboard** | https://covid-czechia.streamlit.app |

Both run the same pipeline — ranking countries by average daily new cases per 100k —
and fetch Johns Hopkins data live, so they need no bundled datasets. The report
(`report/`, built with Quarto) shows *how* the analysis works; the dashboard
(`dashboard/`, built with Streamlit) lets you explore it interactively.

## Folder structure

### `notebooks/` — my own work
| Notebook | What it does | Data source |
|---|---|---|
| `covid-cases-czechia.ipynb` | **Most polished.** Average daily increments per 100k inhabitants, country rankings, comparisons. Has markdown narrative. | JHU global + `populations.csv` |
| `cov-deaths.ipynb` | Deaths analysis, per-capita normalized, multiple charts | JHU global + `populations.csv` |
| `covid-increments.ipynb` | Daily case increments, per-100k normalization | JHU global + `populations.csv` |
| `cov-cz-prophet.ipynb` | Time-series forecasting of Czech cases with Facebook Prophet | JHU global |
| `cov-test-age-dist.ipynb` | Test positivity by age / district | `modely_*.csv` (ÚZIS) |
| `cov-death-distribution.ipynb` | Death distribution analysis | `umrti.csv` (ÚZIS) |
| `covid-obec.ipynb` | Municipality-level (obec) case data | `obec.csv` (ÚZIS, ~181 MB) |
| `cov-capacity.ipynb` | Hospital capacity exploration | — |
| `covid_daily_cases.ipynb` | Concatenates JHU daily report CSVs | local `COVID-19` clone (see note) |
| `Untitled.ipynb` | Scratch / unnamed | — |

### `data/` — supporting datasets
- `populations.csv` — country populations, used for per-capita normalization
- `obec.csv` — Czech municipality-level case data (large)
- `umrti.csv` — Czech deaths
- `modely_*.csv` — ÚZIS district statistics & test positivity
- `umrti data/` — daily snapshots of nakazeni/vyleceni/umrti/testy (Oct 2020)

### `third-party-repos/` — cloned public repos (NOT my work)
- `COVID-19/` — JHU CSSE official dataset (github.com/CSSEGISandData/COVID-19)
- `covid19-dashboard/` — GitHub's covid19-dashboard
- `covidify/` — AaronWard/covidify
- `COVID19-Graphs/` — alainrochette/COVID19-Graphs

### `reference-notebooks/` — downloaded, NOT my work
- `coronavirus-covid-19-visualization-prediction*.ipynb` — a popular Kaggle
  notebook, kept for reference.

## Note on paths
Most notebooks pull JHU data live from `raw.githubusercontent.com`, so they don't
need the local clones. Exception: `covid_daily_cases.ipynb` reads from a relative
`./COVID-19/...` path — update it to `../third-party-repos/COVID-19/...` if you re-run it.
