from typing import List, Dict, Any
from model.appointment_model import AppointmentBase, Appointment
import data.appointment_data as data

async def create_appointment(appointment: AppointmentBase) -> Dict[str, Any]:
    return await data.create_appointment(appointment)

async def get_by_id(id: str) -> Dict[str, Any]:
    return await data.get_by_id(id)

async def get_all() -> List[Appointment]:
    return await data.get_all()

async def update_appointment_by_id(id: str, update_data: dict) -> Dict[str, Any]:
    return await data.update_appointment_by_id(id, update_data)

async def delete_appointment(id: str) -> Dict[str, Any]:
    return await data.delete_appointment_by_id(id)
