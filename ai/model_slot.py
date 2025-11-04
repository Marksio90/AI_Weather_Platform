from __future__ import annotations
from typing import Callable, Dict, List, Tuple
import pandas as pd


# typ slotu: bierze df i zwraca df + listę notatek
ModelSlot = Callable[[pd.DataFrame, float, float], Tuple[pd.DataFrame, List[str]]]


def _ensure_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Upewnia się, że mamy kolumny używane w slotach.
    Nie tworzy sztucznych danych – tylko pilnuje, żeby nie wywaliło się na brak kolumny.
    """
    expected = {"temperature_c", "precip_mm"}
    missing = expected.difference(df.columns)
    if missing:
        # nie podnosimy wyjątku – slot może działać częściowo
        pass
    return df


def slot_none(df: pd.DataFrame, lat: float, lon: float) -> Tuple[pd.DataFrame, List[str]]:
    return df, []


def slot_mock_graphcast(df: pd.DataFrame, lat: float, lon: float) -> Tuple[pd.DataFrame, List[str]]:
    """
    Udajemy, że GraphCast:
    - delikatnie redukujemy opad,
    - lekko wygładzamy temperaturę.
    """
    notes: List[str] = ["slot=mock-graphcast: symulacja poprawy pola opadów i temperatury."]
    df = df.copy()

    if "precip_mm" in df.columns:
        df["precip_mm"] = (df["precip_mm"] * 0.9).round(2)

    if "temperature_c" in df.columns:
        df["temperature_c"] = (
            df["temperature_c"]
            .rolling(window=2, min_periods=1)
            .mean()
            .round(2)
        )

    return df, notes


def slot_mock_downscaler(df: pd.DataFrame, lat: float, lon: float) -> Tuple[pd.DataFrame, List[str]]:
    """
    Udajemy lokalny downscaler – np. poprawka terenowa zależna od szerokości.
    """
    df = df.copy()
    correction = (abs(lat) % 5) * 0.1  # 0.0–0.5°C
    notes = [f"slot=mock-downscaler: lokalna korekta temperatury o {correction:.2f} °C (lat={lat:.2f})."]

    if "temperature_c" in df.columns:
        df["temperature_c"] = (df["temperature_c"] - correction).round(2)

    return df, notes


# rejestr slotów – tu dodajesz kolejne, np. "real-graphcast": slot_real_graphcast
SLOTS: Dict[str, ModelSlot] = {
    "none": slot_none,
    "mock-graphcast": slot_mock_graphcast,
    "mock-downscaler": slot_mock_downscaler,
}


def apply_model_slot(
    df: pd.DataFrame,
    slot_name: str,
    lat: float,
    lon: float,
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Główny punkt wejścia dla warstwy AI-slotów.
    Przyjmuje surowy dataframe prognozy i próbuje przepuścić go przez wybrany slot.
    Zawsze zwraca (df, notatki) – nawet dla nieznanego slotu.
    """
    df = _ensure_weather_columns(df)
    slot = SLOTS.get(slot_name)

    if slot is None:
        # slot nieznany – zwracamy oryginał i krótką notatkę
        return df, [f"slot={slot_name}: nieznany slot modelu – dane bez zmian."]

    return slot(df, lat, lon)
