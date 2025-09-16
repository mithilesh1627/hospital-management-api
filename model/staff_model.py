from pydantic import BaseModel, Field, EmailStr
from auth.auth_role import Role
from datetime import datetime, timezone
from typing import Optional
from functools import partial

class StaffBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=25)
    email: EmailStr
    phone: int = Field(..., description="10 digit contact number", ge=1000000000, le=9999999999)
    role: str = Role.STAFF
    shift: str = Field(..., min_length=2, max_length=20)

class StaffCreate(StaffBase):
    password: str = Field(..., min_length=6)

class Staff(StaffBase):
    id: str = Field(...)
    user_id: Optional[str] = Field(None, description="Linked user ID")
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
    updated_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
