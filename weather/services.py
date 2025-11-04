from __future__ import annotations
from typing import Optional
import pandas as pd

from ingestion.open_meteo_client import fetch_hourly_forecast

SUPPORTED_SOURCES = ["open-meteo"]

def get_hourly_dataframe(
    lat: float,
    lon: float,
    timezone: str = "auto",
    days: int = 7,
    source: str = "open-meteo",
) -> Optional[pd.DataFrame]:
    if source == "open-meteo":
        data = fetch_hourly_forecast(lat=lat, lon=lon, timezone=timezone, forecast_days=days)
    else:
        return None

    if not data or "hourly" not in data:
        return None

    hourly = data["hourly"]
    df = pd.DataFrame({
        "time": pd.to_datetime(hourly["time"]),
        "temperature_c": hourly.get("temperature_2m"),
        "precip_mm": hourly.get("precipitation"),
    })
    df.set_index("time", inplace=True)
    return df
