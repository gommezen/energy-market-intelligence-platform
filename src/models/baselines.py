import pandas as pd
from typing import Dict, Tuple

from src.models.metrics import evaluate


# ---------------------------------------------------------------
# Baseline Forecast Methods
# ---------------------------------------------------------------

def naive(series: pd.Series) -> pd.Series:
    """
    One-step naive forecast.
    Predicts the next value as the previous observed value.
    """
    return series.shift(1)


def seasonal_naive(series: pd.Series, steps_per_day: int = 96) -> pd.Series:
    """
    Seasonal naive forecast for 15-minute data.
    Predicts the next value as the value at the same time yesterday.
    """
    return series.shift(steps_per_day)


def rolling_mean(series: pd.Series, window: int = 24) -> pd.Series:
    """
    Rolling mean forecast using the last `window` observations.
    """
    return series.rolling(window).mean()


# ---------------------------------------------------------------
# Consolidated Baseline Computation
# ---------------------------------------------------------------

def compute_baselines(
    df_super: pd.DataFrame,
    y_test: pd.Series,
    y_train: pd.Series
) -> Tuple[Dict[str, pd.Series], Dict[str, dict], pd.DataFrame]:
    """
    Compute baseline forecast series *and* aligned performance metrics.

    Returns:
        baseline_preds: Dict[str, Series]
            - Naive
            - Seasonal Naive
            - Rolling Mean

        baseline_metrics: Dict[str, dict]
            - Each entry contains {"MAE":..., "RMSE":..., "MAPE":..., "MASE":...}

        baseline_df: pd.DataFrame
            - Tidy DataFrame for quick display in the notebook
    """

    # --- 1) Full-series baseline forecasts ---
    naive_full = naive(df_super["target"])
    seasonal_full = seasonal_naive(df_super["target"])
    rolling_full = rolling_mean(df_super["target"])

    # --- 2) Align to test-set timestamps ---
    baseline_preds = {
        "Naive": naive_full.loc[y_test.index].rename("Naive"),
        "Seasonal Naive": seasonal_full.loc[y_test.index].rename("Seasonal Naive"),
        "Rolling Mean": rolling_full.loc[y_test.index].rename("Rolling Mean"),
    }

    # --- 3) Compute metrics for each baseline ---
    baseline_metrics = {}
    for name, pred in baseline_preds.items():
        baseline_metrics[name] = evaluate(
            y_true=y_test,
            y_pred=pred,
            training_series=y_train,
            name=name
        )

    # --- 4) Create a compact display-friendly DataFrame ---
    baseline_df = pd.DataFrame(baseline_metrics)

    return baseline_preds, baseline_metrics, baseline_df
