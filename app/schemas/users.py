from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional
from datetime import datetime
from typing import Optional, Any
from datetime import date

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    user_ulid: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    
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