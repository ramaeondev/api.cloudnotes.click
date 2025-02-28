from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional
from datetime import datetime
from typing import Optional, Any
from datetime import date

class StandardResponse(BaseModel):
    isSuccess: bool  
    messages: List[str] = []
    errors: List[str] = []
    data: Optional[Any] = None
    status_code: int