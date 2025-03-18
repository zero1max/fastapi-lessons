from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, Field

class UserBase(BaseModel):
    """Base user model with common fields"""
    full_name: constr(min_length=2, max_length=50) = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email address")

class UserCreate(UserBase):
    """Model for creating a new user"""
    username: constr(min_length=3, max_length=20, pattern="^[a-zA-Z0-9_-]+$") = Field(
        ..., 
        description="Username (alphanumeric with underscore and hyphen)"
    )
    password: constr(min_length=8, max_length=64) = Field(
        ..., 
        description="Password (minimum 8 characters)"
    )

class UserUpdate(BaseModel):
    """Model for updating user information"""
    full_name: Optional[constr(min_length=2, max_length=50)] = Field(
        None, 
        description="User's full name"
    )
    email: Optional[EmailStr] = Field(None, description="User's email address")
    password: Optional[constr(min_length=8, max_length=64)] = Field(
        None, 
        description="New password (minimum 8 characters)"
    )

class UserResponse(UserBase):
    """Model for user response data"""
    id: int = Field(..., description="User's unique identifier")
    username: str = Field(..., description="Username")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BaseResponse(BaseModel):
    """Base response model"""
    message: str = Field(..., description="Response message")
    data: Optional[UserResponse] = Field(None, description="Response data")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful",
                "data": None
            }
        }