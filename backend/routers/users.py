from fastapi import APIRouter, HTTPException, Header

from schemas import UserRegister, UserLogin
from database import create_user, get_user_by_email
from auth import (
    hash_password,
    verify_password,
    create_token,
    get_current_user
)

router = APIRouter()


@router.post("/register")
def register(user: UserRegister):

    existing_user = get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    create_user(
        user.email,
        hashed_password
    )

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(user: UserLogin):

    db_user = get_user_by_email(user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
            user.password,
            db_user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_token(user.email)

    return {
        "token": token
    }


@router.get("/me")
def me(authorization: str = Header(None)):

    return {
        "received_token": authorization
    }