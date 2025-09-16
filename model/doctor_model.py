from pydantic import BaseModel,Field

class DoctorBase(BaseModel):
    name:str=Field(...,min_length=2,max_length=25)
    specialization: str = Field(..., min_length=2, max_length=50)
    experience_years: int = Field(..., ge=0)
    city: str = Field(..., min_length=2, max_length=12)
    gender: str = Field(..., pattern="^(male|female|other)$")
    contact: int = Field(..., description="10 digit contact number", le=9999999999, ge=1000000000)

class Doctor(DoctorBase):
    id:str=Field(...)