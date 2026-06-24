from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AHIP API"
    database_url: str = "sqlite:///./ahip.db"
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
