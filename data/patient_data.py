from typing import List, Optional, Any, Dict
from bson import ObjectId
from bson.errors import InvalidId
from data.init import patients_coll
from model.patient_model import Patients,PatientsBase
from fastapi import HTTPException

def dict_to_model(doc: dict) -> Patients:
    """Convert MongoDB dict into Patients model"""
    return Patients(
        id=str(doc["_id"]),
        name=doc["name"],
        city=doc["city"],
        age=int(doc["age"]) if isinstance(doc["age"], dict) else doc["age"],
        gender=doc["gender"],
        height_m=float(doc["height_m"]) if isinstance(doc["height_m"], dict) else doc["height_m"],
        weight_kg=float(doc["weight_kg"]) if isinstance(doc["weight_kg"], dict) else doc["weight_kg"]
    )

def model_to_dict(patient: Patients) -> dict:
    """Convert Patients model to plain dict (exclude internal id field)"""
    return patient.model_dump()

def model_to_json(patient: Patients) -> str:
    """Convert Patients model to JSON string (exclude internal id field)"""
    return patient.model_dump_json()

async def get_by_id(id: str) -> Optional[Patients]:
    """Find one patient by MongoDB _id"""
    try:
        doc = await patients_coll.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return dict_to_model(doc)
    except InvalidId:
        return None
    return None

async def get_all() -> List[Patients]:
    """Fetch all patients as a list of Patients models"""
    patients: List[Patients] = []
    cursor = patients_coll.find({})
    async for doc in cursor:
        patients.append(dict_to_model(doc))
    return patients

async def create_patient(patient:PatientsBase) ->dict:
    insert = await patients_coll.insert_one(patient.model_dump())
    print(insert.inserted_id)
    print(insert.acknowledged)
    return {"message":"New patient is created",
            "_id":f"{str(insert.inserted_id)}"}

async def update_patient_by_id(id:str,update_data:dict)->dict:
    result = await patients_coll.update_one(
        {"_id": ObjectId(id)},
        {"$set":update_data}
    )
    if not result.acknowledged:
        return {"message": "Update operation not acknowledged by MongoDB"}

    if result.matched_count == 0:
        return {"message": "No records matched the filter", "matched_count": 0, "modified_count": 0}


    return { "Message": "Record(s) Updated successfully",
             "matched_count": result.matched_count,
             "modified_count": result.modified_count,
    }

async def delete_patient_by_id(patient_id: str) -> dict:
    """
    Delete a patient by MongoDB _id
    """
    try:
        result = await patients_coll.delete_one({"_id": ObjectId(patient_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid patient ID format")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "message": "Patient deleted successfully",
        "deleted_count": result.deleted_count,
        "_id": patient_id
    }

async def update_patient(filter: dict,update_data: dict,multiple_update: bool = False) -> Dict[str, Any]:
    if multiple_update:
        rec = await patients_coll.update_many(filter, {"$set": update_data})
    else:
        rec = await patients_coll.update_one(filter, {"$set": update_data})

    if not rec.acknowledged:
        return {"message": "Update operation not acknowledged by MongoDB"}

    if rec.matched_count == 0:
        return {
            "message": "No records matched the filter",
            "matched_count": 0,
            "modified_count": 0
        }

    # Fetch updated docs with _id included
    if multiple_update:
        docs = await patients_coll.find(filter).to_list(length=100)
    else:
        docs = await patients_coll.find(filter).to_list(length=1)

    # Convert to Patients model (handles ObjectId → str + bmi/verdict)
    updated_docs = [dict_to_model(doc).model_dump() for doc in docs]

    return {
        "message": "Record(s) updated successfully",
        "matched_count": rec.matched_count,
        "modified_count": rec.modified_count,
        "updated_records": updated_docs
    }
