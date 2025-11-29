# src/models/diagnostics.py

import pandas as pd
import numpy as np


def compute_residuals(y_true: pd.Series, y_pred) -> pd.Series:
    """
    Compute residuals (y_true - y_pred) with alignment checks.

    Parameters
    ----------
    y_true : pd.Series
        Ground truth time series.
    y_pred : array-like or pd.Series
        Forecast values.

    Returns
    -------
    pd.Series
        Residual series aligned exactly with y_true.
    """

    # Convert prediction to aligned Series if needed
    if not isinstance(y_pred, pd.Series):
        try:
            y_pred = pd.Series(y_pred, index=y_true.index)
        except Exception as e:
            raise ValueError(
                "y_pred could not be converted to a Series with y_true index."
            ) from e

    # Validate index alignment
    if not y_pred.index.equals(y_true.index):
        raise ValueError(
            "Index mismatch: y_true and y_pred must share the same index for residuals."
        )

    return y_true - y_pred

