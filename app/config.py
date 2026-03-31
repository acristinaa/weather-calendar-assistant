from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    latitude: float
    longitude: float

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()