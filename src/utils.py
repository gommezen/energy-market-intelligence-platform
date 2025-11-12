import pandas as pd
import matplotlib.pyplot as plt

def plot_series(series: pd.Series, title: str = "Time Series Plot"):
    series.plot(title=title, figsize=(12, 4))
    plt.xlabel("Date")
    plt.ylabel(series.name)
    plt.grid(True)
    plt.show()
