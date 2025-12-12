from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str
    MASTER_DB_NAME: str = "master_db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
