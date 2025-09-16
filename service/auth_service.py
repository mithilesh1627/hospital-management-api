from typing import Dict,Any
from datetime import timedelta
from fastapi import HTTPException
from data.user_data import create_user,get_user_by_id,get_user_by_email
from auth.hashing import get_password_hash,verify_password
from auth.auth_handler import create_access_token

class AuthUser:

    @staticmethod
    async def register_user(email: str, password: str, role: str = "patient") ->dict:
        existing = await get_user_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed = get_password_hash(password)
        user = await create_user(email=email, hashing_password=hashed, role=role)
        return user

    @staticmethod
    async def authenticate_user(email: str, password: str) ->dict:
        user = await get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not verify_password(password, user.get("password", "")):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    @staticmethod
    async def create_token_for_user(user: Dict[str, Any], expires_minutes: int | None = None) -> Dict[str, Any]:
        sub = user["id"]
        role = user.get("role", "patient")
        expires_delta = timedelta(minutes=expires_minutes) if expires_minutes else None
        token_info = create_access_token(subject=sub, role=role, expires_delta=expires_delta)
        return token_info

    @staticmethod
    async def get_user_by_id(user_id:str)->dict:
        return await get_user_by_id(user_id)
