from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.user import UserLogin, UserCreate
from app.schemas.token import Token, TokenPayload
from app.schemas.msg import Msg
from app.db.models.user import User
from pydantic import EmailStr

router = APIRouter()

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(deps.get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh-token", response_model=Token)
def refresh_token(
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Refresh access token.
    For simplicity in this implementation, we just issue a new access token
    if the user is currently authenticated with a valid token.
    In a more complex implementation, you'd use a separate refresh token.
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/password-recovery/{email}", response_model=Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)):
    """
    Password Recovery.
    """
    user = db.query(User).filter(User.email == email).first()

    if not user:
        # We don't want to reveal if the user exists or not
        return {"msg": "If this email exists, a password reset email has been sent."}

    password_reset_token = security.create_access_token(
        data={"sub": email}, expires_delta=timedelta(hours=1)
    )
    
    # In a real app, send email here.
    # For now, we print it to console for testing.
    print(f"PASSWORD RESET TOKEN FOR {email}: {password_reset_token}")
    
    return {"msg": "If this email exists, a password reset email has been sent."}

@router.post("/reset-password", response_model=Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
):
    """
    Reset password
    """
    email = security.verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    hashed_password = security.get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    
    return {"msg": "Password updated successfully"}

@router.post("/logout", response_model=Msg)
def logout():
    """
    Logout. 
    Since we use stateless JWTs, this is mostly a client-side action (deleting the token).
    We provide this endpoint for completeness or future server-side blacklisting.
    """
    return {"msg": "Successfully logged out"}
