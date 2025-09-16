from fastapi import APIRouter, Query, Path, Body
from typing import List
from service import appointment_service as service
from model.appointment_model import  Appointment, AppointmentBase

appointment_router = APIRouter(prefix="/appointments", tags=["Appointments"])

@appointment_router.post("/new-appointment",
                         status_code=201,
                         description="Create a new appointment"
                         )
async def create_appointment(appointment: AppointmentBase = Body(..., description="Appointment details")):
    return await service.create_appointment(appointment)

@appointment_router.get("/", description="Get all appointments")
async def get_all_appointments():
    return await service.get_all_appointments()

@appointment_router.get("/{appointment_id}",description="get the details of appointment using MongoID")
async def get_appointment(appointment_id: str=Path(...,description="get the details of appointment using MongoID")):
    return await service.get_appointment(appointment_id)

@appointment_router.get("/patient/{patient_id}",
                        description="Get all appointments of a patient using PatientID")
async def get_patient_appointments(patient_id: str = Path(..., description="Patient ID")):
    return await service.get_appointments_by_patient(patient_id)

@appointment_router.get("/assigned-doctor/{doctor_id}",
                        description="Doctor can check their assigned appointments")
async def get_doctor_appointments(doctor_id: str = Path(..., description="Doctor ID")):
    return await service.get_appointments_by_doctor(doctor_id)

@appointment_router.get("/{appointment_id}",description="Get details of an appointment using MongoID")
async def get_appointment(appointment_id: str = Path(...,pattern="^[0-9a-fA-F]{24}$",description="Mongo ObjectId (24 hex characters)")):
    return await service.get_appointment(appointment_id)

@appointment_router.put("/update/{appointment_id}",
                        description="Update an appointment using MongoID")
async def update_appointment_id(appointment_id: str = Path(..., description="Mongo ObjectId"),
                             update_data: dict = Body(..., description="Updated fields")):
    return await service.update_appointment_by_id(appointment_id, update_data)

@appointment_router.put("/update/",
                        description="Updates an appointment ")
async def update_appointment(filter_:dict,update_:dict,multiple_update:bool=False):
    return await service.update_appointment(filter_,update_,multiple_update)

@appointment_router.patch("/cancel-appointment/{appointment_id}",
                          description="Cancel an appointment using MongoID")
async def cancel_appointment(appointment_id: str = Path(..., description="Mongo ObjectId")):
    return await service.cancel_appointment(appointment_id)

@appointment_router.delete("/delete/{appointment_id}",
                           description="Delete an appointment using MongoID")
async def delete_appointment(appointment_id: str = Path(..., description="Mongo ObjectId")):
    return await service.delete_appointment_(appointment_id)