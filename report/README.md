# COVID-19 Analysis — Quarto report

A published, narrative version of the `../notebooks/covid-cases-czechia.ipynb`
analysis. Shows the **full data pipeline** — code, reasoning, and charts — with
collapsible "Show code" toggles, rendered to a static website.

**Stack:** Quarto · Python (pandas, matplotlib) · executed against live JHU data.

## Preview locally
```bash
export PATH="$HOME/.local/quarto/bin:$PATH"   # if quarto isn't on PATH
quarto preview index.qmd
```
or render the static site:
```bash
quarto render          # outputs to _site/
```

## Before publishing — fill in 3 placeholders
Search-and-replace these in `_quarto.yml` and `index.qmd`:
- `YOUR-APP.streamlit.app`  → your deployed Streamlit dashboard URL
- `YOUR-USERNAME`           → your GitHub username/repo

## Publish to GitHub Pages (free)
From the repo root, the one-time setup:
```bash
cd report
quarto publish gh-pages
```
This builds the site, pushes it to a `gh-pages` branch, and gives you a public
`https://YOUR-USERNAME.github.io/covid-analysis/` URL. Re-run it to update.

> Alternative: in your GitHub repo Settings → Pages, point at the `gh-pages`
> branch. `quarto publish` configures this automatically the first time.

## Files
- `index.qmd` — the analysis (narrative + code + charts)
- `_quarto.yml` — site config (theme, code-fold, navbar)
- `styles.css` — light visual touch-ups
- `populations.csv` — bundled UN population data (so it renders anywhere)
- `_site/` — build output (git-ignored)
