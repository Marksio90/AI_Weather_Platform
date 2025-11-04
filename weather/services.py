from __future__ import annotations
from typing import Optional, Dict, Callable, Any
import logging

import pandas as pd

from ingestion.open_meteo_client import fetch_hourly_forecast

logger = logging.getLogger(__name__)

# tu rejestrujemy wszystkie źródła, z których umiemy pobrać dane
SUPPORTED_SOURCES = ["open-meteo"]
# w przyszłości: ["open-meteo", "ecmwf-proxy", "noaa-gfs"]


def _df_from_open_meteo(data: dict) -> Optional[pd.DataFrame]:
    """
    Zamienia surowy JSON Open-Meteo na nasz standardowy DataFrame.
    """
    if not data or "hourly" not in data:
        return None

    hourly = data["hourly"]
    times = hourly.get("time")
    if not times:
        return None

    df = pd.DataFrame({"time": pd.to_datetime(times)})

    # mapowanie pól open-meteo -> nasze pola
    if "temperature_2m" in hourly:
        df["temperature_c"] = hourly["temperature_2m"]
    else:
        df["temperature_c"] = None

    if "precipitation" in hourly:
        df["precip_mm"] = hourly["precipitation"]
    else:
        df["precip_mm"] = 0.0

    # możesz tu dopisać:
    # if "relative_humidity_2m" in hourly: df["humidity"] = hourly["relative_humidity_2m"]

    df.set_index("time", inplace=True)
    # sort na wszelki wypadek
    df.sort_index(inplace=True)

    return df


def get_hourly_dataframe(
    lat: float,
    lon: float,
    *,
    timezone: str = "auto",
    days: int = 7,
    source: str = "open-meteo",
) -> Optional[pd.DataFrame]:
    """
    Główny punkt wejścia: pobiera godzinową prognozę z wybranego źródła
    i zwraca ją w naszym ujednoliconym formacie.

    Zwraca:
        DataFrame z indexem czasowym i kolumnami:
            - temperature_c
            - precip_mm
        albo None, jeśli nie udało się pobrać/przetworzyć.
    """
    source = (source or "").lower()

    if source == "open-meteo":
        data = fetch_hourly_forecast(
            lat=lat,
            lon=lon,
            timezone=timezone,
            forecast_days=days,
            # tu można dopisać więcej pól
            hourly=("temperature_2m", "precipitation"),
        )
        df = _df_from_open_meteo(data)
    else:
        logger.warning("Źródło %r nie jest wspierane. Dostępne: %s", source, SUPPORTED_SOURCES)
        return None

    if df is None or df.empty:
        logger.warning("Brak danych pogodowych dla lat=%s lon=%s ze źródła %s", lat, lon, source)
        return None

    return df
