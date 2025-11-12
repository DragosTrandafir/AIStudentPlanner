from fastapi import APIRouter, HTTPException, status
from typing import List

from service.user_service import UserService
from repository.user_repository import UserRepository
from domain.user import User
from config.database import get_session
from dtos.user_dto import UserCreateRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreateRequest):
    with get_session() as session:
        user_repo = UserRepository(session)
        service = UserService(user_repo)
        try:
            user = service.create_user(
                name=user_data.name,
                email=user_data.email,
                major=user_data.major,
                google_id=user_data.google_id
            )
            return user
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    with get_session() as session:
        user_repo = UserRepository(session)
        service = UserService(user_repo)
        user = service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user


@router.get("/", response_model=List[UserResponse])
def get_all_users():
    with get_session() as session:
        user_repo = UserRepository(session)
        service = UserService(user_repo)
        return service.get_all_users()