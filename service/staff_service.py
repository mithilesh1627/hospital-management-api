from typing import List, Optional, Dict, Any
from model.staff_model import Staff, StaffBase
from data import staff_data as staff_data


async def create_staff(staff: StaffBase) -> dict:
    return await staff_data.create_staff(staff)

async def get_all_staff() -> List[dict]:
    return await staff_data.get_all()

async def get_staff_by_id(staff_id: str) -> Optional[Staff]:
    return await staff_data.get_by_id(staff_id)


async def update_staff_id(staff_id: str, update_data: dict) -> dict:
    return await staff_data.update_staff_by_id(staff_id, update_data)


async def delete_staff(staff_id: str) -> dict:
    return await staff_data.delete_staff_by_id(staff_id)

async def update_staff(filter_: dict,update_data: dict,multiple_update: bool = False) -> Dict[str, Any]:
    return await staff_data.update_staff(filter_,update_data,multiple_update)
