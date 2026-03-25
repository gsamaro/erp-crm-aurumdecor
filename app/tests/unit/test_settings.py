from app.config.settings import Settings


def test_settings_loads_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("ENCRYPTION_KEY", "test-encryption-key")

    settings = Settings()

    assert settings.database_url.startswith("postgresql://")
    assert settings.secret_key == "test-secret"
    assert settings.encryption_key == "test-encryption-key"
