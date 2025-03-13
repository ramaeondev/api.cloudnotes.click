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
        allow_origins=config.allowed_origins,
        allow_credentials=True, 
        allow_methods=["*"],
        allow_headers=["*"],
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
        return self.FRONTEND_URL.split(",")
    
@lru_cache
def get_config():
    """Returns a cached instance of Config to avoid multiple reinitializations."""
    return Config()
