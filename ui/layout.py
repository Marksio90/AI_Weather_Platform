from __future__ import annotations
import streamlit as st
from core.i18n import t

def render_header(lang: str = "pl") -> None:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
                    padding: 1.5rem 1.8rem; border-radius: 1.5rem; margin-bottom: 1.5rem;
                    border: 1px solid rgba(148, 163, 184, 0.25);">
            <h1 style="margin:0; font-size: 1.8rem;">🌍 AI Prognoza Pogody</h1>
            <p style="margin-top: .5rem; color: #cbd5f5;">
                Globalna, wieloźródłowa prognoza, gotowa na AI (GraphCast / nowcasting) i głos.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_location_search(lang: str = "pl"):
    st.subheader("🌐 Lokalizacja")
    return st.text_input(
        "Wpisz nazwę miasta / Enter city name",
        value="Warszawa" if lang == "pl" else "Warsaw",
    )

def render_coords_inputs(default_lat: float, default_lon: float, lang: str = "pl"):
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Szerokość geograficzna (lat)", value=default_lat, format="%.4f")
    with col2:
        lon = st.number_input("Długość geograficzna (lon)", value=default_lon, format="%.4f")
    return lat, lon

def render_forecast_charts(df, lang: str = "pl"):
    st.subheader("📈 " + t("forecast_header", lang))
    st.line_chart(df[["temperature_c"]].rename(columns={"temperature_c": t("temperature", lang)}))
    st.bar_chart(df[["precip_mm"]].rename(columns={"precip_mm": t("precipitation", lang)}))
