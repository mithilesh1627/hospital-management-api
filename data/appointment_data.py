from data.init import appointment_coll
from model.appointment_model import AppointmentBase, Appointment
from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Dict, Any
from fastapi import HTTPException
from datetime import datetime, timezone

def dict_to_model(doc: dict) -> Appointment:
    return Appointment(
        id=str(doc["_id"]),
        patient_id=str(doc["patient_id"]),
        doctor_id=str(doc["doctor_id"]),
        appointment_date=doc["appointment_date"],
        reason=doc["reason"],
        appointment_type=doc["appointment_type"],
        status=doc.get("status", "scheduled"),
        payment_status=doc.get("payment_status", "pending"),
        notes=doc.get("notes"),
        created_at=doc.get("created_at", datetime.now(timezone.utc)),
        updated_at=doc.get("updated_at", datetime.now(timezone.utc))
    )

async def create_appointment(appointment: AppointmentBase) -> Dict[str, Any]:
    doc = appointment.model_dump()
    doc["created_at"] = datetime.now(timezone.utc)
    doc["updated_at"] = datetime.now(timezone.utc)
    insert_result = await appointment_coll.insert_one(doc)
    return {"message": "Appointment created", "id": str(insert_result.inserted_id)}

async def get_by_id(_id: str) -> Dict[str, Any]:
    try:
        doc = await appointment_coll.find_one({"_id": ObjectId(_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return dict_to_model(doc).model_dump()
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid appointment ID")

async def get_all() -> List[Appointment]:
    appointments: List[Appointment] = []
    cursor = appointment_coll.find({})
    async for doc in cursor:
        appointments.append(dict_to_model(doc))
    return appointments

async def update_appointment_by_id(id: str, update_data: dict) -> Dict[str, Any]:
    update_data["updated_at"] = datetime.now(timezone.utc)
    try:
        result = await appointment_coll.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid appointment ID")
    if not result.acknowledged:
        return {"message": "Update not acknowledged"}
    if result.matched_count == 0:
        return {"message": "No appointment matched", "matched_count": 0, "modified_count": 0}
    return {"message": "Appointment updated", "matched_count": result.matched_count, "modified_count": result.modified_count}

async def delete_appointment_by_id(_id: str) -> Dict[str, Any]:
    try:
        result = await appointment_coll.delete_one({"_id": ObjectId(_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid appointment ID")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted", "deleted_count": result.deleted_count, "id": _id}
