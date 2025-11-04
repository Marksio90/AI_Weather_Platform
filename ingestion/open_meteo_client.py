from __future__ import annotations
import logging
from typing import Any, Dict, Optional
import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_hourly_forecast(
    lat: float,
    lon: float,
    timezone: str = "auto",
    hourly: str = "temperature_2m,precipitation",
    forecast_days: int = 7,
) -> Optional[Dict[str, Any]]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": hourly,
        "forecast_days": forecast_days,
        "timezone": timezone,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        logger.exception("Error fetching data from Open-Meteo: %s", exc)
        return None
