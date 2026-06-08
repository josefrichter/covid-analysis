"""
COVID-19 Daily Increments Dashboard
-----------------------------------
Interactive version of the `covid-cases-czechia.ipynb` analysis.

Methodology (unchanged from the original notebook):
  1. Pull confirmed-cases time series from the Johns Hopkins CSSE repo.
  2. Group regions into single countries and join UN population data.
  3. For a chosen window N, compute the average DAILY increment of new cases
     over the last N days  ->  (cases_today - cases_N_days_ago) / N
  4. Normalize per 100k inhabitants so countries are comparable.
  5. Rank descending and visualize.

Run locally:   streamlit run app.py
Deploy free:   push this folder to GitHub -> share.streamlit.io
"""

import datetime as dt

import pandas as pd
import plotly.express as px
import streamlit as st

JHU_URL = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
    "csse_covid_19_data/csse_covid_19_time_series/"
    "time_series_covid19_confirmed_global.csv"
)

st.set_page_config(page_title="COVID Daily Increments", page_icon="📈", layout="wide")


# --------------------------------------------------------------------------- #
# Data loading (cached for 6h so the JHU CSV isn't refetched on every click)
# --------------------------------------------------------------------------- #
@st.cache_data(ttl=6 * 3600)
def load_cases() -> pd.DataFrame:
    df = pd.read_csv(JHU_URL, index_col="Country/Region")
    # bigger countries are split into regions -> collapse to one row per country
    cases = df.drop(columns=["Province/State", "Lat", "Long"]).groupby("Country/Region").sum()
    cases.columns = pd.to_datetime(cases.columns)  # date columns -> real datetimes
    return cases


@st.cache_data
def load_populations() -> pd.Series:
    pop = pd.read_csv("populations.csv").groupby("Location")["PopTotal"].sum()
    return pop * 1000  # source is in thousands -> absolute people


cases = load_cases()
population = load_populations()
date_cols = list(cases.columns)
last_date = date_cols[-1].date()


# --------------------------------------------------------------------------- #
# Sidebar controls
# --------------------------------------------------------------------------- #
st.sidebar.header("Parameters")
N = st.sidebar.slider("Averaging window (days)", 1, 21, 7,
                      help="Daily increment is averaged over the last N days.")
as_of = st.sidebar.date_input("As-of date", last_date,
                              min_value=date_cols[N].date(), max_value=last_date)
top_n = st.sidebar.slider("Countries in ranking", 5, 50, 25)
min_pop_m = st.sidebar.slider("Min. population (millions)", 0.0, 50.0, 1.0, 0.5)
highlight = st.sidebar.text_input("Highlight country", "Czechia")

# resolve the as-of date to the nearest available column
as_of_ts = pd.Timestamp(as_of)
end_i = date_cols.index(min((d for d in date_cols if d >= as_of_ts), default=date_cols[-1]))
start_i = end_i - N


# --------------------------------------------------------------------------- #
# Core computation (the notebook's logic, vectorised over all countries)
# --------------------------------------------------------------------------- #
@st.cache_data
def compute(N, end_i, min_pop, as_of_str):
    df = cases.copy()
    df.insert(0, "Population", population)
    df = df[df["Population"] >= min_pop]

    end_col, start_col = date_cols[end_i], date_cols[end_i - N]
    df["NdayIncrement"] = df[end_col] - df[start_col]
    df["DailyAvg"] = df["NdayIncrement"] / N
    df["DailyAvgPer100k"] = df["DailyAvg"] / df["Population"] * 100_000

    out = df[["Population", "NdayIncrement", "DailyAvg", "DailyAvgPer100k"]].copy()
    return out.sort_values("DailyAvgPer100k", ascending=False)


result = compute(N, end_i, min_pop_m * 1_000_000, str(as_of))
ranking = result.head(top_n).reset_index()


# --------------------------------------------------------------------------- #
# Header + KPIs
# --------------------------------------------------------------------------- #
st.title("📈 COVID-19 — Average Daily New Cases per 100k")
st.caption(
    f"Source: Johns Hopkins CSSE · window = {N} days · "
    f"as of {date_cols[end_i].date()} · {len(result)} countries"
)

if highlight in result.index:
    rank = result.index.get_loc(highlight) + 1
    rate = result.loc[highlight, "DailyAvgPer100k"]
    daily = result.loc[highlight, "DailyAvg"]
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{highlight} — global rank", f"#{rank}", f"of {len(result)}")
    c2.metric("Daily new cases / 100k", f"{rate:.1f}")
    c3.metric("Avg new cases / day", f"{daily:,.0f}")
else:
    st.info(f"'{highlight}' not found at this population threshold — adjust the filter.")


# --------------------------------------------------------------------------- #
# Ranking bar chart (highlighted country in a contrasting colour)
# --------------------------------------------------------------------------- #
st.subheader(f"Top {top_n} countries by daily new cases per 100k")
ranking["color"] = (ranking["Country/Region"] == highlight).map(
    {True: highlight, False: "Other countries"}
)
fig = px.bar(
    ranking, x="Country/Region", y="DailyAvgPer100k", color="color",
    color_discrete_map={highlight: "#e4572e", "Other countries": "#4a6fa5"},
    labels={"DailyAvgPer100k": "Daily new cases / 100k", "Country/Region": ""},
    # keep bars in ranked order — without this, colouring splits the data into
    # separate traces and the highlighted country gets pushed to the axis end
    category_orders={"Country/Region": ranking["Country/Region"].tolist()},
    height=480,
)
fig.update_layout(showlegend=False, margin=dict(t=10, b=0))
st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------------------------- #
# Trajectory comparison (7-day rolling avg per 100k, last 120 days)
# --------------------------------------------------------------------------- #
st.subheader("Trend over time")
st.caption(
    f"Daily new cases per 100k over the last 120 days ({N}-day rolling average). "
    "Each line shows how a country's outbreak rose and fell — pick any countries to compare."
)
default_sel = [c for c in [highlight, "Sweden", "Germany", "Italy"] if c in cases.index]
picks = st.multiselect("Countries", sorted(cases.index), default=default_sel)

if picks:
    daily_new = cases.loc[picks].diff(axis=1)
    per100k = daily_new.div(population.loc[picks], axis=0) * 100_000
    smoothed = per100k.T.rolling(N).mean().tail(120)
    smoothed.index.name = "Date"
    long = smoothed.reset_index().melt("Date", var_name="Country", value_name="per100k")
    line = px.line(long, x="Date", y="per100k", color="Country",
                   labels={"per100k": "Daily new cases / 100k (N-day avg)"}, height=420)
    line.update_layout(margin=dict(t=10, b=0))
    st.plotly_chart(line, use_container_width=True)


# --------------------------------------------------------------------------- #
# Table + CSV download
# --------------------------------------------------------------------------- #
with st.expander("Show data table"):
    show = result.head(top_n).copy()
    show["Population"] = (show["Population"] / 1e6).round(2)
    show = show.rename(columns={"Population": "Population (M)"})
    st.dataframe(show.style.format({
        "NdayIncrement": "{:,.0f}", "DailyAvg": "{:,.0f}", "DailyAvgPer100k": "{:.1f}",
    }), use_container_width=True)
    st.download_button("Download CSV", result.to_csv().encode(),
                       f"covid_increments_{date_cols[end_i].date()}.csv", "text/csv")
