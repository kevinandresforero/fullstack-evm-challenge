from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/evm_db"
    echo_sql: bool = False
    api_prefix: str = "/api"
    project_name: str = "EVM Project Manager API"
    project_version: str = "1.0.0"


settings = Settings()
