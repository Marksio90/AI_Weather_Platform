from __future__ import annotations
from typing import Any
import streamlit as st
from core.i18n import t


def render_header(lang: str = "pl") -> None:
    title = t("app_title", lang)
    subtitle = (
        "Globalna, wieloźródłowa prognoza z modułami AI (GraphCast / nowcasting) i TTS."
        if lang == "pl"
        else "Global, multi-source weather with AI modules (GraphCast / nowcasting) and TTS."
    )

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            padding: 1.5rem 1.8rem;
            border-radius: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(148, 163, 184, 0.25);
            display: flex;
            justify-content: space-between;
            gap: 1rem;
        ">
            <div>
                <h1 style="margin:0; font-size: 1.8rem;">{title}</h1>
                <p style="margin-top: .5rem; color: #cbd5f5;">
                    {subtitle}
                </p>
            </div>
            <div style="text-align: right; font-size: .7rem; color: rgba(203, 213, 225, 0.65);">
                <div>Engine: AI + NWP blend</div>
                <div>Latency: near real-time</div>
                <div>Mode: demo</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_location_search(lang: str = "pl") -> str:
    st.subheader("🌐 " + ("Lokalizacja" if lang == "pl" else "Location"))
    return st.text_input(
        t("location_label", lang),
        value="Warszawa" if lang == "pl" else "Warsaw",
    )


def render_coords_inputs(default_lat: float, default_lon: float, lang: str = "pl") -> tuple[float, float]:
    label_lat = "Szerokość geograficzna (lat)" if lang == "pl" else "Latitude"
    label_lon = "Długość geograficzna (lon)" if lang == "pl" else "Longitude"
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input(label_lat, value=default_lat, format="%.4f")
    with col2:
        lon = st.number_input(label_lon, value=default_lon, format="%.4f")
    return lat, lon


def render_forecast_charts(df: Any, lang: str = "pl") -> None:
    """
    Rysuje podstawowe wykresy, ale bez wywalania się jeśli brakuje kolumn.
    """
    st.subheader("📈 " + t("forecast_header", lang))

    if df is None or getattr(df, "empty", True):
        st.info("Brak danych do wykresu.")
        return

    # temperatura
    if "temperature_c" in df.columns:
        st.line_chart(
            df[["temperature_c"]].rename(columns={"temperature_c": t("temperature", lang)})
        )
    else:
        st.warning("Brak kolumny temperatury – pomijam wykres temperatury.")

    # opad
    if "precip_mm" in df.columns:
        st.bar_chart(
            df[["precip_mm"]].rename(columns={"precip_mm": t("precipitation", lang)})
        )
    else:
        st.warning("Brak kolumny opadu – pomijam wykres opadów.")
