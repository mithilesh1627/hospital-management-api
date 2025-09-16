from fastapi import APIRouter, Path, Body, Depends, HTTPException
from typing import Dict, Any, List
from auth.auth_handler import role_required, get_current_user
from auth.auth_role import Role
from model.doctor_model import DoctorBase, DoctorCreate, Doctor
import service.doctor_service as service

doctor_router = APIRouter(prefix="/doctors", tags=["Doctors"])

# Create a doctor (Admin only)
@doctor_router.post("/create", response_model=Dict[str, Any], summary="Create a new doctor")
async def create_doctor(doctor: DoctorCreate, user: Dict[str, Any] = Depends(role_required([Role.ADMIN]))):
    return await service.create_doctor(doctor)

# Get all doctors (Admin/Staff only)
@doctor_router.get("/", response_model=List[Doctor], summary="Get all doctors")
async def get_all(user: Dict[str, Any] = Depends(role_required([Role.ADMIN, Role.STAFF]))):
    return await service.get_all()

# Get doctor by ID (Admin/Staff or self)
@doctor_router.get("/{id}", response_model=Doctor, summary="Get doctor by ID")
async def get_by_id(id: str = Path(...), user: Dict[str, Any] = Depends(get_current_user)):
    if user["role"] == Role.DOCTOR and user["id"] != id:
        raise HTTPException(status_code=403, detail="Not authorized to view this doctor")
    return await service.get_by_id(id)

# Update doctor (Admin or self)
@doctor_router.put("/update/{id}", summary="Update doctor by ID")
async def update_doctor(id: str, update_data: dict = Body(...), user: Dict[str, Any] = Depends(get_current_user)):
    if user["role"] == Role.DOCTOR and user["id"] != id:
        raise HTTPException(status_code=403, detail="Not authorized to update this doctor")
    return await service.update_doctor_by_id(id, update_data)

# Delete doctor (Admin only)
@doctor_router.delete("/delete/{id}", summary="Delete doctor by ID")
async def delete_doctor(id: str, user: Dict[str, Any] = Depends(role_required([Role.ADMIN]))):
    return await service.delete_doctor(id)
