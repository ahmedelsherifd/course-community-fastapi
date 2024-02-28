from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache
import os


class Settings(BaseSettings):
    DBNAME: str
    DBHOST: str
    DBUSER: str
    DBPASS: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env")


@lru_cache
def get_settings(env: str = os.getenv("env")):
    BASE_DIR = Path(__file__).resolve().parent.parent

    if env == "production":
        env_file = str(BASE_DIR / ".env.prod")
    elif env == "testing":
        env_file = str(BASE_DIR / ".env.testing")
    else:
        env_file = str(BASE_DIR / ".env")

    return Settings(_env_file=env_file)
