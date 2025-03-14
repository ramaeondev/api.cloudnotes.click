from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, TIMESTAMP, Text, Index, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import ulid
from app.db.database import Base
import re

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
    is_admin = Column(Boolean, default=False)
    role = Column(String(20), nullable=True)
    
    last_login = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    extra_data = Column(JSON, nullable=True)
    
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_last_login', 'last_login'),
    )
    
    @classmethod
    def validate_email(cls, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

class Category(Base):
    __tablename__ = "categories"
    
    numeric_id = Column(Integer, primary_key=True, autoincrement=True)
    # ULID string as identifier
    id = Column(String(26), unique=True, nullable=False, default=lambda: ulid.new().str)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    name = Column(String(50), nullable=False)
    color_id = Column(Integer, ForeignKey("colors.id", ondelete="SET NULL"), nullable=True)
    
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="categories")
    notes = relationship("Note", back_populates="category")
    color = relationship("Color", back_populates="categories")

class Note(Base):
    __tablename__ = "notes"
    
    # Using ULID string as primary key
    id = Column(String(26), primary_key=True, default=lambda: ulid.new().str)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    # Ensure category_id is stored as a string to match the ULID in categories.id
    category_id = Column(String(26), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    pinned = Column(Boolean, default=False)
    order_index = Column(Integer, nullable=False, default=0)
    
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    is_archived = Column(Boolean, default=False)
    
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    user = relationship("User", back_populates="notes")
    category = relationship("Category", back_populates="notes")
    attachments = relationship("Attachment", back_populates="note", cascade="all, delete-orphan")

class Attachment(Base):
    __tablename__ = "attachments"
    
    id = Column(String(26), primary_key=True, default=lambda: ulid.new().str)
    note_id = Column(String(26), ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    storage_type = Column(String(10), nullable=False, default="s3")
    file_size = Column(Integer, nullable=False)
    file_url = Column(String, nullable=True)
    
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    note = relationship("Note", back_populates="attachments")
    
    __table_args__ = (
        Index('idx_attachment_note', 'note_id'),
        Index('idx_attachment_storage', 'storage_type'),
    )

class Color(Base):
    __tablename__ = "colors"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String(10), unique=True, nullable=False)
    
    categories = relationship("Category", back_populates="color")
    
    __table_args__ = (
        Index('idx_color_unique', 'color'),
    )
