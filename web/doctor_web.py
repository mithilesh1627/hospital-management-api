from fastapi import APIRouter,Path,Body
from service import doctor_service as service
from typing import Optional,List,Dict,Any
from model.doctor_model import Doctor,DoctorBase
doctor_router = APIRouter(prefix="/doctors",tags=["Doctors"])

@doctor_router.get("/",status_code=200,description="Get the details of all doctor ")
async def get_all() -> List[dict]:
    return await service.get_all()

@doctor_router.get("/{id}",status_code=200,description="Get the details of doctor by id ")
async def get_by_id(id: str=Path(...,description="id of doctor",example=['68c646e649e67bf03e2f274b'])) -> Optional[Doctor]:
    return await service.get_by_id(id)

@doctor_router.post("/create-new",status_code=201,description="Add new doctor using this endpoint")
async def create_doctor(doctor: DoctorBase=Body(...)) -> dict:
    return await service.create_doctor(doctor)

@doctor_router.put("/update/{id}",status_code=202,description="Update the details of doctor using id")
async def update_doctor_by_id(id: str=Path(...), update_data: dict=Body(...)) -> dict:
    return await service.update_doctor_by_id(id,update_data)

@doctor_router.put("/update",status_code=202,description="Update the details of doctors")
async def update_patient(filter: dict=Body(...),update_data: dict=Body(...),multiple_update: bool = False) -> Dict[str, Any]:
    return await service.update_doctor(filter, update_data, multiple_update)

@doctor_router.delete(path="/delete/{id}",status_code=200,description="delete the doctor by id")
async def delete_doctor_by_id(id: str=Path(...,)) -> dict:
   return await service.delete_doctor_by_id(id)