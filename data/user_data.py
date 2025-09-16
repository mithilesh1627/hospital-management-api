from data.init import user_coll
from datetime import datetime,timezone
from bson import ObjectId
from bson.errors import InvalidId

async def create_user(email:str,hashing_password:str,role:str="patient")-> dict:
    doc = {"email":email,"password":hashing_password,"role":role,
           "created_at": datetime.now(timezone.utc),
           "updated_at": datetime.now(timezone.utc),
           }
    res = await user_coll.insert_one(doc)
    return {"Message":"new User created successfully",
            "_id": str(res.inserted_id),
            "email": email,
            "role": role}

async def get_user_by_email(email:str)->dict:
    doc = await user_coll.find_one({"email":email})
    if not doc:
        return {"Message":"user not found"}
    doc["_id"] = str(doc["_id"])
    return doc

async def get_user_by_id(user_id:str) ->dict:
    try:
        doc = await user_coll.find_one({"_id":ObjectId(user_id)})
    except InvalidId:
        return {"Message":"Invalid user id "}
    if not doc:
        return {"Message":"user not found"}

    doc["_id"] = str(doc["_id"])
    return doc

# async def update_user_details(update_data: dict, current_user: dict = Depends(get_current_user)):
#     update_data["updated_at"] = datetime.utcnow()
#     result = await user_coll.update_one(
#         {"_id": ObjectId(current_user["id"])},
#         {"$set": update_data}
#     )
#     if result.modified_count == 0:
#         raise HTTPException(status_code=400, detail="No changes made.")
#     return {"message": "User updated successfully."}
#
# async def update_profile_image(
#     file: UploadFile = File(...),
#     current_user: dict = Depends(get_current_user)
# ):
#     file_location = f"static/uploads/{current_user['id']}_{file.filename}"
#     os.makedirs("static/uploads", exist_ok=True)
#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#
#     await user_coll.update_one(
#         {"_id": ObjectId(current_user["id"])},
#         {"$set": {"profile_image": file_location, "updated_at": datetime.utcnow()}}
#     )
#     return {"message": "Profile image updated successfully.", "path": file_location}
#
#
# async def delete_user(current_user: dict = Depends(get_current_user)):
#     await user_coll.delete_one({"_id": ObjectId(current_user["id"])})
#     return {"message": "User deleted successfully."}