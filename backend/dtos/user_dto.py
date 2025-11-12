from pydantic import BaseModel, EmailStr
from typing import Optional, List
class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    major: Optional[str] = None
    google_id: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    major: Optional[str]
    google_id: Optional[str]

    class Config:
        from_attributes = True