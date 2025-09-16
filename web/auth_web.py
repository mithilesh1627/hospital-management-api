from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,HTTPException,status
from typing import Dict

from auth.auth_handler import decode_access_token
from service.auth_service import AuthUser
from model.auth_user_model import Token, UserCreate, UserResponse

auth_router = APIRouter(prefix="/auth",tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

@auth_router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate):
    created = await AuthUser.register_user(user.email, user.password, role=user.role)
    return {"id": created["id"], "email": created["email"], "role": created["role"]}


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await AuthUser.authenticate_user(form_data.username, form_data.password)
    token_info = await AuthUser.create_token_for_user(user)
    return {"access_token": token_info["access_token"], "token_type": token_info["token_type"], "expires_at": token_info["expires_at"]}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = await AuthUser.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def role_required(required_roles):
    if isinstance(required_roles, str):
        roles = [required_roles]
    else:
        roles = list(required_roles)

    async def role_checker(current_user: Dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return current_user
    return role_checker

@auth_router.get("/appointments/doctor-only")
async def doctor_only_endpoint(user=Depends(role_required("doctor"))):
    return {"message": "You are a doctor", "user": user}