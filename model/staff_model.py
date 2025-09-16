from pydantic import BaseModel, Field
from typing import Literal

class StaffBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=20, description="Staff name")
    role: Literal["nurse", "receptionist", "lab_technician", "pharmacist", "janitor"] = Field(..., description="Staff role")
    shift: Literal["morning", "evening", "night"] = Field(..., description="Shift timing")
    salary: float = Field(..., ge=0, description="Monthly salary")
    contact: int = Field(
        ...,
        description="10 digit contact number",
        le=9999999999,
        ge=1000000000
    )
    city: str = Field(..., min_length=2, max_length=12, description="City of staff")

class Staff(StaffBase):
    id: str | None = Field(default=None, description="MongoDB ID")
