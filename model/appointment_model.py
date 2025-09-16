from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class AppointmentBase(BaseModel):
    patient_id: str = Field(..., description="MongoDB ObjectId of patient as string")
    doctor_id: str = Field(..., description="MongoDB ObjectId of doctor as string")
    appointment_date: datetime = Field(..., description="Date & time of appointment")
    reason: str = Field(..., min_length=5, max_length=100)
    status: Literal["scheduled", "completed", "cancelled"] = Field(default="scheduled")
    appointment_type: Literal["in_person", "online"] = Field(default="in_person")
    payment_status: Literal["pending", "paid", "refunded"] = Field(default="pending")
    notes: Optional[str] = Field(None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class Appointment(AppointmentBase):
    iid: str = Field(..., alias="id")

    class Config:
        populate_by_name = True
