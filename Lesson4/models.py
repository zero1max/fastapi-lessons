from pydantic import BaseModel

class User(BaseModel):
    id: int | None = None  
    fullname: str
    username: str
    email: str
    password: str