from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class User(UserCreate):
    id: int

users = []
next_id = 1  

@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    global next_id
    new_user = User(id=next_id, **user.dict())
    next_id += 1
    users.append(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: UserCreate):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = User(id=user_id, **updated_user.dict())
            return users[index]
    raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            del users[index]
            return {"message": "Foydalanuvchi o'chirildi"}
    raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")