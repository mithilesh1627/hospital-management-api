from typing import List, Dict, Any
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from data.init import patients_coll
from model.patient_model import Patients, PatientsBase


def dict_to_model(doc: dict) -> Patients:
    return Patients(
        id=str(doc["_id"]),
        name=doc["name"],
        city=doc["city"],
        age=doc["age"],
        gender=doc["gender"],
        height_m=float(doc["height_m"]),
        weight_kg=float(doc["weight_kg"]),
        email=doc["email"],
        phone=doc["phone"],
        dob=doc["dob"],
        address=doc["address"],
        emergency_contact=doc["emergency_contact"],
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
        bmi=doc.get("bmi"),
        verdict=doc.get("verdict")
    )

def model_to_dict(patient: Patients) -> dict:
    return patient.model_dump()


# CRUD Operations

async def get_by_id(_id: str) -> Dict[str, Any]:
    try:
        doc = await patients_coll.find_one({"_id": ObjectId(_id)})
        if doc:
            return dict_to_model(doc).model_dump()
    except InvalidId:
        return {"message": "Invalid ID"}
    return {"message": f"No patient found with id: {_id}"}

async def get_all() -> List[Patients]:
    patients: List[Patients] = []
    cursor = patients_coll.find({})
    async for doc in cursor:
        patients.append(dict_to_model(doc))
    return patients

async def create_patient(patient: PatientsBase) ->Dict[str, Any]:
    insert = await patients_coll.insert_one(patient.model_dump())
    return {"message": "New patient created", "id": str(insert.inserted_id)}

async def update_patient_by_id(id: str, update_data: dict) -> Dict[str, Any]:
    try:
        result = await patients_coll.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid patient ID")

    if result.matched_count == 0:
        return {"message": "No records matched the filter", "matched_count": 0, "modified_count": 0}

    return {
        "message": "Record updated successfully",
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }

async def update_patient(filter: dict, update_data: dict, multiple_update: bool = False) -> Dict[str, Any]:
    if multiple_update:
        rec = await patients_coll.update_many(filter, {"$set": update_data})
        docs = await patients_coll.find(filter).to_list(length=100)
    else:
        rec = await patients_coll.update_one(filter, {"$set": update_data})
        docs = await patients_coll.find(filter).to_list(length=1)

    if rec.matched_count == 0:
        return {"message": "No records matched the filter", "matched_count": 0, "modified_count": 0}

    updated_docs = [dict_to_model(doc).model_dump() for doc in docs]
    return {
        "message": "Record(s) updated successfully",
        "matched_count": rec.matched_count,
        "modified_count": rec.modified_count,
        "updated_records": updated_docs
    }

async def delete_patient_by_id(patient_id: str) -> Dict[str, Any]:
    try:
        result = await patients_coll.delete_one({"_id": ObjectId(patient_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid patient ID")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"message": "Patient deleted successfully", "deleted_count": result.deleted_count, "id": patient_id}
