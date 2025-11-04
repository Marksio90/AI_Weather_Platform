from __future__ import annotations
from dataclasses import dataclass

@dataclass
class User:
    username: str
    plan: str

def get_current_user(username: str, plan: str) -> "User":
    return User(username=username, plan=plan)

def check_feature_access(user: User, feature: str) -> bool:
    if user.plan == "enterprise":
        return True
    if user.plan == "pro":
        return feature in {"tts", "radar"}
    return feature in set()
