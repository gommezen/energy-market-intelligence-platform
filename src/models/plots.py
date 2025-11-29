"""
Plot utilities for forecasting diagnostics.

Provides:
- plot_residuals(): residual distribution, scatter, and time series
- plot_forecast(): true vs predicted time-series comparison

All functions return figure objects to allow saving or embedding in reports.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
import numpy as np


# ------------------------------------------------------------
# 1. Residual Diagnostics
# ------------------------------------------------------------
def plot_residuals(y_true: pd.Series, y_pred: np.ndarray):
    """
    Plot residual distribution, residual vs predicted, and
    residual time-series.

    Parameters
    ----------
    y_true : pd.Series
        Ground truth values (must be indexed).
    y_pred : array-like
        Model predictions aligned with y_true.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The full residual diagnostics figure.
    axes : np.ndarray
        Array of matplotlib Axes objects.
    """

    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have equal length.")

    # Convert residuals to DataFrame for seaborn type safety
    residuals = pd.Series((y_true - y_pred).values, index=y_true.index, name="residuals")
    pred_series = pd.Series(y_pred, index=y_true.index, name="predicted")

    fig, axes = plt.subplots(1, 3, figsize=(18, 4))

    # ------------------------------------------------------------
    # 1. Residual Distribution (Histplot)
    # ------------------------------------------------------------
    sns.histplot(
        data=residuals.to_frame(),      # dataframe form
        x="residuals",
        kde=True,
        ax=axes[0]
    )
    axes[0].set_title("Residual Distribution")

    # ------------------------------------------------------------
    # 2. Residual vs Predicted
    # ------------------------------------------------------------
    sns.scatterplot(
        data=pd.concat([pred_series, residuals], axis=1),
        x="predicted",
        y="residuals",
        ax=axes[1]
    )
    axes[1].set_title("Residual vs Predicted")
    axes[1].axhline(0, color="red", linewidth=1)

    # ------------------------------------------------------------
    # 3. Residual Time Series
    # ------------------------------------------------------------
    sns.lineplot(
        data=residuals.to_frame(),
        x=residuals.index,
        y="residuals",
        ax=axes[2]
    )
    axes[2].set_title("Residual Time Series")
    axes[2].axhline(0, color="red", linewidth=1)

    plt.tight_layout()
    return fig, axes


# ------------------------------------------------------------
# 2. True vs Predicted (Plotly)
# ------------------------------------------------------------
def plot_forecast(y_true: pd.Series, y_pred: np.ndarray):
    """
    Plot true vs predicted series using Plotly.

    Parameters
    ----------
    y_true : pd.Series
        Ground truth.
    y_pred : array-like
        Predictions.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Interactive Plotly figure.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred lengths do not match.")

    fig = px.line(
        x=y_true.index,
        y=[y_true.values, y_pred],
        labels={"x": "Time", "value": "Congestion Income (EUR)"},
        title="True vs Predicted",
    )

    fig.update_layout(
        height=400,
        legend=dict(title="Series", itemsizing="constant"),
    )

    # Assign legend labels
    fig.data[0].name = "True"
    fig.data[1].name = "Predicted"

    return fig
