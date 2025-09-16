from typing import List, Optional, Dict, Any, Union
from bson import ObjectId, errors
from fastapi import HTTPException
from data.init import staff_coll
from model.staff_model import Staff, StaffBase


def dict_to_model(doc: dict) -> Staff:
    return Staff(
        id=str(doc["_id"]),
        name=doc["name"],
        role=doc["role"],
        shift=doc["shift"],
        salary=float(doc["salary"]),
        contact=int(doc["contact"]),
        city=doc["city"]
    )


async def create_staff(staff: StaffBase) -> dict:
    result = await staff_coll.insert_one(staff.model_dump())
    return {
        "message": "New staff member created successfully",
        "_id": str(result.inserted_id)
    }


async def get_all() -> List[dict]:
    staff_list: List[dict] = []
    cursor = staff_coll.find({})
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        staff_list.append(doc)
    return staff_list


async def get_by_id(staff_id: str) -> Optional[Staff]:
    try:
        doc = await staff_coll.find_one({"_id": ObjectId(staff_id)})
        if doc:
            return dict_to_model(doc)
    except errors.InvalidId:
        return None
    return None


async def update_staff_by_id(staff_id: str, update_data: dict) -> dict:
    try:
        result = await staff_coll.update_one(
            {"_id": ObjectId(staff_id)},
            {"$set": update_data}
        )
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid staff ID format")

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Staff not found")

    return {
        "message": "Staff record updated successfully",
        "matched_count": result.matched_count,
        "modified_count": result.modified_count
    }


async def delete_staff_by_id(staff_id: str) -> dict:
    try:
        result = await staff_coll.delete_one({"_id": ObjectId(staff_id)})
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid staff ID format")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Staff not found")

    return {
        "message": "Staff deleted successfully",
        "deleted_count": result.deleted_count,
        "_id": staff_id
    }

async def update_staff(
    filter: Union[str, dict],
    update_data: dict,
    multiple_update: bool = False
) -> Dict[str, Any]:
    """Update one or many staff records."""

    if isinstance(filter, str):
        try:
            filter = {"_id": ObjectId(filter)}
        except errors.InvalidId:
            raise HTTPException(status_code=400, detail="Invalid staff ID format")


    if multiple_update:
        rec = await staff_coll.update_many(filter, {"$set": update_data})
    else:
        rec = await staff_coll.update_one(filter, {"$set": update_data})

    if not rec.acknowledged:
        return {"message": "Update operation not acknowledged by MongoDB"}

    if rec.matched_count == 0:
        return {
            "message": "No records matched the filter",
            "matched_count": 0,
            "modified_count": 0
        }


    docs = await staff_coll.find(filter).to_list(length=100 if multiple_update else 1)
    updated_docs = [dict_to_model(doc).model_dump() for doc in docs]

    return {
        "message": "Record(s) updated successfully",
        "matched_count": rec.matched_count,
        "modified_count": rec.modified_count,
        "updated_records": updated_docs
    }
