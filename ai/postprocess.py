from __future__ import annotations
import pandas as pd
from typing import List, Tuple

def apply_basic_ai_corrections(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    df = df.copy()
    notes: List[str] = []

    if "precip_mm" in df.columns:
        high_precip = df["precip_mm"] > 80
        if high_precip.any():
            df.loc[high_precip, "precip_mm"] = 80.0
            notes.append("Przycięto ekstremalne wartości opadu do 80 mm.")

    if "temperature_c" in df.columns:
        df["temperature_c"] = df["temperature_c"].rolling(window=3, min_periods=1, center=True).mean()
        notes.append("Wygładzono temperaturę ruchomym oknem (3h).")

    return df, notes
