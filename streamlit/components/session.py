from __future__ import annotations

import time
from typing import MutableMapping

SESSION_TIMEOUT_SECONDS = 15 * 60


def is_session_active(session: MutableMapping[str, object], now: float | None = None) -> bool:
    token = session.get("access_token")
    last_activity = session.get("last_activity")
    if not token or not isinstance(last_activity, (int, float)):
        return False
    current = now if now is not None else time.time()
    return (current - float(last_activity)) <= SESSION_TIMEOUT_SECONDS


def refresh_session(session: MutableMapping[str, object], now: float | None = None) -> None:
    session["last_activity"] = now if now is not None else time.time()


def clear_session(session: MutableMapping[str, object]) -> None:
    session.pop("access_token", None)
    session.pop("last_activity", None)


def enforce_session(session: MutableMapping[str, object], now: float | None = None) -> bool:
    if not is_session_active(session, now=now):
        clear_session(session)
        return False
    refresh_session(session, now=now)
    return True
