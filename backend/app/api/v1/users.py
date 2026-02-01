from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core import security
from app.schemas.user import UserCreate, UserRead, UserBase
from app.db.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(deps.get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = security.get_password_hash(user.password)
    # Default role is already citizen in model, but we respect what is passed?
    # Security: For now, we allow passing role. In real app, only admin might set role or default to citizen.
    # We will assume new users are citizens unless specified (if we want to allow researcher signup, we should be careful).
    # For this implementation, we allow open signup.
    new_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role, 
        is_active=user.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(deps.get_current_active_user)):
    return current_user
