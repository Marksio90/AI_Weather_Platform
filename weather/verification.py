from __future__ import annotations
from typing import Dict
import pandas as pd
import numpy as np

def verify_forecast_vs_actuals(
    forecast_df: pd.DataFrame,
    actuals_df: pd.DataFrame,
) -> Dict[str, float]:
    actuals_df = actuals_df.copy()
    actuals_df["time"] = pd.to_datetime(actuals_df["time"])
    actuals_df.set_index("time", inplace=True)

    joined = forecast_df.join(actuals_df, lsuffix="_forecast", rsuffix="_actual", how="inner")
    metrics: Dict[str, float] = {}

    def mae(a, b):
        return float(np.mean(np.abs(a - b))) if len(a) else float("nan")

    def rmse(a, b):
        return float(np.sqrt(np.mean((a - b) ** 2))) if len(a) else float("nan")

    if "temperature_c_forecast" in joined.columns and "temperature_c_actual" in joined.columns:
        f = joined["temperature_c_forecast"]
        a = joined["temperature_c_actual"]
        metrics["temp_mae"] = mae(a, f)
        metrics["temp_rmse"] = rmse(a, f)

    if "precip_mm_forecast" in joined.columns and "precip_mm_actual" in joined.columns:
        f = joined["precip_mm_forecast"]
        a = joined["precip_mm_actual"]
        metrics["precip_mae"] = mae(a, f)
        metrics["precip_rmse"] = rmse(a, f)

    metrics["n_samples"] = int(len(joined))
    return metrics
