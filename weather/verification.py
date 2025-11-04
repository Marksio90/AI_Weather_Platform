from __future__ import annotations
from typing import Dict, Optional
import pandas as pd
import numpy as np


def _safe_corr(a: pd.Series, b: pd.Series) -> float:
    # korelacja może się wywalić przy małej liczbie próbek
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    try:
        return float(a.corr(b))
    except Exception:
        return float("nan")


def verify_forecast_vs_actuals(
    forecast_df: pd.DataFrame,
    actuals_df: pd.DataFrame,
    *,
    time_tolerance: Optional[str] = None,
) -> Dict[str, float]:
    """
    Porównuje prognozę z obserwacjami i zwraca zestaw metryk.
    Zakłada standardowe nazwy kolumn:
      - w forecast_df: temperature_c, precip_mm
      - w actuals_df: time, temperature_c, precip_mm

    Args:
        forecast_df: DataFrame z prognozą (indeks czasowy)
        actuals_df: DataFrame z obserwacjami (kolumna 'time')
        time_tolerance: np. '5min' – wtedy próbuje dopasować czasy z tolerancją
                        (przydatne gdy obserwacje są o 10:05 a prognoza o 10:00)

    Returns:
        dict z metrykami (można spokojnie serializować do JSON).
    """
    # --- przygotowanie obserwacji ---
    actuals_df = actuals_df.copy()
    actuals_df["time"] = pd.to_datetime(actuals_df["time"])
    actuals_df.set_index("time", inplace=True)
    actuals_df.sort_index(inplace=True)

    forecast_df = forecast_df.copy()
    forecast_df.sort_index(inplace=True)

    # --- dopasowanie czasów ---
    if time_tolerance:
        # resample obserwacji do tego samego kroku co prognoza (przybliżenie)
        # np. jeśli prognoza jest co godzinę, a time_tolerance="10min", to weźmiemy najbliższy punkt
        actuals_aligned = actuals_df.reindex(
            forecast_df.index,
            method="nearest",
            tolerance=time_tolerance,
        )
        joined = forecast_df.join(
            actuals_aligned,
            lsuffix="_forecast",
            rsuffix="_actual",
            how="inner",
        )
    else:
        # klasyczne łączenie po dokładnym timestampie
        joined = forecast_df.join(
            actuals_df,
            lsuffix="_forecast",
            rsuffix="_actual",
            how="inner",
        )

    metrics: Dict[str, float] = {}
    n_all = int(len(joined))
    metrics["n_samples"] = n_all

    if n_all == 0:
        # nic się nie zgrało – zwracamy tylko info
        return metrics

    # helpery
    def mae(a: pd.Series, b: pd.Series) -> float:
        return float(np.mean(np.abs(a - b))) if len(a) else float("nan")

    def rmse(a: pd.Series, b: pd.Series) -> float:
        return float(np.sqrt(np.mean((a - b) ** 2))) if len(a) else float("nan")

    def bias(a: pd.Series, b: pd.Series) -> float:
        # średni błąd: prognoza - obserwacja
        return float(np.mean(b - a)) if len(a) else float("nan")

    # --- temperatura ---
    if "temperature_c_forecast" in joined.columns and "temperature_c_actual" in joined.columns:
        f = joined["temperature_c_forecast"]
        a = joined["temperature_c_actual"]
        valid_mask = a.notna() & f.notna()
        f = f[valid_mask]
        a = a[valid_mask]

        metrics["temp_n"] = int(len(a))
        metrics["temp_mae"] = mae(a, f)
        metrics["temp_rmse"] = rmse(a, f)
        metrics["temp_bias"] = bias(a, f)
        metrics["temp_corr"] = _safe_corr(a, f)

    # --- opad ---
    if "precip_mm_forecast" in joined.columns and "precip_mm_actual" in joined.columns:
        f = joined["precip_mm_forecast"]
        a = joined["precip_mm_actual"]
        valid_mask = a.notna() & f.notna()
        f = f[valid_mask]
        a = a[valid_mask]

        metrics["precip_n"] = int(len(a))
        metrics["precip_mae"] = mae(a, f)
        metrics["precip_rmse"] = rmse(a, f)
        metrics["precip_bias"] = bias(a, f)
        metrics["precip_corr"] = _safe_corr(a, f)

    return metrics
