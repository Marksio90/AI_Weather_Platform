from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class AppConfig:
    app_name: str = "AI Weather Platform"
    default_lat: float = 52.2297
    default_lon: float = 21.0122
    default_lang: str = "pl"
    default_timezone: str = "auto"

    @staticmethod
    def from_env() -> "AppConfig":
        return AppConfig(
            default_lang=os.getenv("APP_DEFAULT_LANG", "pl"),
        )

CONFIG = AppConfig.from_env()
