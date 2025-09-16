from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from functools import partial
from auth.auth_role import Role

class AppointmentBase(BaseModel):
    patient_id: str = Field(..., description="MongoDB ObjectId of the patient")
    doctor_id: str = Field(..., description="MongoDB ObjectId of the doctor")
    appointment_date: datetime = Field(..., description="Appointment date and time")
    reason: str = Field(..., min_length=2, max_length=255)
    appointment_type: str = Field(..., min_length=2, max_length=50)
    status: str = Field(default="scheduled", description="Appointment status")
    payment_status: str = Field(default="pending", description="Payment status")
    notes: Optional[str] = Field(None, description="Optional notes")

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: str = Field(...)
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
    updated_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc))
