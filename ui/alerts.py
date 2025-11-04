from __future__ import annotations
import streamlit as st
import pandas as pd
from typing import List, Dict, Any


# możesz to potem wynieść do configa
ALERT_THRESHOLDS = {
    "rain_mm": 20.0,
    "very_cold_c": -10.0,
    "very_hot_c": 35.0,
}


def _translate(key: str, lang: str) -> str:
    # mini i18n na potrzeby alertów
    STR = {
        "pl": {
            "header": "⚠️ Alerty pogodowe",
            "rain": "Silne opady w najbliższych godzinach (>= {mm} mm).",
            "cold": "Bardzo niska temperatura (poniżej {c} °C).",
            "hot": "Bardzo wysoka temperatura (powyżej {c} °C).",
        },
        "en": {
            "header": "⚠️ Weather alerts",
            "rain": "Heavy rainfall expected in the next hours (>= {mm} mm).",
            "cold": "Very low temperature expected (below {c} °C).",
            "hot": "Very high temperature expected (above {c} °C).",
        },
    }
    return STR.get(lang, STR["en"]).get(key, key)


def render_alerts(df: pd.DataFrame, lang: str = "pl") -> None:
    # brak danych → brak alertów
    if df is None or df.empty:
        return

    alerts: List[str] = []

    # opady
    if "precip_mm" in df.columns:
        high_rain = df["precip_mm"] >= ALERT_THRESHOLDS["rain_mm"]
        if high_rain.any():
            alerts.append(
                _translate("rain", lang).format(mm=ALERT_THRESHOLDS["rain_mm"])
            )

    # bardzo zimno
    if "temperature_c" in df.columns:
        very_cold = df["temperature_c"] <= ALERT_THRESHOLDS["very_cold_c"]
        if very_cold.any():
            alerts.append(
                _translate("cold", lang).format(c=ALERT_THRESHOLDS["very_cold_c"])
            )

        # bardzo gorąco
        very_hot = df["temperature_c"] >= ALERT_THRESHOLDS["very_hot_c"]
        if very_hot.any():
            alerts.append(
                _translate("hot", lang).format(c=ALERT_THRESHOLDS["very_hot_c"])
            )

    if not alerts:
        return

    st.subheader(_translate("header", lang))
    # możesz dodać sortowanie po ważności – na razie kolejność jak wykryto
    for msg in alerts:
        st.warning(msg)
