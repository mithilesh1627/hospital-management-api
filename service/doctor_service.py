from typing import List,Optional,Dict,Any
import data.doctor_data as data
from model.doctor_model import DoctorBase,Doctor

async def get_all() -> List[dict]:
    return await data.get_all()

async def get_by_id(id: str) -> Optional[Doctor]:
    return await data.get_by_id(id)

async def create_doctor(doctor: DoctorBase) -> dict:
    return await data.create_doctor(doctor)

async def update_doctor_by_id(id: str, update_data: dict) -> dict:
    return await data.update_doctor_by_id(id,update_data)

async def update_doctor(filter: dict,update_data: dict,multiple_update: bool = False) -> Dict[str, Any]:
    return await data.update_doctor(filter, update_data, multiple_update)

async def delete_doctor_by_id(id: str) -> dict:
   return await data.delete_doctor_by_id(id)