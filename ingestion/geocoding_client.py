from __future__ import annotations
from typing import List, Dict, Any
import requests

BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

def search_locations(
    name: str,
    count: int = 5,
    language: str = "pl",
) -> List[Dict[str, Any]]:
    if not name.strip():
        return []
    params = {
        "name": name,
        "count": count,
        "language": language,
        "format": "json",
    }
    resp = requests.get(BASE_URL, params=params, timeout=10)
    if resp.status_code != 200:
        return []
    data = resp.json()
    return data.get("results", []) or []

def format_location_option(loc: Dict[str, Any]) -> str:
    country = loc.get("country", "")
    admin1 = loc.get("admin1")
    parts = [loc.get("name", "Unknown")]
    if admin1:
        parts.append(admin1)
    if country:
        parts.append(country)
    label = ", ".join(parts)
    return f"{label} ({loc.get('latitude'):.2f}, {loc.get('longitude'):.2f})"
