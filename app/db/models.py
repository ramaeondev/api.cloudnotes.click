from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from app.db.database import Base  # Ensure this is your SQLAlchemy Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # This should match the DB
    profile_picture = Column(String, nullable=True)
    phone_number = Column(String(15), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(20), nullable=True)
    last_login = Column(TIMESTAMP, nullable=True)
    from sqlalchemy.sql import func
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)
