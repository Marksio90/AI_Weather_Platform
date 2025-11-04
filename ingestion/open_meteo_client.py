from __future__ import annotations
from typing import List, Dict, Any, Optional
import logging
import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"


def search_locations(
    name: str,
    *,
    count: int = 5,
    language: str = "pl",
    session: Optional[requests.Session] = None,
    timeout: int = 10,
) -> List[Dict[str, Any]]:
    """
    Szuka lokalizacji po nazwie w geocodingu Open-Meteo.

    Zwraca listę dictów, albo pustą listę, jeśli nic nie znaleziono
    albo był problem z siecią.

    Uwaga: specjalnie NIE rzucamy wyjątku – UI ma działać dalej.
    """
    name = (name or "").strip()
    if not name:
        return []

    params = {
        "name": name,
        "count": count,
        "language": language,
        "format": "json",
    }

    sess = session or requests
    try:
        resp = sess.get(BASE_URL, params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.warning("Geocoding failed for %r: %s", name, exc)
        return []

    results = data.get("results") or []
    # upewniamy się, że to lista dictów
    if not isinstance(results, list):
        return []
    return results


def get_first_location(
    name: str,
    *,
    language: str = "pl",
    session: Optional[requests.Session] = None,
    timeout: int = 10,
) -> Optional[Dict[str, Any]]:
    """
    Szybki helper: zwróć tylko pierwszy wynik albo None.
    Przydatny na backendzie.
    """
    results = search_locations(
        name,
        count=1,
        language=language,
        session=session,
        timeout=timeout,
    )
    return results[0] if results else None


def format_location_option(loc: Dict[str, Any]) -> str:
    """
    Buduje ładną etykietę do selecta w UI.

    Przykład:
    "Warsaw, Masovian Voivodeship, Poland (52.23, 21.01)"
    """
    name = loc.get("name") or "Unknown"
    country = loc.get("country") or ""
    admin1 = loc.get("admin1") or ""

    parts = [name]
    if admin1:
        parts.append(admin1)
    if country:
        parts.append(country)

    lat = loc.get("latitude")
    lon = loc.get("longitude")

    label = ", ".join(parts)

    if lat is not None and lon is not None:
        return f"{label} ({float(lat):.2f}, {float(lon):.2f})"
    return label
