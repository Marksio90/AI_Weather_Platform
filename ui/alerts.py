from __future__ import annotations
import streamlit as st
import pandas as pd

def render_alerts(df: pd.DataFrame, lang: str = "pl") -> None:
    high_rain = df["precip_mm"] > 20
    very_cold = df["temperature_c"] < -10
    very_hot = df["temperature_c"] > 35

    alerts = []
    if high_rain.any():
        alerts.append("Silne opady w najbliższych godzinach (>= 20 mm).")
    if very_cold.any():
        alerts.append("Bardzo niska temperatura (poniżej -10 °C).")
    if very_hot.any():
        alerts.append("Bardzo wysoka temperatura (powyżej 35 °C).")

    if alerts:
        st.subheader("⚠️ Alerty pogodowe")
        for a in alerts:
            st.warning(a)
