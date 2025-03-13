from pydantic import BaseModel, Field
from typing import Optional, Any, List

class User(BaseModel):
    id: Optional[int] = None  
    fullname: str
    username: str
    email: str
    password: str = Field(..., exclude=True)  # Parolni himoya qilish

class BaseResponseModel(BaseModel):
    success: bool
    data: Optional[Any] = None
    errors: Optional[List[dict]] = None
