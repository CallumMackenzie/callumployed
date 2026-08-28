from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class BrowserSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CALLUMPLOYED_BROWSER_",
        env_file=(ROOT / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    backend: Literal["local", "browserbase"] = Field(default="local")
    headless: bool = Field(default=True)
    timeout_ms: int = Field(default=30_000)
    browserbase_api_key: SecretStr | None = Field(
        default=None,
        validation_alias="BROWSERBASE_API_KEY",
    )


class LlmSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CALLUMPLOYED_LLM_",
        env_file=(ROOT / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    provider: str = Field(default="openai")
    model: str = Field(default="gpt-5.6-terra")
    codex_model: str | None = Field(default=None)
    openai_api_key: SecretStr | None = Field(default=None, validation_alias="OPENAI_API_KEY")
