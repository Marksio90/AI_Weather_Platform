from __future__ import annotations
import streamlit as st

from core.config import CONFIG
from core.logging_config import setup_logging
from core.i18n import t
from core.auth import get_current_user, check_feature_access
from core.storage import init_storage_dir
from ingestion.geocoding_client import search_locations, format_location_option
from weather.services import get_hourly_dataframe, SUPPORTED_SOURCES
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
from ai.postprocess import apply_basic_ai_corrections
from ai.text_forecast import build_text_forecast
from ai.tts import synthesize_speech_to_bytes
from ai.model_slot import apply_model_slot

def main() -> None:
    setup_logging()
    init_storage_dir()
    st.set_page_config(
        page_title="AI Weather Platform",
        page_icon="🌦️",
        layout="wide",
    )

    # --- mock "logowanie" / wybór roli ---
    with st.sidebar:
        st.markdown("### 👤 Użytkownik")
        username = st.text_input("Nazwa użytkownika", value="mateusz")
        plan = st.selectbox(
            "Plan/subskrypcja",
            options=["free", "pro", "enterprise"],
            index=1,
        )
        dev_mode = st.checkbox("🛠️ Tryb walidacji / developer", value=False)

    user = get_current_user(username=username, plan=plan)

    # === SIDEBAR (dalsza część) ===
    lang = st.sidebar.selectbox("Language / Język", options=["pl", "en"], index=0)
    source = st.sidebar.selectbox(
        "Źródło danych / Data source",
        options=SUPPORTED_SOURCES + ["(coming soon) ECMWF", "(coming soon) NOAA"],
        index=0,
    )
    use_ai = st.sidebar.checkbox("AI postprocessing", value=True)
    show_voice = st.sidebar.checkbox("Pokaż tekst prognozy (TTS-ready)", value=True)
    enable_tts = st.sidebar.checkbox("🎧 Wygeneruj audio z prognozy", value=False)

    # === NEW: model slot selector ===
    model_slot_name = st.sidebar.selectbox(
        "AI Model slot",
        options=["none", "mock-graphcast", "mock-downscaler"],
        index=0,
        help="W realu tu wybierzesz prawdziwy model (np. GraphCast). Teraz mamy makiety.",
    )

    render_header(lang)
    render_business_panel(user)

    # --- wyszukiwanie miasta ---
    city_query = render_location_search(lang)

    if "selected_location" not in st.session_state:
        st.session_state.selected_location = None

    locations = []
    if city_query:
        locations = search_locations(city_query, language=lang)
    selected_lat = CONFIG.default_lat
    selected_lon = CONFIG.default_lon
    selected_city_name = None

    if locations:
        options_labels = [format_location_option(loc) for loc in locations]
        chosen_idx = st.selectbox(
            "Wybierz lokalizację z wyników",
            options=list(range(len(options_labels))),
            format_func=lambda i: options_labels[i],
            index=0,
        )
        chosen_location = locations[chosen_idx]
        st.session_state.selected_location = chosen_location
        selected_lat = float(chosen_location["latitude"])
        selected_lon = float(chosen_location["longitude"])
        selected_city_name = chosen_location["name"]
        st.success(
            f"Wybrano: {chosen_location['name']} ({chosen_location['latitude']:.2f}, {chosen_location['longitude']:.2f})"
        )
    else:
        st.info("Brak wyników lub jeszcze nie szukałeś – możesz podać współrzędne ręcznie.")
        selected_lat, selected_lon = render_coords_inputs(CONFIG.default_lat, CONFIG.default_lon, lang)

    # --- pobranie prognozy ---
    real_source = source if source in SUPPORTED_SOURCES else "open-meteo"
    df = get_hourly_dataframe(
        lat=selected_lat,
        lon=selected_lon,
        timezone=CONFIG.default_timezone,
        days=7,
        source=real_source,
    )

    if df is not None:
        # === MODEL SLOT ===
        df_model, model_notes = apply_model_slot(df, model_slot_name, lat=selected_lat, lon=selected_lon)

        # AI POSTPROCESS (po modelu slot)
        if use_ai:
            df_ai, ai_notes = apply_basic_ai_corrections(df_model)
        else:
            df_ai, ai_notes = df_model, []

        ai_notes = list(model_notes) + list(ai_notes)

        # Charts
        render_forecast_charts(df_ai, lang)

        # Alerts
        render_alerts(df_ai, lang=lang)

        # AI summary card
        render_ai_summary_card(df_ai, ai_notes, lang=lang, city_name=selected_city_name)

        # TTS text builder (display + audio)
        if show_voice:
            st.subheader("🗣️ Tekst prognozy / TTS-ready")
            forecast_text = build_text_forecast(df_ai, lang=lang, city_name=selected_city_name)
            st.text_area("Tekst do przeczytania", forecast_text, height=140)

            if enable_tts:
                if check_feature_access(user, "tts"):
                    if st.button("🔊 Wygeneruj i odtwórz prognozę"):
                        audio_bytes = synthesize_speech_to_bytes(forecast_text, lang=lang)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
                        else:
                            st.error("Nie udało się wygenerować audio.")
                else:
                    st.warning("Twój plan nie obejmuje TTS. Ulepsz do PRO lub ENTERPRISE.")

        # Radar / mapa
        if check_feature_access(user, "radar"):
            render_radar_iframe(selected_lat, selected_lon, lang=lang)
        else:
            st.info("Radar/satelita dostępne w planie PRO. Ulepsz plan, aby oglądać dane radarowe.")

        # Nowcasting placeholder
        render_nowcasting_placeholder(selected_lat, selected_lon, lang=lang)

        # Walidacja / verification panel
        if dev_mode or check_feature_access(user, "verification"):
            render_verification_panel(df_ai)

        st.caption(f"{t('last_update', lang)} {df.index.max()}")
    else:
        st.error(t("error_fetch", lang))

    st.markdown("---")
    st.caption("v0.7 • AI model slot (mock) + wcześniejsze moduły")

if __name__ == "__main__":
    main()
