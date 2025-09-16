from fastapi import APIRouter, HTTPException,Body,Path
from typing import List
from model.staff_model import Staff, StaffBase
from service import staff_service as staff_service

staff_router = APIRouter(prefix="/staffs", tags=["Staffs"])


@staff_router.post("/new-staff", response_model=dict)
async def create_staff(staff: StaffBase=Body(...)):
    return await staff_service.create_staff(staff)


@staff_router.get("/", response_model=List[dict])
async def get_all_staff():
    return await staff_service.get_all_staff()


@staff_router.get("/{staff_id}", response_model=Staff)
async def get_staff_by_id(staff_id: str=Path(...,description="get detail of staff using MongoID")):
    staff = await staff_service.get_staff_by_id(staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff


@staff_router.put("/update/{staff_id}", response_model=dict)
async def update_staff_by_id(staff_id: str=Path(...,description="update the data using MongoID"),
                             update_data: dict=Body(...)):
    return await staff_service.update_staff(staff_id, update_data)

@staff_router.put("/update/", response_model=dict)
async def update_staff(filter: dict=Body(...,description="Enter the filter condition for update")
                       ,update_data: dict=Body(...,description="enter the data for update")
                       ,multiple_update: bool = False):
    return await staff_service.update_staff(filter, update_data, multiple_update)


@staff_router.delete("/delete/{staff_id}", response_model=dict)
async def delete_staff(staff_id: str=Path(...,description="Remove the staff using MongoID")):
    return await staff_service.delete_staff(staff_id)
