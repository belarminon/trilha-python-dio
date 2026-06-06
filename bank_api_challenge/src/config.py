from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./bank.db"
    environment: str = "development"
    secret_key: str = "supersecret"
    algorithm: str = "HS256"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
