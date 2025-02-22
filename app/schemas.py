from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional, Any

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

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
    success: bool
    message: str
    status_code: int
    data: Optional[Any] = None