from fastapi import APIRouter, Path, Body, Depends, HTTPException, status
from typing import Any, List, Dict

import service.patient_service as service
from model.patient_model import Patients, PatientsBase, UpdatePatientsRequest
from auth.auth_handler import role_required, get_current_user
from auth.auth_role import Role

patient_router = APIRouter(prefix="/patients", tags=["Patients"])


@patient_router.get("/me", summary="Get my patient profile")
async def get_my_profile(user: Dict[str, Any] = Depends(role_required([Role.PATIENT]))):
    patient = await service.get_by_id(user["id"])
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return patient


@patient_router.get("/{id}", status_code=200, summary="Get a patient by ID")
async def get_by_id(id: str = Path(...), user: Dict[str, Any] = Depends(get_current_user)):
    if user["role"] == Role.PATIENT and user["id"] != id:
        raise HTTPException(status_code=403, detail="Patients can only access their own records")
    elif user["role"] not in [Role.ADMIN, Role.PATIENT]:
        raise HTTPException(status_code=403, detail="Only patients (self) and admins can access patient data")

    patient = await service.get_by_id(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@patient_router.get("/", status_code=200, summary="Get all patients")
async def get_all(user: Dict[str, Any] = Depends(role_required([Role.ADMIN, Role.STAFF]))) -> List[Patients]:
    return await service.get_all()


@patient_router.post("/create_new", response_model=Dict[str, Any], status_code=201, summary="Create a new patient")
async def create_new(patient: PatientsBase, user: Dict[str, Any] = Depends(role_required([Role.ADMIN, Role.STAFF]))):
    return await service.create_patient(patient)


@patient_router.put("/update/{id}", status_code=200, summary="Update a patient by ID")
async def update_patient(id: str = Path(...), update_data: Dict[str, Any] = Body(...), user: Dict[str, Any] = Depends(get_current_user)):
    if user["role"] == Role.PATIENT and user["id"] != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this patient")
    return await service.update_patient_by_id(id, update_data)


@patient_router.put("/updates", status_code=200, summary="Update multiple patients")
async def update_patients(request: UpdatePatientsRequest, user: Dict[str, Any] = Depends(role_required([Role.ADMIN, Role.STAFF]))):
    return await service.update_patients(request.filter_data, request.update_data, request.multi_update)


@patient_router.delete("/delete/{id}", status_code=200, summary="Delete a patient by ID")
async def delete_patient(id: str = Path(...), user: Dict[str, Any] = Depends(role_required([Role.ADMIN]))):
    return await service.delete_patient(id)
