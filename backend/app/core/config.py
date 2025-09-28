"""Application configuration and settings management."""
from functools import lru_cache
from typing import Any

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Container for environment-driven configuration."""

    environment: str = Field("development", description="Runtime environment name")
    api_v1_prefix: str = "/api"
    allowed_origins: list[str] = Field(default_factory=lambda: ["*"])

    okx_base_url: str = Field("https://www.okx.com", env="OKX_BASE_URL")
    okx_api_key: str = Field("", env="OKX_API_KEY")
    okx_api_secret: str = Field("", env="OKX_API_SECRET")
    okx_passphrase: str = Field("", env="OKX_PASSPHRASE")

    deepseek_api_url: str = Field("https://api.deepseek.com/v1", env="DEEPSEEK_API_URL")
    deepseek_api_key: str = Field("", env="DEEPSEEK_API_KEY")

    database_url: str = Field(
        "postgresql+asyncpg://quant_user:quant_pass@db:5432/quant_trading",
        env="DATABASE_URL",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("allowed_origins", pre=True)
    def split_origins(cls, value: Any) -> list[str]:  # noqa: N805
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()


settings = get_settings()
