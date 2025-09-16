from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from datetime import date, datetime, timezone
from typing import Optional
from functools import partial

class PatientsBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=20, description="Name of patient")
    city: str = Field(..., min_length=2, max_length=20, description="City name of patient")
    age: int = Field(..., gt=0, le=120, description="Age should be between 0 and 120")
    gender: str = Field(..., pattern="^(male|female|other)$", description="Gender of the patient")
    height_m: float = Field(..., gt=0, description="Height in meters")
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms")
    email: EmailStr = Field(..., description="Valid email address of the patient")
    phone: int = Field(..., description="10 digit contact number", ge=1000000000, le=9999999999)
    dob: date = Field(..., description="Date of birth of the patient")
    address: str = Field(..., min_length=5, max_length=200, description="Residential address")
    emergency_contact: int = Field(..., description="10 digit emergency contact number", ge=1000000000, le=9999999999)
    created_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc), description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=partial(datetime.now, timezone.utc), description="Record update timestamp")

    bmi: float | None = Field(default=None, exclude=True)
    verdict: str | None = Field(default=None, exclude=True)

    @field_validator("bmi", mode="after")
    def calculate_bmi(cls, v, values):
        """Calculate BMI if height and weight are provided"""
        height = values.get("height_m")
        weight = values.get("weight_kg")
        if height and weight and height > 0:
            return round(weight / (height ** 2), 2)
        return None

    @field_validator("verdict", mode="after")
    def calculate_verdict(cls, v, values):
        """Give health verdict based on BMI"""
        bmi = values.get("bmi")
        if bmi is None:
            return None
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    model_config = ConfigDict(extra="ignore")  # Ignore unexpected fields in input


class Patients(PatientsBase):
    id: str = Field(..., description="Unique ID of the patient")


class UpdatePatientsRequest(BaseModel):
    filter_data: dict
    update_data: dict
    multi_update: Optional[bool] = False
