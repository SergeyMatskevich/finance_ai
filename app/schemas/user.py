from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.models import UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.MEMBER

class UserCreate(UserBase):
    password: str
    apple_id: Optional[str] = None

class UserAppleCreate(BaseModel):
    apple_id: str
    email: EmailStr
    full_name: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    apple_id: Optional[str] = None

    class Config:
        orm_mode = True

class User(UserInDB):
    pass

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime
    apple_id: Optional[str] = None

    class Config:
        from_attributes = True 