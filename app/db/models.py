from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, TIMESTAMP, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import ulid
from app.db.database import Base  # Ensure this is your SQLAlchemy Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_ulid = Column(String(26), unique=True, nullable=False, default=lambda: ulid.new().str)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)
    phone_number = Column(String(15), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(20), nullable=True)
    last_login = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")


class Note(Base):
    __tablename__ = "notes"
    id = Column(String(26), primary_key=True, default=lambda: ulid.new().str)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    category_id = Column(String(26), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    pinned = Column(Boolean, default=False)
    order_index = Column(Integer, nullable=False, default=0)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    is_archived = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="notes")
    category = relationship("Category", back_populates="notes")  # ✅ Added missing relationship
    attachments = relationship("Attachment", back_populates="note", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(26), primary_key=True, default=lambda: ulid.new().str)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)  # ✅ Allow NULL
    name = Column(String(50), nullable=False)
    color = Column(String(10), nullable=True, default="#FFFFFF")  # Default color
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="categories")
    notes = relationship("Note", back_populates="category")  # ✅ Added missing relationship


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(String(26), primary_key=True, default=lambda: ulid.new().str)
    note_id = Column(String(26), ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    storage_type = Column(String(10), nullable=False, default="s3")  # "db" for inline, "s3" for external
    file_size = Column(Integer, nullable=False)  # File size in bytes
    file_url = Column(String, nullable=True)  # Used for AWS S3 storage
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    note = relationship("Note", back_populates="attachments")
