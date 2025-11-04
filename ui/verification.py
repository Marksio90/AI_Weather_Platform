from __future__ import annotations
import streamlit as st
import pandas as pd

from weather.verification import verify_forecast_vs_actuals
from core.storage import save_verification_result


REQUIRED_COLS = {"time", "temperature_c", "precip_mm"}


def render_verification_panel(forecast_df: pd.DataFrame) -> None:
    st.subheader("🛠️ Walidacja prognozy")

    st.write(
        "Wgraj CSV z rzeczywistymi obserwacjami w formacie: "
        "`time, temperature_c, precip_mm`.\n"
        "Kolumna `time` powinna być w formacie ISO (np. 2025-11-04 12:00)."
    )

    uploaded = st.file_uploader("Wgraj CSV z obserwacjami", type=["csv"])

    if uploaded is None:
        st.info("Nie wgrano pliku – brak walidacji.")
        return

    # wczytaj jako DataFrame
    try:
        actuals_df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"Nie udało się wczytać CSV: {exc}")
        return

    # pokaż userowi, co wgrał
    st.caption("Podgląd wgranych danych:")
    st.dataframe(actuals_df.head(30), use_container_width=True)

    # sprawdź kolumny
    missing = REQUIRED_COLS.difference(actuals_df.columns)
    if missing:
        st.error(f"Brakuje kolumn: {', '.join(missing)}. Uzupełnij plik i wgraj ponownie.")
        return

    # licz metryki
    metrics = verify_forecast_vs_actuals(forecast_df, actuals_df)

    st.success("Metryki policzone:")
    st.json(metrics)

    # zapisz wynik do storage – w JSON
    save_path = save_verification_result(metrics, as_json=True, filename_prefix="verification")
    st.caption(f"Wynik zapisany do: {save_path}")

    # ładniejsza interpretacja
    n_samples = metrics.get("n_samples", 0)
    if n_samples == 0:
        st.warning("Uwaga: brak wspólnych timestampów między prognozą a obserwacjami – metryki mogą być puste.")
    else:
        st.info(f"Porównano {n_samples} rekordów prognozy z obserwacjami.")
