from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import asyncpg

from models import UserCreate, UserUpdate, UserResponse, BaseResponse
from db import Database, DatabaseError
from dependencies import get_db

class UserCreate(BaseModel):
    full_name: str
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: str

class BaseResponse(BaseModel):
    message: str
    data: Optional[UserResponse] = None

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Database = Depends(get_db)):
    """Create a new user"""
    try:
        result = await db.add(
            full_name=user.full_name,
            username=user.username,
            email=user.email,
            password=user.password
        )
        return result
    except asyncpg.UniqueViolationError:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[UserResponse])
async def get_users(db: Database = Depends(get_db)):
    """Get all users"""
    try:
        return await db.all()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/{user_id}", response_model=UserResponse)
# async def get_user(user_id: int, db: Database = Depends(get_db)):
#     """Get user by ID"""
#     try:
#         user = await db.get_by_id(user_id)
#         if not user:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"User with ID {user_id} not found"
#             )
#         return user
#     except DatabaseError as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Database = Depends(get_db)
):
    """Update user information by ID"""
    try:
        result = await db.update(
            user_id=user_id,
            full_name=user_update.full_name,
            email=user_update.email,
            password=user_update.password
        )
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"User with ID {user_id} not found"
            )
        return result
    except asyncpg.UniqueViolationError:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}", response_model=BaseResponse)
async def delete_user(user_id: int, db: Database = Depends(get_db)):
    """Delete a user by ID"""
    try:
        result = await db.delete(user_id)
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"User with ID {user_id} not found"
            )
        return BaseResponse(message=f"User with ID {user_id} successfully deleted")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))