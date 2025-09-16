from pydantic import BaseModel, EmailStr, Field, validator, field_validator
from typing import Optional
from datetime import datetime
from auth.auth_role import Role
import re

class UserBase(BaseModel):
    email: EmailStr
    role: Role
    linked_id: Optional[str] = None  # MongoDB ObjectId of patient/doctor/staff

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128,description="Strong password(password has at least 1 uppercase, 1 lowercase, 1 digit, 1 special char)")

    @field_validator('password')
    def password_strength(cls, v):
        """Ensure password has at least 1 uppercase, 1 lowercase, 1 digit, 1 special char"""
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    role: Optional[Role]
    linked_id: Optional[str]

    @validator('password')
    def password_strength(cls, v):
        if v is None:
            return v
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserOut(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
