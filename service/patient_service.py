from model.patient_model import Patients, PatientsBase
import data.patient_data as data
from typing import List, Any

async def get_by_id(id: str) -> Patients | None:
    return await data.get_by_id(id)

async def get_all() -> List[Patients]:
    return await data.get_all()

async def create_patient(patient: PatientsBase) -> dict:
    return await data.create_patient(patient)

async def update_patient_by_id(id: str, update_data: dict) -> dict:
    return await data.update_patient_by_id(id, update_data)

async def update_patients(filter: dict,update_data: dict,multiple_update: bool = False) -> dict[str, Any] | None:
    return await data.update_patient(filter, update_data, multiple_update)

async def delete_patient(id: str) -> dict:
    return await data.delete_patient_by_id(id)
