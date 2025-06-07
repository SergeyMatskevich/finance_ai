from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.models import User
from app.schemas.user import UserCreate, User as UserSchema, UserUpdate, UserAppleCreate
from app.db.database import get_db
from app.core.security import get_password_hash, verify_password
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким email
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Проверяем, существует ли пользователь с таким apple_id
    if user.apple_id:
        db_user = db.query(User).filter(User.apple_id == user.apple_id).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apple ID already registered"
            )
    
    # Создаем нового пользователя
    hashed_password = get_password_hash(user.password) if user.password else None
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role,
        apple_id=user.apple_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/apple", response_model=UserSchema)
def create_apple_user(user: UserAppleCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким apple_id
    db_user = db.query(User).filter(User.apple_id == user.apple_id).first()
    if db_user:
        return db_user
    
    # Проверяем, существует ли пользователь с таким email
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        # Если пользователь существует, обновляем его apple_id
        db_user.apple_id = user.apple_id
        db.commit()
        db.refresh(db_user)
        return db_user
    
    # Создаем нового пользователя
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        apple_id=user.apple_id,
        hashed_password=None  # Для Apple auth пароль не нужен
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.email:
        current_user.email = user_update.email
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users 