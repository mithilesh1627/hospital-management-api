from typing import List, Optional, Dict, Any
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from data.init import doctors_coll
from model.doctor_model import Doctor, DoctorBase

def dict_to_model(doc: dict) -> Doctor:
    return Doctor(
        id=str(doc["_id"]),
        name=doc["name"],
        specialization=doc["specialization"],
        experience_years=doc["experience_years"],
        city=doc["city"],
        gender=doc["gender"],
        contact=doc["contact"]
    )

async def get_all() -> List[dict]:
    doctors: List[dict] = []
    cursor = doctors_coll.find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doctors.append(doc)
    return doctors

async def get_by_id(id: str) -> Optional[Doctor]:
    try:
        doc = await doctors_coll.find_one({"_id": ObjectId(id)})
        if doc:
            return dict_to_model(doc)
    except InvalidId:
        return None
    return None

async def create_doctor(doctor: DoctorBase) -> dict:
    insert = await doctors_coll.insert_one(doctor.model_dump())
    return {"message": "Doctor add to DB", "_id": str(insert.inserted_id)}

async def update_doctor_by_id(id: str, update_data: dict) -> dict:
    try:
        result = await doctors_coll.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid doctor ID format")

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {
        "message": "Doctor updated successfully",
        "matched_count": result.matched_count,
        "modified_count": result.modified_count
    }

async def delete_doctor_by_id(id: str) -> dict:
    try:
        result = await doctors_coll.delete_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid doctor ID format")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {
        "message": "Doctor deleted successfully",
        "deleted_count": result.deleted_count,
        "_id": id
    }

async def update_doctor(filter: dict,update_data: dict,multiple_update: bool = False) -> Dict[str, Any]:
    if multiple_update:
        rec = await doctors_coll.update_many(filter, {"$set": update_data})
    else:
        rec = await doctors_coll.update_one(filter, {"$set": update_data})

    if not rec.acknowledged:
        return {"message": "Update operation not acknowledged by MongoDB"}

    if rec.matched_count == 0:
        return {
            "message": "No records matched the filter",
            "matched_count": 0,
            "modified_count": 0
        }

    if multiple_update:
        docs = await doctors_coll.find(filter).to_list(length=100)
    else:
        docs = await doctors_coll.find(filter).to_list(length=1)

    #
    updated_docs = [dict_to_model(doc).model_dump() for doc in docs]

    return {
        "message": "Record(s) updated successfully",
        "matched_count": rec.matched_count,
        "modified_count": rec.modified_count,
        "updated_records": updated_docs
    }
