import importlib
from types import SimpleNamespace

import sqlalchemy
import sqlalchemy.engine


def test_engine_uses_ssl_for_postgres(monkeypatch):
    called = {}

    def fake_create_engine(url, **kwargs):
        called["url"] = url
        called["kwargs"] = kwargs
        return object()

    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setattr(sqlalchemy, "create_engine", fake_create_engine)
    monkeypatch.setattr(
        sqlalchemy.engine, "make_url", lambda _: SimpleNamespace(drivername="postgresql")
    )

    import app.config.database as database

    importlib.reload(database)

    assert called["kwargs"]["connect_args"]["sslmode"] == "require"
