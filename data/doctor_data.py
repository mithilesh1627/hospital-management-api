from data.init import doctors_coll, users_coll
from model.doctor_model import DoctorBase, DoctorCreate, Doctor
from auth.auth_handler import get_password_hash
from auth.auth_role import Role
from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Dict, Any
from fastapi import HTTPException
from datetime import datetime, timezone

def dict_to_model(doc: dict) -> Doctor:
    return Doctor(
        id=str(doc["_id"]),
        user_id=str(doc.get("user_id")) if doc.get("user_id") else None,
        name=doc["name"],
        email=doc["email"],
        specialization=doc["specialization"],
        experience_years=doc["experience_years"],
        city=doc.get("city", ""),
        gender=doc.get("gender", "other"),
        contact=doc["contact"],
        role=doc.get("role", Role.DOCTOR),
        created_at=doc.get("created_at", datetime.now(timezone.utc)),
        updated_at=doc.get("updated_at", datetime.now(timezone.utc))
    )

def model_to_dict(doctor: DoctorBase) -> dict:
    return doctor.model_dump(exclude_unset=True)

async def create_doctor(doctor: DoctorCreate) -> dict:
    # Create linked user account
    hashed_password = get_password_hash(doctor.password)
    user_doc = {
        "email": doctor.email,
        "password": hashed_password,
        "role": Role.DOCTOR,
        "linked_id": None,  # placeholder, will set after doctor insert
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    user_insert = await users_coll.insert_one(user_doc)

    # Create doctor document and link user_id
    doctor_dict = model_to_dict(doctor)
    doctor_dict["user_id"] = str(user_insert.inserted_id)
    doctor_dict["created_at"] = datetime.now(timezone.utc)
    doctor_dict["updated_at"] = datetime.now(timezone.utc)
    doctor_insert = await doctors_coll.insert_one(doctor_dict)

    # Update user linked_id to point to doctor
    await users_coll.update_one({"_id": user_insert.inserted_id}, {"$set": {"linked_id": doctor_insert.inserted_id}})

    return {"message": "Doctor created with linked user", "doctor_id": str(doctor_insert.inserted_id), "user_id": str(user_insert.inserted_id)}

async def get_by_id(_id: str) -> Dict[str, Any]:
    try:
        doc = await doctors_coll.find_one({"_id": ObjectId(_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return dict_to_model(doc).model_dump()
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid doctor ID")

async def get_all() -> List[Doctor]:
    doctors: List[Doctor] = []
    cursor = doctors_coll.find({})
    async for doc in cursor:
        doctors.append(dict_to_model(doc))
    return doctors

async def update_doctor_by_id(id: str, update_data: dict) -> dict:
    result = await doctors_coll.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if not result.acknowledged:
        return {"message": "Update operation not acknowledged by MongoDB"}
    if result.matched_count == 0:
        return {"message": "No records matched the filter", "matched_count": 0, "modified_count": 0}
    return {"message": "Doctor updated successfully", "matched_count": result.matched_count, "modified_count": result.modified_count}

async def delete_doctor_by_id(_id: str) -> dict:
    try:
        result = await doctors_coll.delete_one({"_id": ObjectId(_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid doctor ID format")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deleted successfully", "deleted_count": result.deleted_count, "id": _id}
