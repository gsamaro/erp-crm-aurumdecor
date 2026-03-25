from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken

from app.config.settings import settings


def _get_fernet() -> Fernet:
    key = settings.encryption_key
    if not key:
        raise RuntimeError("ENCRYPTION_KEY is required")
    try:
        return Fernet(key.encode("utf-8"))
    except Exception as exc:  # pragma: no cover - defensive
        raise ValueError("Invalid ENCRYPTION_KEY") from exc


def encrypt_value(value: str | None) -> str | None:
    if value is None:
        return None
    fernet = _get_fernet()
    return fernet.encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_value(value: str | None) -> str | None:
    if value is None:
        return None
    fernet = _get_fernet()
    try:
        return fernet.decrypt(value.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        raise ValueError("Failed to decrypt value") from exc
