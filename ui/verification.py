from __future__ import annotations
import streamlit as st
import pandas as pd
from weather.verification import verify_forecast_vs_actuals
from core.storage import save_verification_result

def render_verification_panel(forecast_df: pd.DataFrame) -> None:
    st.subheader("🛠️ Walidacja prognozy")
    st.write("Wgraj CSV z rzeczywistymi obserwacjami (time, temperature_c, precip_mm).")

    uploaded = st.file_uploader("Wgraj CSV", type=["csv"])
    if uploaded is not None:
        actuals_df = pd.read_csv(uploaded)
        metrics = verify_forecast_vs_actuals(forecast_df, actuals_df)
        st.success("Metryki policzone:")
        st.json(metrics)
        save_path = save_verification_result(metrics)
        st.caption(f"Wynik zapisany do: {save_path}")
    else:
        st.info("Nie wgrano pliku – brak walidacji.")
