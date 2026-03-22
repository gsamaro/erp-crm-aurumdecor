from app.config.settings import Settings


def test_settings_loads_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    monkeypatch.setenv("SECRET_KEY", "test-secret")

    settings = Settings()

    assert settings.database_url.startswith("postgresql://")
    assert settings.secret_key == "test-secret"
