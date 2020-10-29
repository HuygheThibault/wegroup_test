from __future__ import absolute_import

from importlib.metadata import version

from pydantic import BaseSettings, SecretStr

try:  # nosec
    from dotenv import load_dotenv

    load_dotenv(verbose=True)
except Exception:  # nosec
    pass


class Config(BaseSettings):
    FASTAPI_VERSION: str = version("fastapi")
    PYDANTIC_VERSION: str = version("pydantic")
    HTTPX_VERSION: str = version("httpx")
    DB_DSN: SecretStr


config = Config()
