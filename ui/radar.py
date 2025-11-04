from __future__ import annotations
import streamlit as st

def render_radar_iframe(lat: float, lon: float, lang: str = "pl") -> None:
    st.subheader("🛰️ Radar / Satelita (osadzone)")
    st.markdown(
        """
        <p style="color: #94a3b8;">
        Poniżej osadzony jest przykładowy widżet radarowy. W wdrożeniu produkcyjnym
        wstaw tu URL do dostawcy danych radarowych.
        </p>
        """,
        unsafe_allow_html=True,
    )
    html_iframe = f"""
    <iframe width="100%" height="420"
        src="https://embed.windy.com/embed2.html?lat={lat:.2f}&lon={lon:.2f}&detailLat={lat:.2f}&detailLon={lon:.2f}&zoom=5&level=surface&overlay=rain&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
        frameborder="0"></iframe>
    """
    st.components.v1.html(html_iframe, height=430, scrolling=False)
