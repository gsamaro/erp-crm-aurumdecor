import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from components.session import (  # noqa: E402
    SESSION_TIMEOUT_SECONDS,
    clear_session,
    enforce_session,
    is_session_active,
    refresh_session,
)


def test_session_active_false_without_token():
    session = {}
    assert not is_session_active(session, now=100.0)


def test_session_active_true_with_token_and_recent_activity():
    session = {"access_token": "token", "last_activity": 100.0}
    assert is_session_active(session, now=100.0 + SESSION_TIMEOUT_SECONDS - 1)


def test_session_inactive_after_timeout():
    session = {"access_token": "token", "last_activity": 100.0}
    assert not is_session_active(session, now=100.0 + SESSION_TIMEOUT_SECONDS + 1)


def test_enforce_session_clears_expired():
    session = {"access_token": "token", "last_activity": 100.0}
    assert not enforce_session(session, now=100.0 + SESSION_TIMEOUT_SECONDS + 10)
    assert "access_token" not in session


def test_refresh_session_updates_timestamp():
    session = {"access_token": "token"}
    refresh_session(session, now=123.0)
    assert session["last_activity"] == 123.0


def test_clear_session_removes_keys():
    session = {"access_token": "token", "last_activity": 100.0}
    clear_session(session)
    assert session == {}
