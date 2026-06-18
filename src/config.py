from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise Resolution Agent"
    database_path: Path = Field(default=Path("data/era.sqlite3"))
    audit_dir: Path = Field(default=Path("data/audit"))
    reports_dir: Path = Field(default=Path("data/reports"))

<<<<<<< HEAD
    ai_provider: str = "local"
    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"

=======
>>>>>>> f0cc8763078e8a8235c2a0c24a43013c507bb539
    openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_deployment: str | None = None

    qdrant_url: str | None = None
    qdrant_api_key: str | None = None

    servicenow_instance_url: str | None = None
    servicenow_token: str | None = None

    langsmith_api_key: str | None = None
    langsmith_project: str = "enterprise-resolution-agent"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    settings.audit_dir.mkdir(parents=True, exist_ok=True)
    settings.reports_dir.mkdir(parents=True, exist_ok=True)
    return settings
