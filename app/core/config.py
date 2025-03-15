import os
from functools import lru_cache
from typing import ClassVar
from fastapi import Request
from pydantic_settings import BaseSettings
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base,engine

def init_cors(app):
    """Initialize CORS settings for the FastAPI application."""
    config = get_config()
    origins = config.allowed_origins
    
    # For debugging
    print(f"Allowed origins: {origins}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True, 
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Accept"],
        expose_headers=["Content-Type", "Authorization"],
        max_age=600,  # Cache preflight requests for 10 minutes
    )

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
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:4200")
    ALGORITHM:str = os.getenv("ALGORITHM", "HS256")
    PWD_CONTEXT: ClassVar[CryptContext] = CryptContext(schemes=["bcrypt"], deprecated="auto")
    @property
    def allowed_origins(self):
        """Return allowed origins for CORS."""
        env = os.getenv("ENV", "development")
        if env == "production":
            return self.FRONTEND_URL.split(",")  # Restrict in production
        return ["*"]  # Allow all origins in development


    
@lru_cache
def get_config():
    """Returns a cached instance of Config to avoid multiple reinitializations."""
    return Config()
