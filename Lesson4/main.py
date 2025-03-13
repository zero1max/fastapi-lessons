from fastapi import FastAPI, HTTPException
from typing import List
from .models import User, BaseResponseModel
from .database import Database

app = FastAPI()
db = Database()

# ------------------------------- POST --------------------------------
@app.post("/user/")
async def create_user(user: User):
    user_id = db.add_user(user.fullname, user.username, user.email, user.password)
    user_data = user.dict()
    user_data["id"] = user_id
    return BaseResponseModel(success=True, data=user_data)

# ------------------------------- GET --------------------------------
@app.get("/users/")
async def read_users():
    users = db.get_all_users()
    user_list = [
        {"id": u[0], "fullname": u[1], "username": u[2], "email": u[3], "password": u[4]}
        for u in users
    ]
    return BaseResponseModel(success=True, data=user_list)

# ------------------------------- PUT --------------------------------
@app.put("/user/{user_id}")
async def update_user(user_id: int, user: User):
    existing_user = db.get_user(user_id)
    if not existing_user:
        return BaseResponseModel(success=False, errors=[{"message": "User not found"}])

    db.update_user(user_id, user.fullname, user.username, user.email, user.password)
    return BaseResponseModel(success=True, data={**user.dict(), "id": user_id})

# ------------------------------- Delete --------------------------------
@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    existing_user = db.get_user(user_id)
    if not existing_user:
        return BaseResponseModel(success=False, errors=[{"message": "User not found"}])
    
    db.delete_user(user_id)
    return BaseResponseModel(success=True, data={"message": "User deleted"})
