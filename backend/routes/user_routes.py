from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.user_repository import UserRepository
from backend.service.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


class UserCreateRequest(BaseModel):
    name: str
    username: str
    email: str
    password: str
    major: Optional[str] = None
    google_id: Optional[str] = None


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    major: Optional[str] = None
    google_id: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str
    major: Optional[str]
    google_id: Optional[str]
    created_at: datetime


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


class LoginResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str
    major: Optional[str]
    google_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    """User login with username/email and password"""
    with get_session() as session:
        service = UserService(UserRepository(session))
        try:
            user = service.login_user(payload.username_or_email, payload.password)
            return user
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_user(payload: UserCreateRequest):
    """Create a new user."""
    with get_session() as session:
        service = UserService(UserRepository(session))
        try:
            user = service.create_user(
                name=payload.name,
                username=payload.username,
                email=payload.email,
                password=payload.password,
                major=payload.major,
                google_id=payload.google_id
            )
            return user
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Google ID already exists")


@router.get("/", response_model=List[UserResponse])
def list_users():
    """List all users."""
    with get_session() as session:
        service = UserService(UserRepository(session))
        return service.list_all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get a specific user by ID."""
    with get_session() as session:
        service = UserService(UserRepository(session))
        user = service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdateRequest):
    """Update a user."""
    with get_session() as session:
        service = UserService(UserRepository(session))
        try:
            user = service.update_user(
                user_id=user_id,
                name=payload.name,
                email=payload.email,
                major=payload.major,
                google_id=payload.google_id
            )
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Google ID already exists")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Delete a user."""
    with get_session() as session:
        service = UserService(UserRepository(session))
        if not service.delete_user(user_id):
            raise HTTPException(status_code=404, detail="User not found")