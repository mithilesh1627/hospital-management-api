from typing import List, Dict, Any
from model.doctor_model import DoctorBase, DoctorCreate, Doctor
import data.doctor_data as data

async def create_doctor(doctor: DoctorCreate) -> dict:
    return await data.create_doctor(doctor)

async def get_by_id(id: str) -> Dict[str, Any]:
    return await data.get_by_id(id)

async def get_all() -> List[Doctor]:
    return await data.get_all()

async def update_doctor_by_id(id: str, update_data: dict) -> dict:
    return await data.update_doctor_by_id(id, update_data)

async def delete_doctor(id: str) -> dict:
    return await data.delete_doctor_by_id(id)
