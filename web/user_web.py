from fastapi import APIRouter,HTTPException, Depends, Path, Body
from typing import Dict
from auth.auth_handler import (get_current_user,create_access_token,role_required,verify_password)
from auth.auth_role import Role
import service.user_service as service
from model.login_model import LoginRequest, LoginResponse
from model.user_model import UserCreate, UserUpdate, UserOut

user_router = APIRouter(prefix="/users", tags=["Users"])

# Create user (Admin only)
@user_router.post("/", response_model=Dict, summary="Create a new user")
async def create_user(user: UserCreate, current_user: Dict = Depends(role_required([Role.ADMIN]))):
    return await service.create_user(user)

# Get current user profile
@user_router.get("/me", summary="Get my profile")
async def get_my_profile(current_user: Dict = Depends(get_current_user)):
    return await service.get_user_by_id(current_user["id"])

# Update user (self or admin)
@user_router.put("/{user_id}", summary="Update user")
async def update_user(user_id: str, update_data: UserUpdate, current_user: Dict = Depends(get_current_user)):
    # Patients/Doctors/Staff can update only themselves
    if current_user["role"] != Role.ADMIN and current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    return await service.update_user(user_id, update_data.model_dump(exclude_unset=True))

# Delete user (Admin only)
@user_router.delete("/{user_id}", summary="Delete a user")
async def delete_user(user_id: str, current_user: Dict = Depends(role_required([Role.ADMIN]))):
    return await service.delete_user(user_id)

@user_router.post("/login", response_model=LoginResponse, summary="Login and get JWT token")
async def login(request: LoginRequest):
    user = await service.get_user_by_email(str(request.email))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = create_access_token(subject=user["id"], role=user["role"])
    return LoginResponse(**token_data)