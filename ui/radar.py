from __future__ import annotations
import streamlit as st


def _radar_desc(lang: str) -> str:
    if lang == "pl":
        return (
            "Poniżej osadzony jest przykładowy widżet radarowo-satelitarny. "
            "W wersji produkcyjnej podmień URL na komercyjnego lub własnego dostawcę danych."
        )
    return (
        "Below is an example embedded radar/satellite widget. "
        "In production, replace the URL with your commercial or internal data provider."
    )


def render_radar_iframe(
    lat: float,
    lon: float,
    lang: str = "pl",
    *,
    provider: str = "windy",
    height: int = 430,
    api_key: str | None = None,
) -> None:
    """
    Renderuje sekcję z radarem/satelitą.
    - provider="windy" – szybki, publiczny embed
    - provider="rainviewer" – inny, też popularny
    - api_key – w razie gdybyś osadzał płatnego dostawcę
    """
    title = "🛰️ Radar / Satelita" if lang == "pl" else "🛰️ Radar / Satellite"
    st.subheader(title)
    st.markdown(
        f"<p style='color: #94a3b8;'>{_radar_desc(lang)}</p>",
        unsafe_allow_html=True,
    )

    # wybór providera – teraz 2 przykładowych
    if provider == "windy":
        src = (
            "https://embed.windy.com/embed2.html"
            f"?lat={lat:.2f}&lon={lon:.2f}"
            f"&detailLat={lat:.2f}&detailLon={lon:.2f}"
            "&zoom=5&level=surface&overlay=rain"
            "&menu=&message=&marker=&calendar=&pressure=&type=map"
            "&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
        )
    elif provider == "rainviewer":
        # RainViewer też ma embed, tu możesz wstawić swój URL albo build z backendu
        src = f"https://www.rainviewer.com/map.html?loc={lat:.2f},{lon:.2f},7&o=1"
    else:
        # fallback – pokażemy chociaż Windy
        src = (
            "https://embed.windy.com/embed2.html"
            f"?lat={lat:.2f}&lon={lon:.2f}&zoom=5&overlay=rain"
        )

    # jeśli kiedyś będziesz miał własny tile server wymagający tokena, możesz go skleić tu:
    if api_key is not None:
        # przykładowo: src = f"{src}&api_key={api_key}"
        pass

    st.components.v1.html(
        f'<iframe width="100%" height="{height}" src="{src}" frameborder="0"></iframe>',
        height=height,
        scrolling=False,
    )
