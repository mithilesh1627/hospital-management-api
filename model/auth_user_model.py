from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal, Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    email: EmailStr
    role: Literal["admin", "doctor", "staff", "patient"] = "patient"

class UserCreate(UserBase):
    password: str = Field(..., min_length=8,
                          description="password should contain 8 chars,and must include 1 uppercase letter,1 lowercase letter,1 digit and 1 special character")

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """Validate password strength with detailed error messages."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must contain at least one special character.")
        return v
class UserInDB(UserBase):
    _id: str

class UserResponse(UserBase):
    _id: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime

class TokenData(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
