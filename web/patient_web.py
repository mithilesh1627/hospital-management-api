from fastapi import APIRouter, Query, HTTPException, Path, Body
from service import patient_service as service
from typing import Any
from model.patient_model import Patients,PatientsBase,UpdatePatientsRequest

patient_router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@patient_router.get("/", status_code=200,
                    summary="Get all patients")
async def get_all() -> list[Patients]:
    return await service.get_all()

@patient_router.get("/{id}", status_code=200,
                    summary="Get a patient by ID")
async def get_by_id(id: str = Path(..., description="MongoDB ID of the patient")) -> dict | None:
    patient = await service.get_by_id(id)
    if patient:
        return patient.model_dump()
    raise HTTPException(status_code=404, detail="Patient not found")

@patient_router.post("/create_new", response_model=dict, status_code=201, summary="Create a new patient")
async def create_new(patient: PatientsBase) -> dict:
    return await service.create_patient(patient)

@patient_router.put("/update/{id}", status_code=201, summary="Update a patient by ID")
async def update_patient(
    id: str = Path(..., description="MongoDB ID of the patient to update"),
    update_data: dict = Body(..., description="Fields to update")
) -> dict:
    return await service.update_patient_by_id(id=id, update_data=update_data)

@patient_router.put("/updates", status_code=201, summary="Update multiple patients")
async def update_patients(request: UpdatePatientsRequest) -> dict[str, Any] | None:
    return await service.update_patients(
        request.filter_data,
        request.update_data,
        request.multi_update
    )

@patient_router.delete("/delete/{id}", status_code=200, summary="Delete a patient by ID")
async def delete_patient(id: str = Path(..., description="MongoDB ID of the patient to delete")) -> dict:
    return await service.delete_patient(id)
