from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    PRIVATE_KEY: str
    PUBLIC_KEY: str
    ACCESS_EXPIRE_MINUTES: int 
    REFRESH_EXPIRE_DAYS: int

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


load_dotenv(override=True)  
settings = Settings()