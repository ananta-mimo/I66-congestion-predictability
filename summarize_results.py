"""
summarize_results.py
--------------------
Quick CLI summary of model evaluation results.
Prints a formatted table of test MAE and RMSE
across all models and forecast horizons.

Usage:
    python summarize_results.py
    python summarize_results.py --metric mae
    python summarize_results.py --metric rmse
    python summarize_results.py --horizon 5min
"""

import argparse
import pandas as pd
from pathlib import Path

RESULTS_PATH = Path("outputs/model_results/overall_horizon_model_results.csv")
HORIZONS     = ["5min", "15min", "30min"]
MODELS       = ["Persistence", "LinearRegression", "RandomForest", "XGBoost"]


def load_results(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Results file not found: {path}")
    return pd.read_csv(path)


def print_summary(df: pd.DataFrame, metric: str, horizon: str | None) -> None:
    col = f"test_{metric}"
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found. Choose 'mae' or 'rmse'.")

    if horizon:
        df = df[df["horizon"] == horizon]
        if df.empty:
            raise ValueError(f"No results for horizon '{horizon}'. "
                             f"Choose from: {HORIZONS}")

    pivot = (
        df[df["model"].isin(MODELS)]
        .pivot(index="model", columns="horizon", values=col)
        .reindex(index=MODELS, columns=HORIZONS)
        .round(4)
    )

    print(f"\nTest {metric.upper()} by Model and Horizon")
    print("=" * 50)
    print(pivot.to_string())
    print()

    # Best model per horizon
    print("Best model per horizon:")
    for h in ([horizon] if horizon else HORIZONS):
        if h in pivot.columns:
            best = pivot[h].idxmin()
            val  = pivot[h].min()
            print(f"  {h:>6}  →  {best:<20} ({metric.upper()} = {val:.4f})")
    print()


def main() -> None:
    ap = argparse.ArgumentParser(description="Summarize I-66 model evaluation results.")
    ap.add_argument("--metric",  choices=["mae", "rmse"], default="mae",
                    help="Metric to display (default: mae)")
    ap.add_argument("--horizon", choices=HORIZONS, default=None,
                    help="Filter to a single horizon (default: all)")
    args = ap.parse_args()

    df = load_results(RESULTS_PATH)
    print_summary(df, args.metric, args.horizon)


if __name__ == "__main__":
    main()
