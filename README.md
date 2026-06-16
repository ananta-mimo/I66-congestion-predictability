# Congestion Predictability Ceiling on I-66 ITB: An Endogenous TTI Baseline Study

This repository contains the code, outputs, and analysis for a study on freeway congestion prediction using probe-based Travel Time Index (TTI) data on the I-66 Inside the Beltway (ITB) corridor in Northern Virginia. The paper is currently under peer review at *Transportation Research Part C: Emerging Technologies*.

> **Note:** Raw data is not included in this repository due to licensing restrictions (RITIS/INRIX probe data, SmarterRoads API, VDOT crash records). The pipeline is fully reproducible with access to these sources. See [Data Sources](#data-sources) below.

---

## Research Summary

This study establishes a **predictability ceiling** for short-term freeway congestion forecasting using only endogenous TTI signals (lags, rolling statistics, calendar features). It addresses the question: *how much predictive value can be extracted from travel time history alone, before adding exogenous signals such as tolls, weather, or events?*

Key contributions:

- A rigorous endogenous baseline across 41 TMCs on I-66 ITB (EB + WB), spanning 2022–2025
- Multi-horizon forecasting at 5, 15, and 30-minute prediction horizons
- Persistence baseline comparison with XGBoost, Random Forest, and Linear Regression
- Spatial generalization experiments: pooled cross-TMC model and leave-one-TMC-out (LOTO)
- Predictability ceiling analysis: how volatility at a segment level bounds achievable accuracy
- XGBoost hyperparameter tuning validated as marginal; reported as a robustness check

The I-66 ITB corridor has a unique asymmetric tolling structure (EB tolled during AM peak, WB during PM peak), making it a particularly rich environment for studying congestion dynamics.
## Visualization App Link

**Live App → https://i66-congestion-explorer.streamlit.app/**
---

## Repository Structure

```
i66-congestion-predictability/
│
├── notebooks/
│   ├── 1_ingestion/
│   │   └── toll_data_download.ipynb         # SmarterRoads API toll data downloader
│   │
│   ├── 2_silver_build/
│   │   ├── 01_process_ritis_speed_tt.ipynb  # RITIS/INRIX probe data → silver parquet
│   │   └── 02_toll_silver_table.ipynb       # Toll raw XML → 5-min aligned silver table
│   │
│   ├── 3_gold_builder/
│   │   └── phase1_gold_table_builder.ipynb  # Silver TTI → gold feature table (lags, rolling stats, calendar)
│   │
│   ├── 4_eda/
│   │   └── project1_tti_endogenous_eda.ipynb  # Full EDA: TTI distributions, autocorrelation, regime analysis
│   │
│   └── 5_modelling/
│       ├── 01_multi_horizon_models.ipynb         # Per-TMC models at 5/15/30-min horizons
│       ├── 02_pooled_spatial_generalization.ipynb # Pooled cross-TMC generalization
│       ├── 03_loto_spatial_generalization.ipynb   # Leave-one-TMC-out evaluation
│       ├── 04_predictability_ceiling_analysis.ipynb # Ceiling: volatility vs. error regression
│       ├── 05_xgboost_hyperparameter_tuning.ipynb  # Hyperparameter search (robustness check)
│       └── 06_figures_multi_horizon.ipynb          # Figure generation for paper
│
├── outputs/
│   ├── figures/          # All EDA and model output figures (PNG)
│   ├── tables/           # EDA summary tables (CSV)
│   └── model_results/
│       ├── *.csv                           # Horizon model results (overall, per-TMC, per-year)
│       ├── hyperparameter_tuning/          # XGBoost tuning grid and best params
│       ├── loto/                           # Leave-one-TMC-out results
│       ├── pooled/                         # Pooled model results
│       └── predictability_ceiling/         # Ceiling regression results
│
├── requirements.txt
└── README.md
```

---

## Pipeline Overview

The pipeline follows a **medallion architecture** (raw → silver → gold → model):

```
Raw Data Sources
  (RITIS probe data, SmarterRoads toll API, ASOS weather, VDOT crashes)
       │
       ▼
1_ingestion       → Download raw data (API calls, file downloads)
       │
       ▼
2_silver_build    → Clean, align to 5-min UTC spine, write parquet
       │
       ▼
3_gold_builder    → Join silver tables, engineer lag/rolling/calendar features
       │
       ▼
4_eda             → Exploratory analysis, autocorrelation, regime characterization
       │
       ▼
5_modelling       → Train/val/test split (year-based), model training, evaluation
```

**Train/val/test split:** 2022 train, 2023 val, 2024–2025 test. No random shuffling. Splits are time-based to prevent leakage.

---

## Key Results

| Horizon | Model | Test MAE | vs. Persistence |
|---------|-------|----------|-----------------|
| 5 min   | XGBoost | — | see `outputs/model_results/` |
| 15 min  | XGBoost | — | see `outputs/model_results/` |
| 30 min  | XGBoost | — | see `outputs/model_results/` |

Full numeric results are in `outputs/model_results/paper_summary_table.csv`. Figures are in `outputs/figures/`.

---

## Data Sources

This study uses the following data sources, none of which are included in this repository:

| Source | Description | Access |
|--------|-------------|--------|
| RITIS / INRIX NPMRDS | Probe-based speed and travel time at 5-min resolution, TMC-level | [RITIS](https://ritis.org) (institutional subscription) |
| SmarterRoads API | Dynamic toll prices on I-66 ITB at 5-min cadence | [511-ATIS](https://data.511-atis-ttrip-prod.iteriscloud.com/smarterRoads) (token required — set `SMARTERROADS_TOKEN` env var) |
| Iowa State ASOS | Airport weather observations (temperature, precipitation, visibility) | [Iowa State ASOS](https://mesonet.agron.iastate.edu/ASOS/) (public) |
| VDOT Crash Records | Incident locations and timestamps on I-66 | VDOT Open Data |

To reproduce the pipeline, obtain access to these sources and configure the path constants in each notebook's `CONFIG` section.

---

## Setup

```bash
pip install -r requirements.txt
```

For the toll data downloader, set your API token as an environment variable:

```bash
# Linux / macOS
export SMARTERROADS_TOKEN="your_token_here"

# Windows PowerShell
$env:SMARTERROADS_TOKEN = "your_token_here"
```

---

## Citation

This paper is currently under review. Citation details will be added upon acceptance.

---

## License

Code in this repository is released under the MIT License. Output figures and tables are associated with the paper under review and should not be reproduced without permission.
