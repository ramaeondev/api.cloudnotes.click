from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional
from datetime import datetime
from typing import Optional, Any
from datetime import date

from app.schemas.users import UserSchema

class LoginResponse(BaseModel):
    isSuccess: bool
    messages: List[str]
    errors: List[str]
    access_token: str
    token_type: str
    refresh_token: str
    data: Dict[str, UserSchema]  
    status_code: int