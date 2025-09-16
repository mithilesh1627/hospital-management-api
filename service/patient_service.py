from model.patient_model import Patients, PatientsBase
import data.patient_data as data
from typing import List, Dict, Any, Union

async def get_by_id(_id: str) -> Union[Dict[str, Any], Patients]:
    return await data.get_by_id(_id)

async def get_all() -> List[Patients]:
    return await data.get_all()

async def create_patient(patient: PatientsBase) -> Dict[str, Any]:
    return await data.create_patient(patient)

async def update_patient_by_id(id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    return await data.update_patient_by_id(id, update_data)

async def update_patients(filter_: Dict[str, Any], update_data: Dict[str, Any], multiple_update: bool = False) -> Dict[str, Any]:
    return await data.update_patient(filter_, update_data, multiple_update)

async def delete_patient(id_: str) -> Dict[str, Any]:
    return await data.delete_patient_by_id(id_)
