from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "erp-crm-aurumdecor"
    environment: str = "development"
    database_url: str
    secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
