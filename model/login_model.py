from pydantic import BaseModel,field_validator, EmailStr, Field
import re
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

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

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_at: str
