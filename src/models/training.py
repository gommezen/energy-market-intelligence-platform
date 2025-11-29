from sklearn.ensemble import RandomForestRegressor
import numpy as np

def train_random_forest(X_train, y_train):
    """
    Train a stable random-forest model with predefined settings.
    """
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model
