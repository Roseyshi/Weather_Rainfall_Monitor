# Kenya Weather & Rainfall Monitor

A near-real-time weather dashboard for eight Kenyan locations. A scheduled GitHub Actions pipeline collects temperature, humidity and rainfall data every 15 minutes, and a Gradio dashboard visualises it on a live map and time series.

**Live dashboard:** https://huggingface.co/spaces/roseyshi/Weather_Rainfall_Monitor

<!-- Add a screenshot: save it as docs/dashboard.png and uncomment the line below -->
<!-- ![Dashboard screenshot](docs/dashboard.png) -->

## Why I built this

I wanted a small project that shows the full path from a public data source to a visualisation people can use: a scheduled extract, an incrementally updated dataset, and a dashboard that refreshes by itself, all on free tools. Weather and rainfall data is also directly relevant to agriculture and risk analysis.

## How it works

```
Open-Meteo API  ->  GitHub Actions (every 15 min)  ->  data/history.csv  ->  Gradio dashboard
                    runs fetch.py                      committed to repo     reads the CSV,
                                                                             refreshes every 60 s
```

1. **Extract.** `fetch.py` requests current conditions for all sites from the [Open-Meteo](https://open-meteo.com/) forecast API in a single call.
2. **Load.** New rows are appended to `data/history.csv`. Duplicate `(time, site)` pairs are dropped, and the file is capped at the latest 8,000 rows to keep it small.
3. **Schedule.** A GitHub Actions workflow runs the script every 15 minutes and commits the updated CSV back to the repository. A failed run triggers GitHub's standard failure notification.
4. **Visualise.** The dashboard (hosted on Hugging Face Spaces) reads the CSV from the repository's raw URL and redraws a map of the latest readings plus temperature and rainfall time series for the selected site.

## Locations monitored

Nairobi, Murang'a, Kisumu, Mombasa, Eldoret, Nakuru, Garissa and Kitale.

## Data collected

| Column | Description |
|---|---|
| `time` | Observation time (UTC) |
| `site` | Location name |
| `lat`, `lon` | Coordinates used for the request |
| `temp_c` | Air temperature at 2 m (°C) |
| `humidity` | Relative humidity at 2 m (%) |
| `rain_mm` | Precipitation (mm) |

## Tech stack

- **Python** (requests, pandas)
- **GitHub Actions** for scheduling and automation
- **Open-Meteo API** as the data source
- **Gradio** and **Plotly** for the dashboard
- **Hugging Face Spaces** for hosting

## Repository structure

```
.
├── .github/workflows/fetch.yml   # scheduled job (every 15 minutes)
├── data/history.csv              # accumulated observations
├── fetch.py                      # extract + load script
└── README.md
```

The dashboard code lives in the Hugging Face Space linked above.

## Run it locally

```bash
git clone https://github.com/Roseyshi/Weather_Rainfall_Monitor.git
cd Weather_Rainfall_Monitor
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install requests pandas
python fetch.py
```

Running `fetch.py` creates or updates `data/history.csv`. No API key is required.

## Limitations

- **Near-real-time, not real-time.** The source updates roughly every 15 minutes, and GitHub Actions schedules can be delayed by several minutes.
- **Model-based values.** Open-Meteo returns modelled data for the requested coordinates, not readings from a physical weather station at each site.
- **Free-tier behaviour.** The Hugging Face Space may take a moment to wake up after a period of inactivity, and GitHub can pause scheduled workflows in repositories with no activity for an extended period.
- **Small history.** Only the most recent 8,000 rows are kept, so this is not a long-term archive.

## Possible improvements

- Add validation rules in `fetch.py` (for example, reject negative rainfall or implausible temperatures) and log rejected rows.
- Add alert thresholds, such as flagging heavy rainfall at a site.
- Add `pytest` tests for the extraction and validation logic.
- Store history in a database instead of a CSV.

## Data source and attribution

Weather data is provided by [Open-Meteo](https://open-meteo.com/). Please review their terms of use and attribution requirements before reusing this project, as the free API is intended for non-commercial use.

## Author

Roseline Wahome, [LinkedIn](https://www.linkedin.com/in/roseline-wahome-dataanalyst/) | [GitHub](https://github.com/Roseyshi) | [Portfolio](https://roseyshi.github.io/Portfolio)
