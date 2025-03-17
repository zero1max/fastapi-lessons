from fastapi import APIRouter, HTTPException
from db import Database
from models import User, BaseResponse
from config import DB_URL

router = APIRouter(prefix="/api/users", tags=["Users"])
db = Database(DB_URL)

@router.post("/", response_model=BaseResponse)
async def create_user(user: User):
    """Yangi foydalanuvchi qo'shish"""
    try:
        result = await db.add(user)
        return BaseResponse(message="Foydalanuvchi muvaffaqiyatli qo'shildi", data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[User])
async def get_users():
    """Barcha foydalanuvchilarni olish"""
    try:
        users = await db.all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{username}", response_model=BaseResponse)
async def update_user(username: str, new_data: User):
    """Foydalanuvchini yangilash"""
    try:
        result = await db.update(username, new_data)
        return BaseResponse(message="Foydalanuvchi muvaffaqiyatli yangilandi", data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{username}", response_model=BaseResponse)
async def delete_user(username: str):
    """Foydalanuvchini o'chirish"""
    try:
        result = await db.delete(username)
        return BaseResponse(message="Foydalanuvchi muvaffaqiyatli o'chirildi", data=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))