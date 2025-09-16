from dotenv import load_dotenv
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> dict[str, Any]:
    """Generate a new JWT access token with subject & role claims."""
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": subject, "role": role, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "expires_at": expire,
    }

def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    """Decode and validate a JWT access token. Returns None if invalid/expired."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
