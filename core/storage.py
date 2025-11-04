from __future__ import annotations
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional


# można nadpisać w dockerze / .env: STORAGE_BASE_DIR=/app/data
BASE_DIR = os.getenv("STORAGE_BASE_DIR", "/mnt/data")
DEFAULT_SUBDIR = "ai-weather-logs"


def get_logs_dir(subdir: str = DEFAULT_SUBDIR) -> str:
    """
    Zwraca pełną ścieżkę do katalogu logów / artefaktów.
    """
    return os.path.join(BASE_DIR, subdir)


def init_storage_dir(subdir: str = DEFAULT_SUBDIR) -> str:
    """
    Tworzy katalog, jeśli nie istnieje. Zwraca jego ścieżkę.
    """
    path = get_logs_dir(subdir)
    os.makedirs(path, exist_ok=True)
    return path


def _timestamp() -> str:
    # 2025-11-04_121314_123456 – z mikrosekundami, żeby uniknąć kolizji
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")


def save_verification_result(
    metrics: Dict[str, Any],
    *,
    subdir: str = DEFAULT_SUBDIR,
    as_json: bool = True,
    filename_prefix: str = "verification",
) -> str:
    """
    Zapisuje wynik walidacji do pliku w storage.

    - domyślnie zapisuje jako JSON (łatwiej potem wczytać),
    - ale można zapisać w formacie "k: v" (as_json=False),
    - zwraca ścieżkę do utworzonego pliku.
    """
    logs_dir = init_storage_dir(subdir)
    ts = _timestamp()
    ext = "json" if as_json else "txt"
    path = os.path.join(logs_dir, f"{filename_prefix}_{ts}.{ext}")

    if as_json:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, ensure_ascii=False, indent=2)
    else:
        with open(path, "w", encoding="utf-8") as f:
            for k, v in metrics.items():
                f.write(f"{k}: {v}\n")

    return path


def save_generic_payload(
    payload: Any,
    *,
    subdir: str = DEFAULT_SUBDIR,
    filename_prefix: str = "payload",
) -> str:
    """
    Uniwersalny zapis czegokolwiek, co da się zjsonować.
    Przydatne np. do dumpowania wyjścia modelu AI.
    """
    logs_dir = init_storage_dir(subdir)
    ts = _timestamp()
    path = os.path.join(logs_dir, f"{filename_prefix}_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path
