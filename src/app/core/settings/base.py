from enum import Enum
from pydantic_settings import BaseSettings
from pydantic import Field


class AppEnvTypes(str, Enum):
    prod = "prod"
    dev = "dev"
    test = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = Field(default=AppEnvTypes.dev)

    class Config:
        env_file = ".env"
        extra = "ignore"
