from pydantic import EmailStr

from data.init import user_coll
from model.user_model import UserCreate, UserOut
from bson import ObjectId
from datetime import datetime,timezone
from fastapi import HTTPException
from auth.auth_handler import get_password_hash, verify_password


async def create_user(user: UserCreate) -> dict:
    user_dict = user.model_dump()
    user_dict["email"] = str(user_dict["email"])
    user_dict["password"] = get_password_hash(user.password)
    user_dict["created_at"] = datetime.now(timezone.utc)
    user_dict["updated_at"] = datetime.now(timezone.utc)

    res = await user_coll.insert_one(user_dict)
    return {"id": str(res.inserted_id), "message": "User created successfully"}

async def get_user_by_email(email: str|EmailStr) -> dict | None:
    user = await user_coll.find_one({"email": str(email)})
    if user:
        user["id"] = str(user["_id"])
    return user

async def get_user_by_id(user_id: str) -> dict | None:
    try:
        user = await user_coll.find_one({"_id": ObjectId(user_id)})
        if user:
            user["id"] = str(user["_id"])
        return user
    except:
        return None

async def update_user(user_id: str, update_data: dict) -> dict:
    update_data["updated_at"] = datetime.now(timezone.utc)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    res = await user_coll.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"matched_count": res.matched_count,
            "modified_count": res.modified_count}

async def delete_user(user_id: str) -> dict:
    res = await user_coll.delete_one({"_id": ObjectId(user_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"deleted_count": res.deleted_count}
