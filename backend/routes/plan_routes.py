from datetime import date, datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.plan_repository import PlanRepository
from backend.repository.user_repository import UserRepository
from backend.service.plan_service import PlanService

router = APIRouter(prefix="/users/{user_id}/plans", tags=["plans"])


class PlanCreateRequest(BaseModel):
    plan_date: date
    notes: Optional[str] = None


class PlanUpdateRequest(BaseModel):
    plan_date: Optional[date] = None
    notes: Optional[str] = None


class AITaskEntry(BaseModel):
    """Represents an AI Task entry in a plan."""
    time_allotted: str
    ai_task_name: str
    task_name: str
    difficulty: int
    priority: int

    @classmethod
    def from_ai_task(cls, ai_task):
        return cls(
            time_allotted=ai_task.time_allotted,
            ai_task_name=ai_task.ai_task_name,
            task_name=ai_task.subject.name,
            difficulty=ai_task.difficulty,
            priority=ai_task.priority,
        )


class PlanResponse(BaseModel):
    plan_date: date
    entries: List[AITaskEntry]
    notes: Optional[str]

    class Config:
        from_attributes = True

    @classmethod
    def from_plan(cls, plan):
        """Custom constructor to include entries from ai_tasks."""
        return cls(
            plan_date=plan.plan_date,
            entries=[AITaskEntry.from_ai_task(task) for task in plan.ai_tasks],
            notes=plan.notes,
        )


class PlanDetailResponse(BaseModel):
    """Detailed plan response with id and timestamps."""
    id: int
    user_id: int
    plan_date: date
    entries: List[AITaskEntry]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_plan(cls, plan):
        return cls(
            id=plan.id,
            user_id=plan.user_id,
            plan_date=plan.plan_date,
            entries=[AITaskEntry.from_ai_task(task) for task in plan.ai_tasks],
            notes=plan.notes,
            created_at=plan.created_at,
            updated_at=plan.updated_at,
        )


@router.post("/", response_model=PlanDetailResponse, status_code=status.HTTP_201_CREATED)
def add_plan(user_id: int, payload: PlanCreateRequest):
    """Create a new plan for a specific user."""
    with get_session() as session:
        service = PlanService(
            PlanRepository(session),
            UserRepository(session)
        )
        try:
            plan = service.create_plan(
                user_id=user_id,
                plan_date=payload.plan_date,
                notes=payload.notes,
            )
            return PlanDetailResponse.from_plan(plan)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")


@router.get("/latest", response_model=PlanResponse)
def get_latest_plan(user_id: int):
    """Get the most recent plan for a specific user."""
    with get_session() as session:
        service = PlanService(
            PlanRepository(session),
            UserRepository(session)
        )
        plans = service.list_for_user(user_id, offset=0, limit=1)
        if not plans:
            raise HTTPException(status_code=404, detail="No plans found for this user")
        return PlanResponse.from_plan(plans[0])


@router.get("/history", response_model=List[PlanResponse])
def get_plan_history(user_id: int):
    """Get all plans for a specific user."""
    with get_session() as session:
        service = PlanService(
            PlanRepository(session),
            UserRepository(session)
        )
        plans = service.list_for_user(user_id)
        return [PlanResponse.from_plan(plan) for plan in plans]


@router.get("/", response_model=List[PlanDetailResponse])
def list_user_plans(user_id: int):
    """List all plans for a specific user with full details."""
    with get_session() as session:
        service = PlanService(
            PlanRepository(session),
            UserRepository(session)
        )
        plans = service.list_for_user(user_id)
        return [PlanDetailResponse.from_plan(plan) for plan in plans]


@router.get("/{plan_id}", response_model=PlanDetailResponse)
def get_plan(user_id: int, plan_id: int):
    """Get a specific plan."""
    with get_session() as session:
        service = PlanService(
            PlanRepository(session),
            UserRepository(session)
        )
        plan = service.get_plan(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        if plan.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return PlanDetailResponse.from_plan(plan)


@router.get("/date/{plan_date}", response_model=PlanResponse)
def get_plan_by_date(user_id: int, plan_date: date):
    """Get a plan by date for a specific user."""
    with get_session() as session:
        service = PlanService(
            PlanRepository(session),
            UserRepository(session)
        )
        plan = service.get_plan_by_date(user_id, plan_date)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found for this date")
        return PlanResponse.from_plan(plan)


@router.put("/{plan_id}", response_model=PlanDetailResponse)
def update_plan(user_id: int, plan_id: int, payload: PlanUpdateRequest):
    """Update a plan."""
    with get_session() as session:
        service = PlanService(
            PlanRepository(session),
            UserRepository(session)
        )
        try:
            plan = service.update_plan(
                plan_id=plan_id,
                user_id=user_id,
                plan_date=payload.plan_date,
                notes=payload.notes,
            )
            if not plan:
                raise HTTPException(status_code=404, detail="Plan not found")
            return PlanDetailResponse.from_plan(plan)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(user_id: int, plan_id: int):
    """Delete a plan."""
    with get_session() as session:
        service = PlanService(
            PlanRepository(session),
            UserRepository(session)
        )
        try:
            if not service.delete_plan(plan_id=plan_id, user_id=user_id):
                raise HTTPException(status_code=404, detail="Plan not found")
        except ValueError as e:
            raise HTTPException(status_code=403, detail=str(e))