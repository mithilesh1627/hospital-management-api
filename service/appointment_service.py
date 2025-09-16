import data.appointment_data as data
from typing import List, Optional, Any, Dict, Coroutine
from datetime import datetime,timezone
from bson import ObjectId
from model.appointment_model import Appointment,AppointmentBase

async def create_appointment(appointment: AppointmentBase) -> dict:
    if appointment.appointment_date < datetime.now(timezone.utc):
        raise ValueError("Appointment date cannot be in the past")
    return await data.create_appointment(appointment)

async def get_appointment(appointment_id: str) -> Optional[Appointment]:
    return await data.get_appointment(appointment_id)

async def get_all_appointments() -> List[dict]:
    return await data.get_all_appointments()

async def get_appointments_by_patient(patient_id: str) -> Appointment | None:
    return await data.get_by_patient(patient_id)

async def get_appointments_by_doctor(doctor_id: str) -> List[Appointment]:
    return await data.get_by_doctor(doctor_id)

async def get_upcoming_appointments(patient_id: str = None, doctor_id: str = None)-> List[Appointment]:
    return await data.get_upcoming_appointments(patient_id,doctor_id)

async def update_appointment_by_id(appointment_id: str, update_data: dict) -> dict:
    if "appointment_date" in update_data:
        if update_data["appointment_date"] < datetime.now(timezone.utc):
            raise ValueError("Updated appointment date cannot be in the past")
    return await data.update_appointment_by_id(appointment_id, update_data)

async def delete_appointment_(appointment_id: str) -> dict:
    return await data.delete_appointment(appointment_id)

async def cancel_appointment(appointment_id: str) ->  Dict[str, Any]:
        return await data.update_appointment({"id": ObjectId(appointment_id)},{"status": "cancelled"},False)

async def update_appointment(filter_: dict,update_data: dict,multiple_update: bool = False) -> Dict[str, Any]:
    return await data.update_appointment(filter_,update_data,multiple_update)