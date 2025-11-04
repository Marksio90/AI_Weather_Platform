from __future__ import annotations
from typing import Any, Dict

_STRINGS: Dict[str, Dict[str, Any]] = {
    "pl": {
        "app_title": "🌍 AI Prognoza Pogody",
        "location_label": "Wpisz lokalizację (na razie używamy współrzędnych):",
        "forecast_header": "Prognoza godzinowa",
        "temperature": "Temperatura (°C)",
        "precipitation": "Opad (mm)",
        "last_update": "Ostatnia aktualizacja danych:",
        "error_fetch": "Nie udało się pobrać danych pogodowych.",
        # dodatkowe, które się często przydadzą
        "alerts.header": "⚠️ Alerty pogodowe",
        "alerts.heavy_rain": "Silne opady w najbliższych godzinach.",
        "alerts.very_cold": "Bardzo niska temperatura.",
        "alerts.very_hot": "Bardzo wysoka temperatura.",
        "voice.title": "🗣️ Tekst prognozy / TTS-ready",
        "common.unknown": "Nieznany",
    },
    "en": {
        "app_title": "🌍 AI Weather Forecast",
        "location_label": "Enter location (for now using coordinates):",
        "forecast_header": "Hourly forecast",
        "temperature": "Temperature (°C)",
        "precipitation": "Precipitation (mm)",
        "last_update": "Last data update:",
        "error_fetch": "Failed to fetch weather data.",
        "alerts.header": "⚠️ Weather alerts",
        "alerts.heavy_rain": "Heavy rainfall expected in the next hours.",
        "alerts.very_cold": "Very low temperature expected.",
        "alerts.very_hot": "Very high temperature expected.",
        "voice.title": "🗣️ Forecast text / TTS-ready",
        "common.unknown": "Unknown",
    },
}


def _get_lang_dict(lang: str) -> Dict[str, Any]:
    """Zwraca słownik językowy, albo en jeśli nie ma danego języka."""
    return _STRINGS.get(lang, _STRINGS["en"])


def t(key: str, lang: str = "pl", **kwargs: Any) -> str:
    """
    Pobiera tłumaczenie dla danego klucza.
    - jeśli klucz nie istnieje w danym języku → próbuje en
    - jeśli nadal nie ma → zwraca sam klucz
    - można użyć formatowania: t("hello_user", name="Mateusz")
    """
    lang_dict = _get_lang_dict(lang)
    raw = lang_dict.get(key)

    if raw is None:
        # fallback na en
        raw = _STRINGS["en"].get(key)

    if raw is None:
        # dev-friendly – od razu w UI widać, czego brakuje
        return f"[i18n:{key}]"

    if kwargs:
        try:
            return raw.format(**kwargs)
        except Exception:
            # jak ktoś poda więcej parametrów niż w stringu – trudno, zwracamy raw
            return raw

    return raw
