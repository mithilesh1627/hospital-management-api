from data.init import staff_coll, user_coll
from model.staff_model import StaffBase, StaffCreate, Staff
from auth.auth_handler import get_password_hash
from auth.auth_role import Role
from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Dict, Any
from fastapi import HTTPException
from datetime import datetime, timezone

def dict_to_model(doc: dict) -> Staff:
    return Staff(
        id=str(doc["_id"]),
        user_id=str(doc.get("user_id")) if doc.get("user_id") else None,
        name=doc["name"],
        email=doc["email"],
        phone=doc["phone"],
        role=doc.get("role", Role.STAFF),
        shift=doc["shift"],
        created_at=doc.get("created_at", datetime.now(timezone.utc)),
        updated_at=doc.get("updated_at", datetime.now(timezone.utc))
    )

def model_to_dict(staff: StaffBase) -> dict:
    return staff.model_dump(exclude_unset=True)

async def create_staff(staff: StaffCreate) -> dict:
    # Create linked user account
    hashed_password = get_password_hash(staff.password)
    user_doc = {
        "email": staff.email,
        "password": hashed_password,
        "role": Role.STAFF,
        "linked_id": None,  # will set after staff insert
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    user_insert = await user_coll.insert_one(user_doc)

    # Create staff document and link user_id
    staff_dict = model_to_dict(staff)
    staff_dict["user_id"] = str(user_insert.inserted_id)
    staff_dict["created_at"] = datetime.now(timezone.utc)
    staff_dict["updated_at"] = datetime.now(timezone.utc)
    staff_insert = await staff_coll.insert_one(staff_dict)

    # Update user linked_id
    await user_coll.update_one({"_id": user_insert.inserted_id}, {"$set": {"linked_id": staff_insert.inserted_id}})

    return {"message": "Staff created with linked user", "staff_id": str(staff_insert.inserted_id), "user_id": str(user_insert.inserted_id)}

async def get_by_id(_id: str) -> Dict[str, Any]:
    try:
        doc = await staff_coll.find_one({"_id": ObjectId(_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Staff not found")
        return dict_to_model(doc).model_dump()
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid staff ID")

async def get_all() -> List[Staff]:
    staff_list: List[Staff] = []
    cursor = staff_coll.find({})
    async for doc in cursor:
        staff_list.append(dict_to_model(doc))
    return staff_list

async def update_staff_by_id(id: str, update_data: dict) -> dict:
    result = await staff_coll.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if not result.acknowledged:
        return {"message": "Update operation not acknowledged by MongoDB"}
    if result.matched_count == 0:
        return {"message": "No records matched the filter", "matched_count": 0, "modified_count": 0}
    return {"message": "Staff updated successfully", "matched_count": result.matched_count, "modified_count": result.modified_count}

async def delete_staff_by_id(_id: str) -> dict:
    try:
        result = await staff_coll.delete_one({"_id": ObjectId(_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid staff ID format")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"message": "Staff deleted successfully", "deleted_count": result.deleted_count, "id": _id}
