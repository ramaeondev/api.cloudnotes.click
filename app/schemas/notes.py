from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.schemas.users import UserResponse

class AttachmentResponse(BaseModel):
    id: str
    file_name: str
    file_url: str

    class Config:
        from_attributes = True

# New nested model for Color
class ColorResponse(BaseModel):
    id: int
    color: str

    class Config:
        from_attributes = True

# Updated CategoryResponse using the nested ColorResponse model
class CategoryResponse(BaseModel):
    id: str 
    numeric_id: int 
    name: str
    color: Optional[ColorResponse] = None

    class Config:
        from_attributes = True

class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    date: datetime
    pinned: bool = False
    order_index: int
    is_deleted: bool
    deleted_at: Optional[datetime] = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    user: Optional[UserResponse] = None
    category: Optional[CategoryResponse] = None
    attachments: List[AttachmentResponse] = []

    class Config:
        from_attributes = True  # Ensures the Pydantic model works with SQLAlchemy

class NotesRequest(BaseModel):
    month: int  # UI will send this (1-12)
    year: int   # UI will send this (e.g., 2024)

class NoteCreate(BaseModel):
    title: str
    content: str
    date: datetime  # User must provide this field
    category_name: Optional[str] = None 
    note_id: Optional[str] = None