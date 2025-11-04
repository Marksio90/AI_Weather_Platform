from __future__ import annotations
from typing import Tuple, List
import pandas as pd

def apply_model_slot(
    df: pd.DataFrame,
    slot_name: str,
    lat: float,
    lon: float,
) -> Tuple[pd.DataFrame, List[str]]:
    """
    slot_name:
      - "none" – nic nie robimy
      - "mock-graphcast" – udajemy, że model poprawił opad i temperaturę
      - "mock-downscaler" – udajemy, że podbiliśmy rozdzielczość i lekko skorygowaliśmy temperaturę
    Zwracamy: (df_po_modelu, notatki)
    """
    df = df.copy()
    notes: List[str] = []

    if slot_name == "none":
        return df, notes

    if slot_name == "mock-graphcast":
        # lekkie obniżenie opadów i wygładzenie temperatury
        if "precip_mm" in df.columns:
            df["precip_mm"] = df["precip_mm"] * 0.9
        if "temperature_c" in df.columns:
            df["temperature_c"] = df["temperature_c"].rolling(window=2, min_periods=1).mean()
        notes.append("Zastosowano model slot: mock-graphcast (symulacja poprawy pola opadów i temperatury).")
        return df, notes

    if slot_name == "mock-downscaler":
        # dodajmy małą korektę terenową zależną od szerokości geogr. (symulacja)
        correction = (abs(lat) % 5) * 0.1
        if "temperature_c" in df.columns:
            df["temperature_c"] = df["temperature_c"] - correction
        notes.append(f"Zastosowano model slot: mock-downscaler (lokalna korekta temperatury o {correction:.2f} °C).")
        return df, notes

    # nieznany slot
    notes.append("Nieznany slot modelu – dane bez zmian.")
    return df, notes
