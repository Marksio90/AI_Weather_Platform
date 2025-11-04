from __future__ import annotations

import streamlit as st
import pandas as pd
import logging

# === CORE / CONFIG ===
try:
    from core.config import CONFIG
except Exception:  # awaryjnie, żeby się dało uruchomić
    class _FallbackConfig:
        app_name = "AI Weather Platform"
        default_lat = 52.2297
        default_lon = 21.0122
        default_lang = "pl"
        default_timezone = "auto"
    CONFIG = _FallbackConfig()

from core.logging_config import setup_logging
from core.i18n import t
from core.auth import get_current_user, check_feature_access
from core.storage import init_storage_dir

# === DOMAIN ===
from ingestion.geocoding_client import search_locations, format_location_option
from weather.services import get_hourly_dataframe, SUPPORTED_SOURCES

# === UI ===
from ui.layout import (
    render_header,
    render_location_search,
    render_coords_inputs,
    render_forecast_charts,
)
from ui.sections import render_nowcasting_placeholder, render_ai_summary_card
from ui.alerts import render_alerts
from ui.radar import render_radar_iframe
from ui.business import render_business_panel
from ui.verification import render_verification_panel

# === AI / POST ===
from ai.postprocess import apply_basic_ai_corrections
from ai.text_forecast import build_text_forecast
from ai.tts import synthesize_speech_to_bytes
from ai.model_slot import apply_model_slot


# ---------------------------
# CACHING / HELPERS
# ---------------------------

@st.cache_data(show_spinner=False)
def cached_forecast(
    lat: float,
    lon: float,
    timezone: str,
    days: int,
    source: str,
) -> pd.DataFrame | None:
    """
    Proste cachowanie prognozy – żeby przy zmianie UI nie walić co chwilę w API.
    Klucz: wszystkie argumenty.
    """
    return get_hourly_dataframe(
        lat=lat,
        lon=lon,
        timezone=timezone,
        days=days,
        source=source,
    )


def _select_location_from_search(city_query: str, lang: str):
    """
    Obsługuje scenariusz: user wpisał miasto → pobierz listę → pozwól wybrać.
    Zwraca (name, lat, lon) albo (None, default lat/lon)
    """
    locations = []
    if city_query:
        locations = search_locations(city_query, language=lang)

    if locations:
        options_labels = [format_location_option(loc) for loc in locations]
        chosen_idx = st.selectbox(
            "Wybierz lokalizację z wyników",
            options=list(range(len(options_labels))),
            format_func=lambda i: options_labels[i],
            index=0,
        )
        chosen_location = locations[chosen_idx]
        st.success(
            f"Wybrano: {chosen_location['name']} "
            f"({chosen_location['latitude']:.2f}, {chosen_location['longitude']:.2f})"
        )
        return (
            chosen_location["name"],
            float(chosen_location["latitude"]),
            float(chosen_location["longitude"]),
        )

    # brak wyników – ręczne współrzędne
    st.info("Brak wyników lub jeszcze nie szukałeś – możesz podać współrzędne ręcznie.")
    lat, lon = render_coords_inputs(CONFIG.default_lat, CONFIG.default_lon, lang)
    return None, lat, lon


# ---------------------------
# MAIN APP
# ---------------------------

def main() -> None:
    log = setup_logging(__name__)
    init_storage_dir()

    st.set_page_config(
        page_title=CONFIG.app_name,
        page_icon="🌦️",
        layout="wide",
    )

    # ============ SIDEBAR – USER / PLAN ============
    with st.sidebar:
        st.markdown("### 👤 Użytkownik")
        username = st.text_input("Nazwa użytkownika", value="mateusz")
        plan = st.selectbox(
            "Plan/subskrypcja",
            options=["free", "pro", "enterprise"],
            index=1,
            help="Plan decyduje o dostępie do TTS, radaru i walidacji.",
        )
        dev_mode = st.checkbox("🛠️ Tryb walidacji / developer", value=False)

    user = get_current_user(username=username, plan=plan)

    # ============ SIDEBAR – SETTINGS ============
    lang = st.sidebar.selectbox("Language / Język", options=["pl", "en"], index=0)
    source = st.sidebar.selectbox(
        "Źródło danych / Data source",
        options=SUPPORTED_SOURCES + ["(coming soon) ECMWF", "(coming soon) NOAA"],
        index=0,
    )
    use_ai = st.sidebar.checkbox("AI postprocessing", value=True)
    show_voice = st.sidebar.checkbox("Pokaż tekst prognozy (TTS-ready)", value=True)
    enable_tts = st.sidebar.checkbox("🎧 Wygeneruj audio z prognozy", value=False)
    model_slot_name = st.sidebar.selectbox(
        "AI Model slot",
        options=["none", "mock-graphcast", "mock-downscaler"],
        index=0,
        help="Slot na prawdziwy model (GraphCast / HF). Teraz makiety.",
    )

    # ============ HEADER + PANEL UŻYTKOWNIKA ============
    render_header(lang)
    render_business_panel(user)

    # ============ LOCATION INPUT ============
    city_query = render_location_search(lang)
    selected_city_name, selected_lat, selected_lon = _select_location_from_search(city_query, lang)

    # ============ FETCH FORECAST ============
    real_source = source if source in SUPPORTED_SOURCES else "open-meteo"
    try:
        df = cached_forecast(
            lat=selected_lat,
            lon=selected_lon,
            timezone=CONFIG.default_timezone,
            days=7,
            source=real_source,
        )
    except Exception as exc:
        log.exception("Błąd przy pobieraniu prognozy: %s", exc)
        df = None

    if df is None:
        st.error(t("error_fetch", lang))
        st.stop()

    # ============ AI MODEL SLOT ============
    df_model, model_notes = apply_model_slot(
        df,
        slot_name=model_slot_name,
        lat=selected_lat,
        lon=selected_lon,
    )

    # ============ AI POSTPROCESS ============
    if use_ai:
        df_ai, ai_notes = apply_basic_ai_corrections(df_model)
    else:
        df_ai, ai_notes = df_model, []

    # scal notatki
    all_notes = list(model_notes) + list(ai_notes)

    # ============ VISUALS ============
    render_forecast_charts(df_ai, lang)
    render_alerts(df_ai, lang=lang)
    render_ai_summary_card(df_ai, all_notes, lang=lang, city_name=selected_city_name)

    # ============ TTS / TEXT ============
    if show_voice:
        st.subheader("🗣️ " + t("voice.title", lang) if t("voice.title", lang) else "🗣️ Tekst prognozy")
        forecast_text = build_text_forecast(df_ai, lang=lang, city_name=selected_city_name)
        st.text_area("Tekst do przeczytania", forecast_text, height=160)

        if enable_tts:
            if check_feature_access(user, "tts"):
                if st.button("🔊 Wygeneruj i odtwórz prognozę"):
                    audio_bytes = synthesize_speech_to_bytes(forecast_text, lang=lang)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")
                    else:
                        st.error("Nie udało się wygenerować audio (sprawdź internet / gTTS).")
            else:
                st.warning("Twój plan nie obejmuje TTS. Ulepsz do PRO lub ENTERPRISE.")

    # ============ RADAR ============
    if check_feature_access(user, "radar"):
        render_radar_iframe(selected_lat, selected_lon, lang=lang)
    else:
        st.info("Radar/satelita dostępne w planie PRO. Ulepsz plan, aby oglądać dane radarowe.")

    # ============ NOWCASTING PLACEHOLDER ============
    render_nowcasting_placeholder(selected_lat, selected_lon, lang=lang)

    # ============ VERIFICATION PANEL ============
    if dev_mode or check_feature_access(user, "verification"):
        render_verification_panel(df_ai)

    st.caption(f"{t('last_update', lang)} {df.index.max()}")
    st.markdown("---")
    st.caption("v0.7+ • modular, cached, AI-slot-first")


if __name__ == "__main__":
    main()
