from __future__ import annotations
from dataclasses import dataclass
from typing import Set, Dict


# zdefiniuj w jednym miejscu, co który plan może
PLAN_FEATURES: Dict[str, Set[str]] = {
    "free": set(),  # tylko podstawy
    "pro": {"tts", "radar"},
    "enterprise": {"tts", "radar", "verification", "admin"},
}


@dataclass(frozen=True)
class User:
    username: str
    plan: str  # "free" | "pro" | "enterprise"
    # w przyszłości: org_id: str | None = None


def normalize_plan(plan: str) -> str:
    """
    Sprowadza plan do małych liter, obsługuje ewentualne aliasy.
    """
    p = plan.strip().lower()
    if p in ("ent", "enterprise", "corp"):
        return "enterprise"
    if p in ("pro", "professional"):
        return "pro"
    return "free" if p == "" else p


def get_current_user(username: str, plan: str) -> User:
    """
    Tworzy obiekt User z ujednoliconym planem.
    """
    return User(username=username, plan=normalize_plan(plan))


def check_feature_access(user: User, feature: str) -> bool:
    """
    Sprawdza, czy użytkownik ma dostęp do danej funkcji.
    Enterprise ma zawsze wszystko zdefiniowane w PLAN_FEATURES["enterprise"].
    """
    plan = normalize_plan(user.plan)
    allowed = PLAN_FEATURES.get(plan, set())
    return feature in allowed
