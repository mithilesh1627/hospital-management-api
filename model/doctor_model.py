from pydantic import BaseModel, Field, EmailStr
from auth.auth_role import Role
from typing import Literal, Optional
from datetime import datetime, timezone
from functools import partial

class DoctorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=25)
    email: EmailStr
    specialization: str = Field(..., min_length=2, max_length=50)
    experience_years: int = Field(..., ge=0)
    city: str = Field(..., min_length=2, max_length=12)
    gender: Literal["male", "female", "other"] = Field(..., description="Gender of the doctor")
    contact: int = Field(..., description="10 digit contact number", le=9999999999, ge=1000000000)
    role: str = Role.DOCTOR

class DoctorCreate(DoctorBase):
    password: str = Field(..., min_length=6)  # Password for user account

class Doctor(DoctorBase):
    id: str = Field(...)
    user_id: Optional[str] = Field(None, description="Linked user ID")
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
    updated_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
