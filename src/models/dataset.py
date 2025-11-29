from pathlib import Path
import pandas as pd

def load_feature_dataset(path):
    """
    Load engineered feature dataset (parquet) and validate structure.
    Accepts both str and Path inputs.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Feature file missing: {path}")

    df = pd.read_parquet(path)

    # --- Required structure checks ---
    if "RevenueEUR" not in df.columns:
        raise ValueError("Dataset missing required column 'RevenueEUR'.")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("Index must be a DatetimeIndex.")

    df = df.sort_index()

    return df


def build_supervised(df, horizon=1):
    """
    Turn a time-series into supervised learning format.

    Parameters
    ----------
    df : DataFrame
        Must contain 'RevenueEUR'
    horizon : int
        Steps ahead (1 step = 15 min)

    Returns
    -------
    DataFrame with new 'target' column.
    """
    if horizon < 1:
        raise ValueError("Horizon must be >= 1")

    if "RevenueEUR" not in df.columns:
        raise ValueError("Missing 'RevenueEUR' in dataset")

    df = df.copy()
    df["target"] = df["RevenueEUR"].shift(-horizon)

    # drop last incomplete rows
    df = df.dropna(subset=["target"])

    return df


def time_split(df, target="target", ratio=0.8):
    """
    Split a time-indexed DataFrame into train/test sets
    without shuffling and with clean separation.

    Parameters
    ----------
    df : pd.DataFrame
        Supervised dataset with features + target column.
    target : str
        Name of the target column.
    ratio : float
        Fraction used for training.

    Returns
    -------
    X_train, X_test, y_train, y_test : tuple of pd.DataFrame / pd.Series
    """

    if target not in df.columns:
        raise KeyError(f"Target column '{target}' not found in dataframe.")

    if not df.index.is_monotonic_increasing:
        df = df.sort_index()

    split_idx = int(len(df) * ratio)

    train = df.iloc[:split_idx].copy()
    test  = df.iloc[split_idx:].copy()

    X_train = train.drop(columns=[target])
    y_train = train[target]

    X_test = test.drop(columns=[target])
    y_test = test[target]

    return X_train, X_test, y_train, y_test
