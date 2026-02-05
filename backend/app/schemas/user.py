from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.db.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.citizen
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str

