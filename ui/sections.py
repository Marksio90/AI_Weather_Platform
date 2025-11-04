from __future__ import annotations
import streamlit as st

def render_nowcasting_placeholder(lat: float, lon: float, lang: str = "pl") -> None:
    st.subheader("🌧️ Nowcasting / Radar (placeholder)")
    st.info(
        "Tutaj w kolejnych paczkach podepniemy obraz radarowy/satelitarny aktualizowany co 5–15 min.",
        icon="ℹ️",
    )
    st.write(f"Wybrana lokalizacja: lat={lat:.2f}, lon={lon:.2f}")

def render_ai_summary_card(df, ai_notes, lang: str = "pl", city_name: str | None = None) -> None:
    city_part = f"dla {city_name}" if city_name else ""
    st.markdown(
        f"""
        <div style="background: rgba(15, 118, 110, 0.12); border: 1px solid rgba(45, 212, 191, 0.25);
                    border-radius: 1rem; padding: 1rem 1.2rem; margin: 1rem 0;">
            <h3 style="margin-top:0;">🤖 AI postprocessing {city_part}</h3>
            <p style="margin-bottom: 0.4rem;">Dane zostały lekko wygładzone i przycięte do realistycznych zakresów.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if ai_notes:
        st.write("Notatki AI:")
        for n in ai_notes:
            st.write(f"- {n}")
