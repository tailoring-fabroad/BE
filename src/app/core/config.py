from functools import lru_cache
from typing import Dict, Type

from src.app.core.settings.app import AppSettings
from src.app.core.settings.base import AppEnvTypes, BaseAppSettings
from src.app.core.settings.development import DevAppSettings
from src.app.core.settings.production import ProdAppSettings
from src.app.core.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
