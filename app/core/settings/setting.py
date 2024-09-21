from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    external_api: str
    time_window_hour: int = 1

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
