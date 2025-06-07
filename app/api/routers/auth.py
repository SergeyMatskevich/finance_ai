from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

from app.core.security import create_access_token, verify_password
from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.models import User
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

class AppleLoginRequest(BaseModel):
    apple_id: str
    email: str
    full_name: Optional[str] = None

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/apple", response_model=Token)
async def login_with_apple(
    request: AppleLoginRequest,
    db: Session = Depends(get_db)
):
    # Проверяем, существует ли пользователь с таким apple_id
    user = db.query(User).filter(User.apple_id == request.apple_id).first()
    
    if not user:
        # Если пользователя с таким apple_id нет, ищем по email
        user = db.query(User).filter(User.email == request.email).first()
        if user:
            # Если пользователь с таким email есть, но apple_id не установлен — обновляем его
            if not user.apple_id:
                user.apple_id = request.apple_id
                db.commit()
                db.refresh(user)
        else:
            # Если пользователя нет вообще — создаём
            user = User(
                email=request.email,
                apple_id=request.apple_id,
                full_name=request.full_name or request.email.split('@')[0],
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user 