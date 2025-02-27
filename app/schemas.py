from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from typing import Optional, Any

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    username: Optional[str] = None  # Make username optional

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    is_active: bool
    role: str
    created_at: datetime

class Config:
    from_attributes = True

class StandardResponse(BaseModel):
    isSuccess: bool  # Indicates success or failure
    messages: List[str] = []  # List of success messages
    errors: List[str] = []  # List of error messages
    data: Optional[Any] = None  # Response data
    status_code: int  # HTTP status code
class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True