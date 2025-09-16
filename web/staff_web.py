from fastapi import APIRouter, Path, Body, Depends, HTTPException
from typing import List, Dict, Any
from auth.auth_handler import role_required, get_current_user
from auth.auth_role import Role
from model.staff_model import StaffBase, StaffCreate, Staff

import service.staff_service as service

staff_router = APIRouter(prefix="/staff", tags=["Staff"])

# Create staff (Admin only)
@staff_router.post("/create", response_model=Dict[str, Any], summary="Create new staff")
async def create_staff(staff: StaffCreate, user: Dict[str, Any] = Depends(role_required([Role.ADMIN]))):
    return await service.create_staff(staff)

# Get all staff (Admin only)
@staff_router.get("/", response_model=List[Staff], summary="Get all staff")
async def get_all(user: Dict[str, Any] = Depends(role_required([Role.ADMIN]))):
    return await service.get_all()

# Get staff by ID (Admin only)
@staff_router.get("/{id}", response_model=Staff, summary="Get staff by ID")
async def get_by_id(id: str = Path(...), user: Dict[str, Any] = Depends(role_required([Role.ADMIN]))):
    return await service.get_by_id(id)

# Update staff (Admin only)
@staff_router.put("/update/{id}", summary="Update staff by ID")
async def update_staff(id: str, update_data: dict = Body(...), user: Dict[str, Any] = Depends(role_required([Role.ADMIN]))):
    return await service.update_staff_by_id(id, update_data)

# Delete staff (Admin only)
@staff_router.delete("/delete/{id}", summary="Delete staff by ID")
async def delete_staff(id: str, user: Dict[str, Any] = Depends(role_required([Role.ADMIN]))):
    return await service.delete_staff(id)
