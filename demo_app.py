from __future__ import annotations

from typing import Optional, List, Dict, Any
import pandas as pd
import requests
import streamlit as st

# ================== USTAWIENIA STRONY ==================
st.set_page_config(
    page_title="🌦 AI Weather DEMO",
    page_icon="🌦",
    layout="wide",
)

# ================== HERO ==================
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#0f172a 0%,#312e81 100%);
                padding:1.05rem 1.25rem;
                border-radius:1.1rem;
                margin-bottom:1rem;">
      <h1 style="color:#e2e8f0;margin-bottom:0.25rem;">🌦 AI Weather – Demo</h1>
      <p style="color:rgba(226,232,240,.78);margin-bottom:0;">
        Lokalizacja → prognoza → wnioski → wykresy → mapa.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ======= próba użycia Twoich modułów (po cichu) =======
search_locations_func = None
fetch_weather_df_func = None
try:
    from ingestion.open_meteo_client import search_locations as _s  # type: ignore

    search_locations_func = _s
except Exception:
    pass
try:
    from weather.services import fetch_weather_df as _f  # type: ignore

    fetch_weather_df_func = _f
except Exception:
    pass


# ======= fallbacki – tylko w kodzie, UI milczy =======
def fallback_search_locations(name: str, count: int = 5, language: str = "pl") -> List[Dict[str, Any]]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": name,
        "count": count,
        "language": language,
        "format": "json",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("results", []) or []
    except Exception:
        return []


def fallback_fetch_weather_df(lat: float, lon: float, days: int = 3) -> pd.DataFrame:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,weathercode",
        "forecast_days": days,
        "timezone": "auto",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    df = pd.DataFrame({"time": times})
    for col in ["temperature_2m", "relative_humidity_2m", "precipitation", "weathercode"]:
        if col in hourly:
            df[col] = hourly[col]
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")
    return df


def weathercode_to_text(code: int) -> str:
    mapping = {
        0: "bezchmurnie",
        1: "słonecznie",
        2: "częściowe zachmurzenie",
        3: "zachmurzenie",
        45: "mgła",
        48: "mgła osadzająca",
        51: "mżawka lekka",
        53: "mżawka",
        55: "mżawka gęsta",
        61: "deszcz lekki",
        63: "deszcz",
        65: "deszcz intensywny",
        80: "przelotne opady",
        81: "mocniejsze opady",
        82: "ulewne opady",
        95: "burza",
        96: "burza z gradem",
        99: "silna burza z gradem",
    }
    return mapping.get(int(code), "warunki mieszane")


# ================== UI: lokalizacja + parametry ==================
c1, c2 = st.columns([2.2, 0.8])

with c1:
    query = st.text_input("🔎 Lokalizacja", value="Warszawa")
    if query.strip():
        if search_locations_func:
            raw_results = search_locations_func(query, count=6, language="pl")
        else:
            raw_results = fallback_search_locations(query, count=6, language="pl")
    else:
        raw_results = []

    options = []
    for r in raw_results:
        parts = [r.get("name", "—")]
        if r.get("admin1"):
            parts.append(r["admin1"])
        if r.get("country"):
            parts.append(r["country"])
        if r.get("latitude") is not None and r.get("longitude") is not None:
            parts.append(f"({r['latitude']:.2f}, {r['longitude']:.2f})")
        options.append(
            {
                "label": ", ".join(parts),
                "lat": r.get("latitude"),
                "lon": r.get("longitude"),
            }
        )

    if options:
        label = st.selectbox("📍 Wybierz", [o["label"] for o in options])
        chosen = next(o for o in options if o["label"] == label)
        lat, lon = chosen["lat"], chosen["lon"]
    else:
        st.info("Używam Warszawy.")
        lat, lon = 52.2297, 21.0122

with c2:
    days = st.slider("📆 Dni prognozy", 1, 7, 3)
    smooth_daily = st.checkbox("Agregacja dzienna", value=True)

# ================== pobranie danych ==================
try:
    if fetch_weather_df_func:
        df = fetch_weather_df_func(source="open-meteo", lat=lat, lon=lon, days=days)
    else:
        df = fallback_fetch_weather_df(lat, lon, days)
except Exception:
    df = fallback_fetch_weather_df(lat, lon, days)

if df is None or df.empty:
    st.error("Brak danych pogodowych.")
    st.stop()

df = df.sort_index()

# ================== KPI / szybkie wnioski ==================
max_temp = float(df["temperature_2m"].max())
min_temp = float(df["temperature_2m"].min())
total_precip = float(df.get("precipitation", pd.Series(dtype=float)).sum())
current_code = int(df.iloc[0].get("weathercode", 0))
current_desc = weathercode_to_text(current_code)
avg_hum = float(df.get("relative_humidity_2m", pd.Series(dtype=float)).mean() or 0.0)

k1, k2, k3, k4 = st.columns(4)
k1.metric("🌡 max", f"{max_temp:.1f} °C")
k2.metric("🧊 min", f"{min_temp:.1f} °C")
k3.metric("☔ opady", f"{total_precip:.1f} mm")
k4.metric("💧 wilg.", f"{avg_hum:.0f} %")

# proste alerty
alerts = []
if total_precip > 5:
    alerts.append("możliwe mokre okresy – weź parasol")
if max_temp > 27:
    alerts.append("bardzo ciepło – zadbaj o wodę")
if min_temp < 0:
    alerts.append("przymrozki – uważaj na drogach")
if current_code in (95, 96, 99):
    alerts.append("burzowo – śledź aktualne komunikaty")
if not alerts:
    alerts.append("brak szczególnych zagrożeń w prognozie")

st.markdown("### 🧠 Szybka interpretacja")
st.write(f"Teraz: **{current_desc}**.")
for a in alerts:
    st.write(f"• {a.capitalize()}.")

# ================== dane dzienne (agregacja) ==================
if smooth_daily:
    daily = pd.DataFrame()
    daily["temp_max"] = df["temperature_2m"].resample("D").max()
    daily["temp_min"] = df["temperature_2m"].resample("D").min()
    if "precipitation" in df.columns:
        daily["precipitation_sum"] = df["precipitation"].resample("D").sum()
else:
    daily = None

# ================== zakładki ==================
tab_overview, tab_charts, tab_map, tab_data = st.tabs(
    ["📋 Przegląd", "📈 Wykresy", "🗺 Mapa", "📄 Dane"]
)

with tab_overview:
    st.markdown("#### Najbliższe godziny")
    # pokaż 12 najbliższych
    st.dataframe(df.head(12))

    if daily is not None:
        st.markdown("#### Dzienne podsumowanie")
        st.dataframe(daily)

with tab_charts:
    st.markdown("#### Temperatura godzinowa")
    st.line_chart(df["temperature_2m"])

    if "precipitation" in df.columns:
        st.markdown("#### Opady")
        st.bar_chart(df["precipitation"])

    if daily is not None:
        st.markdown("#### Dzienne maks. temperatury")
        st.line_chart(daily["temp_max"])

with tab_map:
    st.markdown("#### Położenie")
    st.map(
        pd.DataFrame(
            {
                "lat": [lat],
                "lon": [lon],
            }
        ),
        zoom=8,
    )

with tab_data:
    st.markdown("#### Dane godzinowe")
    st.dataframe(df)

    if daily is not None:
        st.markdown("#### Dane dzienne")
        st.dataframe(daily)
