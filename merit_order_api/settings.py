import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "powerplant-coding-challenge"
    PROJECT_VERSION: float = 1.0
    DOMAIN_ENV: str = "development"
    MOCK_API_CALLS_FOR_TESTS: bool = False
    Test: bool = False

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../env/local.env")
        env_file_encoding = 'utf-8'