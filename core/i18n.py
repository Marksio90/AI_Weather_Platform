_STRINGS = {
    "pl": {
        "app_title": "🌍 AI Prognoza Pogody",
        "location_label": "Wpisz lokalizację (na razie używamy współrzędnych):",
        "forecast_header": "Prognoza godzinowa",
        "temperature": "Temperatura (°C)",
        "precipitation": "Opad (mm)",
        "last_update": "Ostatnia aktualizacja danych:",
        "error_fetch": "Nie udało się pobrać danych pogodowych.",
    },
    "en": {
        "app_title": "🌍 AI Weather Forecast",
        "location_label": "Enter location (for now using coordinates):",
        "forecast_header": "Hourly forecast",
        "temperature": "Temperature (°C)",
        "precipitation": "Precipitation (mm)",
        "last_update": "Last data update:",
        "error_fetch": "Failed to fetch weather data.",
    },
}

def t(key: str, lang: str = "pl") -> str:
    return _STRINGS.get(lang, _STRINGS["en"]).get(key, key)
