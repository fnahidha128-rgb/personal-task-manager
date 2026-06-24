from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
import uuid

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

sessions = {}

api_key_header = APIKeyHeader(name="Authorization")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str,
                    hashed_password: str):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_token(email: str):
    token = str(uuid.uuid4())
    sessions[token] = email
    return token


def get_current_user(
        token: str = Depends(api_key_header)
):
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    if token not in sessions:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return sessions[token]