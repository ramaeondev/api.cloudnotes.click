from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional
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
    date: datetime # User must provide this field
class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    date: datetime
    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    """Schema for user details in the login response."""
    user_id: int
    user_ulid: str
    first_name: str
    last_name: str
    email: str
    access_token: str
    refresh_token: str

class LoginResponse(BaseModel):
    isSuccess: bool
    messages: List[str]
    errors: List[str]
    access_token: str
    token_type: str
    refresh_token: str
    data: Dict[str, UserSchema]  
    status_code: int
