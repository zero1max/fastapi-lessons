from fastapi import FastAPI, HTTPException
from typing import List
from .models import User
from .database import Database

app = FastAPI()
db = Database()

# ------------------------------- POST --------------------------------
@app.post("/user/", response_model=User)
async def create_user(user: User):
    user_id = db.add_user(user.fullname, user.username, user.email, user.password)
    return {**user.dict(), "id": user_id}

# ------------------------------- GET --------------------------------
@app.get("/users/", response_model=List[User])
async def read_users():
    users = db.get_all_users()
    return [{"id": u[0], "fullname": u[1], "username": u[2], "email": u[3], "password": u[4]} for u in users]

# ------------------------------- PUT --------------------------------
@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    existing_user = db.get_user(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.update_user(user_id, user.fullname, user.username, user.email, user.password)
    return {**user.dict(), "id": user_id}

# ------------------------------- Delete --------------------------------
@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    existing_user = db.get_user(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete_user(user_id)
    return {"detail": "User deleted"}
