from pydantic import EmailStr

import data.user_data as data
from model.user_model import UserCreate
from typing import Dict

async def create_user(user: UserCreate) -> Dict:
    return await data.create_user(user)

async def get_user_by_email(email: str) -> dict | None:
    return await data.get_user_by_email(email)

async def get_user_by_id(user_id: str) -> dict | None:
    return await data.get_user_by_id(user_id)

async def update_user(user_id: str, update_data: dict) -> dict:
    return await data.update_user(user_id, update_data)

async def delete_user(user_id: str) -> dict:
    return await data.delete_user(user_id)
