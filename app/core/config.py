import os
from functools import lru_cache
from typing import ClassVar
from pydantic_settings import BaseSettings
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base,engine

def init_cors(app):
    """Initialize CORS settings for the FastAPI application."""
    config = get_config()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,  # ✅ Use allowed origins from config
        allow_credentials=True, 
        allow_methods=["*"],  # ✅ Allow all methods
        allow_headers=["*"],  # ✅ Allow all headers
        expose_headers=["*"],  # ✅ Expose all headers
        max_age=600,  # Cache preflight requests for 10 minutes
    )
   # Debugging Log
    print(f"✅ CORS Allowed Origins: {config.allowed_origins}")  # 🛠 Debugging
    
def init_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(bind=engine)

class Config(BaseSettings):
    """Configuration settings for the application."""
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME")  # 🔴 Use a real secret in production!
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    CONFIRMATION_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("CONFIRMATION_TOKEN_EXPIRE_MINUTES", 60))
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    FRONTEND_URLS: str = os.getenv("FRONTEND_URLS", "https://platform.cloudnotes.click,https://cloudnotes.click")
    ALGORITHM:str = os.getenv("ALGORITHM", "HS256")
    PWD_CONTEXT: ClassVar[CryptContext] = CryptContext(schemes=["bcrypt"], deprecated="auto")

    allowed_origins: list[str] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        env = os.getenv("ENV", "development")
        frontend_urls = self.FRONTEND_URLS.split(",")
        self.allowed_origins = [url.strip() for url in frontend_urls] if env == "production" else ["*"]


    
@lru_cache
def get_config():
    """Returns a cached instance of Config to avoid multiple reinitializations."""
    return Config()
