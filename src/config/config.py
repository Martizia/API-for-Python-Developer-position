from typing import Any
import os
from pathlib import Path
from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings

path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "../../.env")


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY_JWT: str
    ALGORITHM: str

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: Any):
        if v not in ["HS256", "HS512"]:
            raise ValueError("Algorithm must be HS256 or HS512")
        return v

    model_config = ConfigDict(
        extra="ignore", env_file=config_path, env_file_encoding="utf-8"  # noqa
    )


config = Settings()
