from typing import List, Optional, Any, Dict, Coroutine
from datetime import datetime,timezone
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from data.init import appointment_coll
from model.appointment_model import AppointmentBase, Appointment

def dict_to_model(doc: dict) -> Appointment:
    return Appointment(
        _id=str(doc["_id"]),
        patient_id=doc["patient_id"],
        doctor_id=doc["doctor_id"],
        appointment_date=doc["appointment_date"],
        reason=doc["reason"],
        status=doc["status"],
        appointment_type= doc["appointment_type"],
        payment_status=doc["payment_status"],
        notes=doc["notes"],
        created_at=doc["created_at"],
        updated_at=doc["updated_at"]
    )

async def create_appointment(appointment: AppointmentBase) -> dict:
    doc = appointment.model_dump()
    doc["created_at"] = datetime.now(timezone.utc)
    doc["updated_at"] = None
    result = await appointment_coll.insert_one(doc)
    return {"message": "Appointment created successfully",
            "appointment_id":f"{result.inserted_id}"}

async def get_appointment(appointment_id: str) -> Optional[Appointment]:
    doc = await appointment_coll.find_one({"_id": ObjectId(appointment_id)})
    if doc:
        return Appointment(
            _id=str(doc["_id"]),
            **{k: v for k, v in doc.items() if k != "_id"}
        )
    else:
        raise HTTPException(status_code=404, detail="Appointment not found")

async def get_all_appointments()-> List[dict]:
    appoint: List[dict] = []
    cursor = appointment_coll.find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        appoint.append(doc)
    return appoint

async def get_by_patient(patient_id: str) -> Appointment | None:
    try:
        doc = await appointment_coll.find_one({"patient_id": ObjectId(patient_id)},{})
        if doc:
            return dict_to_model(doc)
    except InvalidId:
        return None
    return None

async def get_by_doctor(doctor_id: str) -> List[Appointment]:
    cursor =  appointment_coll.find({"doctor_id": ObjectId(doctor_id)})
    docs = await cursor.to_list()
    return docs

async def get_upcoming_appointments(patient_id: str = None, doctor_id: str = None):

    now = datetime.now(timezone.utc)
    query = {
        "status": "scheduled",
        "appointment_date": {"$gt": now}
    }

    if patient_id:
        query["patient_id"] = patient_id
    if doctor_id:
        query["doctor_id"] = doctor_id

    cursor = appointment_coll.find(query).sort("appointment_date", 1)
    return await cursor.to_list(length=100)

async def update_appointment_by_id(appointment_id: str, update_data: dict) -> dict:
    try:
        update_data["updated_at"] = datetime.utcnow()
        result = await appointment_coll.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": update_data}
        )
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid doctor ID format")

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {
        "message": "Appointment updated successfully",
        "matched_count": result.matched_count,
        "modified_count": result.modified_count
    }

async def delete_appointment(appointment_id: str) ->dict:
    try:
        result = await appointment_coll.delete_one({"_id": ObjectId(appointment_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid doctor ID format")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {
        "message": "Appointment deleted successfully",
        "deleted_count": result.deleted_count
    }

async def update_appointment(filter_: dict,update_data: dict,multiple_update: bool = False) -> Dict[str, Any]:
    if multiple_update:
        rec = await appointment_coll.update_many(filter_, {"$set": update_data})
    else:
        rec = await appointment_coll.update_one(filter_, {"$set": update_data})

    if not rec.acknowledged:
        return {"message": "Update operation not acknowledged by MongoDB"}

    if rec.matched_count == 0:
        return {
            "message": "No records matched the filter",
            "matched_count": 0,
            "modified_count": 0
        }

    if multiple_update:
        docs = await appointment_coll.find(filter_).to_list(length=100)
    else:
        docs = await appointment_coll.find(filter_).to_list(length=1)

    #
    updated_docs = [dict_to_model(doc).model_dump() for doc in docs]

    return {
        "message": "Record(s) updated successfully",
        "matched_count": rec.matched_count,
        "modified_count": rec.modified_count,
        "updated_records": updated_docs
    }