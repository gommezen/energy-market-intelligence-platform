import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ------------------------------------------------------------
# Error metrics
# ------------------------------------------------------------
def rmse(y_true, y_pred):
    """Root Mean Square Error."""
    return np.sqrt(mean_squared_error(y_true, y_pred))


def mape(y_true, y_pred):
    """
    Mean Absolute Percentage Error.
    Uses epsilon to avoid division by zero.
    """
    eps = 1e-8
    return np.mean(np.abs((y_true - y_pred) / (y_true + eps))) * 100


def mase(y_true, y_pred, insample):
    """
    Mean Absolute Scaled Error.
    insample is the training series used for naive scaling.
    """
    naive_scale = np.mean(np.abs(insample.diff().dropna()))
    return np.mean(np.abs(y_true - y_pred)) / naive_scale


# ------------------------------------------------------------
# Unified evaluation function
# ------------------------------------------------------------
def evaluate(y_true, y_pred, training_series, name="Model"):
    """
    Compute all standard forecast metrics.

    Parameters
    ----------
    y_true : pd.Series
        Ground-truth values.

    y_pred : pd.Series or np.ndarray
        Predicted values.

    training_series : pd.Series
        The series used for MASE scaling (typically y_train).

    name : str
        Name of the model (for logging).

    Returns
    -------
    dict
        MAE, RMSE, MAPE, MASE
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse_val = rmse(y_true, y_pred)
    mape_val = mape(y_true, y_pred)
    mase_val = mase(y_true, y_pred, training_series)

    return {
        "MAE": mae,
        "RMSE": rmse_val,
        "MAPE": mape_val,
        "MASE": mase_val,
    }
