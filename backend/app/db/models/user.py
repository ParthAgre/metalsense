from sqlalchemy import Boolean, Column, Integer, String, Enum
from app.db.base_class import Base
import enum

class UserRole(str, enum.Enum):
    citizen = "citizen"
    researcher = "researcher"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.citizen, nullable=False)
    is_active = Column(Boolean, default=True)
