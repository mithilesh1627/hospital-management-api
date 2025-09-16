from fastapi import APIRouter, Path, Body, Depends, HTTPException
from typing import List, Dict, Any
from auth.auth_handler import role_required, get_current_user
from auth.auth_role import Role
from model.appointment_model import AppointmentBase, Appointment
import service.appointment_service as service

appointment_router = APIRouter(prefix="/appointments", tags=["Appointments"])

# Create appointment (Patient, Admin)
@appointment_router.post("/create", response_model=Dict[str, Any], summary="Create a new appointment")
async def create_appointment(appointment: AppointmentBase, user: Dict[str, Any] = Depends(role_required([Role.PATIENT, Role.ADMIN]))):
    return await service.create_appointment(appointment)

# Get all appointments (Admin/Staff/Doctor)
@appointment_router.get("/", response_model=List[Appointment], summary="Get all appointments")
async def get_all(user: Dict[str, Any] = Depends(role_required([Role.ADMIN, Role.STAFF, Role.DOCTOR]))):
    return await service.get_all()

# Get appointment by ID (Patient, Doctor, Admin)
@appointment_router.get("/{id}", response_model=Appointment, summary="Get appointment by ID")
async def get_by_id(id: str = Path(...), user: Dict[str, Any] = Depends(get_current_user)):
    return await service.get_by_id(id)

# Update appointment (Admin, Staff)
@appointment_router.put("/update/{id}", summary="Update appointment by ID")
async def update_appointment(id: str, update_data: dict = Body(...), user: Dict[str, Any] = Depends(role_required([Role.ADMIN, Role.STAFF]))):
    return await service.update_appointment_by_id(id, update_data)

# Delete appointment (Admin only)
@appointment_router.delete("/delete/{id}", summary="Delete appointment by ID")
async def delete_appointment(id: str, user: Dict[str, Any] = Depends(role_required([Role.ADMIN]))):
    return await service.delete_appointment(id)
