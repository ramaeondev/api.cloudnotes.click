from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from app.db.database import Base  # Ensure this is your SQLAlchemy Base
from ulid import ULID

class User(Base):
    __tablename__ = "users"

    id = Column(String(26), primary_key=True, default=lambda: str(ULID()))  # ULID as primary key
    integer_id = Column(Integer, unique=True, nullable=False, autoincrement=True)  # New Integer ID
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=True)
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
