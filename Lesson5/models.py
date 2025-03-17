from pydantic import BaseModel
from typing import Optional, Any, List

class BaseResponse(BaseModel):
    status: bool = True
    data: Optional[Any] = None
    errors: Optional[List[dict]] = None

class User(BaseModel):
    full_name: str
    username: str
    email: str
    password: str