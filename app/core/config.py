import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL_ASYNC: str = os.getenv("DATABASE_URL_ASYNC")
    DATABASE_URL_SYNC: str = os.getenv("DATABASE_URL_SYNC")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",60 ))
    
    

settings = Settings()
