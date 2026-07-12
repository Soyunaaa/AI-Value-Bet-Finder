from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    football_data_api_key: str
    football_data_base_url: str = (
        "https://api.football-data.org/v4"
    )

    odds_api_key: str
    odds_api_base_url: str = (
        "https://api.the-odds-api.com/v4"
    )
    odds_api_default_region: str = "eu"

    database_url: str = (
        "sqlite+aiosqlite:///./database/value_bet_finder.db"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()