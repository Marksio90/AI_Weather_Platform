from __future__ import annotations
import os
from datetime import datetime

BASE_DIR = "/mnt/data"

def get_logs_dir() -> str:
    return os.path.join(BASE_DIR, "ai-weather-logs")

def init_storage_dir() -> None:
    os.makedirs(get_logs_dir(), exist_ok=True)

def save_verification_result(metrics: dict) -> str:
    logs_dir = get_logs_dir()
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(logs_dir, f"verification_{ts}.txt")
    with open(path, "w", encoding="utf-8") as f:
        for k, v in metrics.items():
            f.write(f"{k}: {v}\n")
    return path
