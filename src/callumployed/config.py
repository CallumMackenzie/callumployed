from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class LlmSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CALLUMPLOYED_LLM_",
        env_file=(ROOT / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    provider: str = Field(default="openai")
    model: str = Field(default="gpt-4.1-mini")
    openai_api_key: SecretStr | None = Field(default=None, validation_alias="OPENAI_API_KEY")
