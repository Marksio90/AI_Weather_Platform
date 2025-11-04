from __future__ import annotations
from typing import Iterable, Optional, Any
import streamlit as st


def render_nowcasting_placeholder(lat: float, lon: float, lang: str = "pl") -> None:
    """
    Placeholder pod przyszły moduł nowcastingu (5–15 min).
    Pokazujemy userowi, że to jest zaplanowane i z czym będzie spięte.
    """
    title = "🌧️ Nowcasting / radar (w przygotowaniu)" if lang == "pl" else "🌧️ Nowcasting / radar (coming soon)"
    st.subheader(title)

    txt_pl = (
        "Ten moduł będzie pobierał najnowszy obraz radarowy/satelitarny i prognozował przesuwanie opadów w horyzoncie 0–3h. "
        "Idealne do burz i nagłych ulew."
    )
    txt_en = (
        "This module will fetch the latest radar/satellite image and nowcast precip movement for 0–3h. "
        "Perfect for storms and sudden downpours."
    )

    st.info(txt_pl if lang == "pl" else txt_en, icon="ℹ️")

    st.caption(
        f"{'Wybrana lokalizacja' if lang == 'pl' else 'Selected location'}: "
        f"lat={lat:.2f}, lon={lon:.2f}"
    )


def render_ai_summary_card(
    df: Any,
    ai_notes: Iterable[str],
    *,
    lang: str = "pl",
    city_name: Optional[str] = None,
) -> None:
    """
    Pokazuje kartę z informacją, że dane zostały przepuszczone przez AI (slot + postprocessing)
    i wypisuje notatki z tego procesu.
    """
    city_part = f"dla {city_name}" if city_name else ""
    subtitle_pl = "Dane zostały skorygowane przez moduły AI (slot modelu + postprocessing)."
    subtitle_en = "Data has been adjusted by AI modules (model slot + postprocessing)."

    st.markdown(
        f"""
        <div style="
            background: rgba(15, 118, 110, 0.12);
            border: 1px solid rgba(45, 212, 191, 0.25);
            border-radius: 1rem;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        ">
            <h3 style="margin-top:0;">🤖 AI postprocessing {city_part}</h3>
            <p style="margin-bottom: 0.4rem;">
                {(subtitle_pl if lang == "pl" else subtitle_en)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    notes_list = list(ai_notes or [])
    if notes_list:
        st.write("Notatki AI:" if lang == "pl" else "AI notes:")
        for n in notes_list:
            st.write(f"- {n}")
    else:
        st.caption("Brak dodatkowych korekt AI." if lang == "pl" else "No additional AI adjustments.")
