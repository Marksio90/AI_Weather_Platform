from __future__ import annotations
from typing import List, Tuple, Optional, Dict, Any
import pandas as pd


def apply_basic_ai_corrections(
    df: pd.DataFrame,
    *,
    max_precip_mm: float = 80.0,
    temp_smooth_window: int = 3,
    enable_precip_clip: bool = True,
    enable_temp_smooth: bool = True,
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Bardzo lekki postprocessing AI:
    - przycina absurdalnie wysokie opady (np. błędy źródła),
    - wygładza ząbki temperatury ruchomym oknem,
    - zwraca listę notatek, które można pokazać w UI.

    Parametry są jawne, więc możesz je potem trzymać w configu/DB.
    """
    df = df.copy()
    notes: List[str] = []

    # --- 1. sanity check: czy mamy jakiekolwiek dane
    if df.empty:
        return df, ["Brak danych – pominięto postprocessing."]

    # --- 2. opad: clipping ekstremów
    if enable_precip_clip and "precip_mm" in df.columns:
        too_high_mask = df["precip_mm"] > max_precip_mm
        if too_high_mask.any():
            original_max = float(df.loc[too_high_mask, "precip_mm"].max())
            df.loc[too_high_mask, "precip_mm"] = max_precip_mm
            notes.append(
                f"Przycięto {too_high_mask.sum()} wartości opadu powyżej {max_precip_mm} mm "
                f"(oryginalne maksimum: {original_max:.1f} mm)."
            )

    # --- 3. temperatura: wygładzanie
    if enable_temp_smooth and "temperature_c" in df.columns:
        # zapamiętamy, czy na pewno było co wygładzić
        before_std = float(df["temperature_c"].std()) if len(df) > 1 else 0.0

        df["temperature_c"] = (
            df["temperature_c"]
            .rolling(window=temp_smooth_window, min_periods=1, center=True)
            .mean()
        )

        after_std = float(df["temperature_c"].std()) if len(df) > 1 else 0.0
        if after_std < before_std:
            notes.append(
                f"Wygładzono temperaturę oknem {temp_smooth_window}h "
                f"(odchylenie spadło z {before_std:.2f} do {after_std:.2f})."
            )
        else:
            # raczej nie powinno się zdarzyć, ale lepiej mieć info
            notes.append("Wykonano wygładzanie temperatury, ale nie wykryto spadku zmienności.")

    # --- 4. jeśli nic nie zrobiliśmy, powiedz to jasno
    if not notes:
        notes.append("Postprocessing AI nie wprowadził zmian (dane wyglądały OK).")

    return df, notes
