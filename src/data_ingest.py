import pandas as pd
import requests_cache
from entsoe import EntsoePandasClient
from src.config import ENTSOE_API_TOKEN, TIMEZONE, AREA

def fetch_day_ahead_prices(start: str, end: str, area: str = AREA) -> pd.Series:
    session = requests_cache.CachedSession('cache/entsoe_cache')
    client = EntsoePandasClient(api_key=ENTSOE_API_KEY, session=session)
    prices = client.query_day_ahead_prices(area, start=pd.Timestamp(start, tz=TIMEZONE), end=pd.Timestamp(end, tz=TIMEZONE))
    prices.name = 'DayAheadPrice'
    return prices
