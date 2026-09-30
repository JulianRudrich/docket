"""Runtime configuration, read from environment variables or a local .env file."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DOCKET_", env_file=".env", extra="ignore")

    model: str = "claude-opus-5-5"
    data_dir: Path = Path("data")
    results_dir: Path = Path("results")
    prompt_version: str = "extraction_v1"

    @property
    def labels_dir(self) -> Path:
        return self.data_dir / "labels"

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def splits_file(self) -> Path:
        return self.data_dir / "splits.json"


def get_settings() -> Settings:
    return Settings()
