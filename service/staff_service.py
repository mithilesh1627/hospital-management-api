from typing import List, Dict, Any
from model.staff_model import StaffBase, StaffCreate, Staff
import data.staff_data as data

async def create_staff(staff: StaffCreate) -> dict:
    return await data.create_staff(staff)

async def get_by_id(id: str) -> Dict[str, Any]:
    return await data.get_by_id(id)

async def get_all() -> List[Staff]:
    return await data.get_all()

async def update_staff_by_id(id: str, update_data: dict) -> dict:
    return await data.update_staff_by_id(id, update_data)

async def delete_staff(id: str) -> dict:
    return await data.delete_staff_by_id(id)
