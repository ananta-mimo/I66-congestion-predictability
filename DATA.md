# Data Guide

This document describes the data schema and directory layout expected by the pipeline. Raw data is not distributed with this repository.

---

## Expected Directory Layout

The notebooks expect data to live outside this repository in a sibling `Data/` directory. Set paths in each notebook's `CONFIG` section to match your local layout.

```
../Data/
├── a_raw_download/
│   ├── data_speed_tt/              # RITIS/INRIX ZIP exports (one per year)
│   └── i66_toll_trip_pricing_monthly/
│       ├── raw_xml/                # Raw SmarterRoads XML archives
│       ├── csv_monthly/            # Monthly CSV outputs
│       └── parquet_monthly/        # Monthly parquet outputs
│
├── b_processed_data/
│   └── ritis_speed_tt_5min/        # Silver TTI parquet files (one per year)
│       ├── I-66_Research_Speed_TT_2022_silver.parquet
│       ├── I-66_Research_Speed_TT_2023_silver.parquet
│       ├── I-66_Research_Speed_TT_2024_silver.parquet
│       └── I-66_Research_Speed_TT_2025_silver.parquet
│
└── c_final_tables/
    └── baseline_model_gold_table/  # Gold feature tables (combined + year-specific)
        ├── I66_phase1_TTI_features_2022_2025_combined.parquet
        └── I66_phase1_TTI_features_<year>.parquet
```

---

## Silver Table Schema

Each silver parquet file (per year) has the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `tmc` | string | TMC identifier (41 segments, EB + WB) |
| `ts_utc` | datetime[UTC] | 5-minute timestamp in UTC |
| `ts_local` | datetime | Timestamp in US/Eastern |
| `tti` | float | Travel Time Index (ratio of travel time to free-flow) |
| `confidence` | int | INRIX confidence score (0–100) |
| `road` | string | Road name |
| `miles` | float | Segment length in miles |
| `direction` | string | EB or WB |

---

## Gold Table Schema

The gold table extends the silver table with engineered features:

| Column group | Description |
|---|---|
| `tti_lag_1` ... `tti_lag_12` | TTI lags at 5-min intervals (1 lag = 5 min back) |
| `tti_rolling_mean_6`, `_12` | Rolling mean over 30-min and 60-min windows |
| `tti_rolling_standard_deviation_6`, `_12` | Rolling std over 30-min and 60-min windows |
| `tti_change_1_step` | First difference of TTI (lag_1 minus lag_2) |
| `tti_absolute_change_1_step` | Absolute value of first difference |
| `sin_hour`, `cos_hour` | Cyclical hour-of-day encoding |
| `sin_day_of_week`, `cos_day_of_week` | Cyclical day-of-week encoding |
| `sin_month`, `cos_month` | Cyclical month encoding |
| `is_weekend_flag` | 1 if Saturday or Sunday |
| `target_tti_5min_ahead` | Prediction target at +5 min |
| `target_tti_15min_ahead` | Prediction target at +15 min |
| `target_tti_30min_ahead` | Prediction target at +30 min |

---

## Train / Val / Test Split

Splits are time-based. No random shuffling is applied.

| Split | Years |
|-------|-------|
| Train | 2022 |
| Validation | 2023 |
| Test | 2024–2025 |

---

## Corridor Description

I-66 Inside the Beltway (ITB) is a managed lane corridor in Northern Virginia with an asymmetric tolling structure:

- **Eastbound (EB):** Tolled during AM peak (5:30–9:30 AM weekdays)
- **Westbound (WB):** Tolled during PM peak (3:00–7:00 PM weekdays)

The corridor spans approximately 10 miles and is covered by 41 TMC segments.
