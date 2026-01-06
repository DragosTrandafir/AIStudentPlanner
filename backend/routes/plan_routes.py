from datetime import date, datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.config.database import get_session
from backend.repository.plan_repository import PlanRepository
from backend.repository.user_repository import UserRepository
from backend.repository.subject_repository import SubjectRepository
from backend.repository.ai_task_repository import AITaskRepository
from backend.service.plan_service import PlanService
from backend.service.ai_task_service import AITaskService
from backend.domain.ai_task import AITask
from backend.domain.plan import Plan

router = APIRouter(prefix="/users/{user_id}/plans", tags=["plans"])


class PlanCreateRequest(BaseModel):
    plan_date: date
    notes: Optional[str] = None


class PlanUpdateRequest(BaseModel):
    plan_date: Optional[date] = None
    notes: Optional[str] = None


class AITaskEntry(BaseModel):
    """Represents an AI Task entry in a plan."""
    id: int  # AI task database ID
    time_allotted: str
    ai_task_name: str
    task_name: str
    difficulty: int
    priority: int

    @classmethod
    def from_ai_task(cls, ai_task):
        return cls(
            id=ai_task.id,
            time_allotted=ai_task.time_allotted,
            ai_task_name=ai_task.ai_task_name,
            task_name=ai_task.subject.name,
            difficulty=ai_task.difficulty,
            priority=ai_task.priority,
        )


class PlanResponse(BaseModel):
    """Plan response with date, entries, notes, and generation_id."""
    id: int  # Plan database ID
    plan_date: date
    entries: List[AITaskEntry]
    notes: Optional[str]
    generation_id: Optional[str] = None  # UUID for schedule/generation grouping

    class Config:
        from_attributes = True

    @classmethod
    def from_plan(cls, plan):
        """Custom constructor to include entries from ai_tasks."""
        return cls(
            id=plan.id,
            plan_date=plan.plan_date,
            entries=[AITaskEntry.from_ai_task(task) for task in plan.ai_tasks],
            notes=plan.notes,
            generation_id=plan.generation_id,
        )


@router.post("/", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def add_plan(user_id: int, payload: PlanCreateRequest):
    """Create a new plan for a specific user."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        service = PlanService(
            PlanRepository(session),
            user_repo
        )
        try:
            plan = service.create_plan(
                user_id=user_id,
                plan_date=payload.plan_date,
                notes=payload.notes,
            )
            return PlanResponse.from_plan(plan)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error")


@router.get("/latest", response_model=PlanResponse)
def get_latest_plan(user_id: int):
    """Get the most recent plan for a specific user."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        service = PlanService(
            PlanRepository(session),
            user_repo
        )
        plans = service.list_for_user(user_id, offset=0, limit=1)
        if not plans:
            raise HTTPException(status_code=404, detail="No plans found for this user")
        return PlanResponse.from_plan(plans[0])


@router.get("/latest-schedule", response_model=List[PlanResponse])
def get_latest_schedule(user_id: int):
    """Get the entire latest schedule (all plans from latest generation) for a user."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        plan_repo = PlanRepository(session)
        service = PlanService(plan_repo, user_repo)
        
        # Get all plans from the latest generation
        plans = service.get_latest_generation(user_id)
        if not plans:
            raise HTTPException(status_code=404, detail="No schedules found for this user")
        
        return [PlanResponse.from_plan(plan) for plan in plans]


class ScheduleWithFeedback(BaseModel):
    """Schedule with its feedback."""
    plans: List[PlanResponse]
    feedback: Optional[Dict[str, Any]] = None


class LastTwoSchedulesResponse(BaseModel):
    """Response for last two schedules."""
    current_schedule: Optional[ScheduleWithFeedback] = None
    last_schedule: Optional[ScheduleWithFeedback] = None


@router.get("/last-two-schedules", response_model=LastTwoSchedulesResponse)
def get_last_two_schedules(user_id: int):
    """Get the last two schedules with their feedback."""
    from backend.repository.feedback_repository import FeedbackRepository
    
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        plan_repo = PlanRepository(session)
        feedback_repo = FeedbackRepository(session)
        service = PlanService(plan_repo, user_repo)
        
        # Get last two schedules
        latest_plans, second_latest_plans = plan_repo.get_last_two_generations(user_id)
        
        current_schedule = None
        last_schedule = None
        
        if latest_plans:
            generation_id = latest_plans[0].generation_id
            feedback = feedback_repo.get_feedback_for_generation(user_id, generation_id)
            current_schedule = ScheduleWithFeedback(
                plans=[PlanResponse.from_plan(p) for p in latest_plans],
                feedback={
                    "id": feedback.id,
                    "rating": feedback.rating,
                    "comments": feedback.comments,
                    "created_at": feedback.created_at.isoformat(),
                } if feedback else None
            )
        
        if second_latest_plans:
            generation_id = second_latest_plans[0].generation_id
            feedback = feedback_repo.get_feedback_for_generation(user_id, generation_id)
            last_schedule = ScheduleWithFeedback(
                plans=[PlanResponse.from_plan(p) for p in second_latest_plans],
                feedback={
                    "id": feedback.id,
                    "rating": feedback.rating,
                    "comments": feedback.comments,
                    "created_at": feedback.created_at.isoformat(),
                } if feedback else None
            )
        
        return LastTwoSchedulesResponse(
            current_schedule=current_schedule,
            last_schedule=last_schedule
        )


@router.get("/history", response_model=List[PlanResponse])
def get_plan_history(user_id: int):
    """Get all plans for a specific user."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        service = PlanService(
            PlanRepository(session),
            user_repo
        )
        plans = service.list_for_user(user_id)
        return [PlanResponse.from_plan(plan) for plan in plans]


@router.get("/", response_model=List[PlanResponse])
def list_user_plans(user_id: int):
    """List all plans for a specific user."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        service = PlanService(
            PlanRepository(session),
            user_repo
        )
        plans = service.list_for_user(user_id)
        return [PlanResponse.from_plan(plan) for plan in plans]


@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(user_id: int, plan_id: int):
    """Get a specific plan."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        service = PlanService(
            PlanRepository(session),
            user_repo
        )
        plan = service.get_plan(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        if plan.user_id != user_id:
            raise HTTPException(status_code=403, detail="Plan does not belong to this user")
        return PlanResponse.from_plan(plan)


@router.get("/date/{plan_date}", response_model=PlanResponse)
def get_plan_by_date(user_id: int, plan_date: date):
    """Get a plan by date for a specific user."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        service = PlanService(
            PlanRepository(session),
            user_repo
        )
        plan = service.get_plan_by_date(user_id, plan_date)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found for this date")
        return PlanResponse.from_plan(plan)


@router.put("/{plan_id}", response_model=PlanResponse)
def update_plan(user_id: int, plan_id: int, payload: PlanUpdateRequest):
    """Update a plan."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        service = PlanService(
            PlanRepository(session),
            user_repo
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
            return PlanResponse.from_plan(plan)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(user_id: int, plan_id: int):
    """Delete a plan."""
    with get_session() as session:
        user_repo = UserRepository(session)
        
        # Check if user exists
        if not user_repo.get(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        service = PlanService(
            PlanRepository(session),
            user_repo
        )
        try:
            if not service.delete_plan(plan_id=plan_id, user_id=user_id):
                raise HTTPException(status_code=404, detail="Plan not found")
        except ValueError as e:
            raise HTTPException(status_code=403, detail=str(e))


class GeneratedPlanResponse(BaseModel):
    """Response for generated AI plan."""
    plans: List[PlanResponse]
    message: str


@router.post("/generate", response_model=GeneratedPlanResponse, status_code=status.HTTP_201_CREATED)
def generate_plan(user_id: int):
    """
    Generate an AI plan for the user based on their subjects.
    Uses the AI orchestrator to generate study tasks and creates plans with AI tasks.
    """
    from ai_system.orchestrator.ai_orchestrator import AiOrchestrator

    with get_session() as session:
        user_repo = UserRepository(session)
        subject_repo = SubjectRepository(session)
        plan_repo = PlanRepository(session)
        ai_task_repo = AITaskRepository(session)

        # Check if user exists
        user = user_repo.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if user has subjects
        subjects = subject_repo.list_for_user(user_id)
        if not subjects:
            raise HTTPException(
                status_code=400,
                detail="No subjects found for this user. Add subjects before generating a plan."
            )

        # Create subject name to id mapping for fast lookup
        subject_map = {}
        for s in subjects:
            subject_map[s.name.lower()] = s.id
            subject_map[s.title.lower()] = s.id

        try:
            # Initialize orchestrator and generate plan
            orchestrator = AiOrchestrator()
            ai_plan = orchestrator.generate_plan_for_user(user_id, save_to_backend=False)

            if not ai_plan or "calendar" not in ai_plan:
                raise HTTPException(
                    status_code=500,
                    detail="AI orchestrator failed to generate a valid plan"
                )

            # Generate a unique generation_id for this schedule
            generation_id = str(uuid4())

            print(f"[generate_plan] AI plan calendar: {ai_plan.get('calendar')}")

            created_plans = []
            plan_service = PlanService(plan_repo, user_repo)
            ai_task_service = AITaskService(ai_task_repo, subject_repo, plan_repo)

            # Process each day in the generated calendar
            for day_plan in ai_plan.get("calendar", []):
                plan_date_str = day_plan.get("date")
                if not plan_date_str:
                    continue

                try:
                    plan_date = datetime.strptime(plan_date_str, "%Y-%m-%d").date()
                except ValueError:
                    continue

                notes = day_plan.get("notes", "")
                entries = day_plan.get("entries", [])

                # Create plan even if it has no entries (can be empty/rest day)
                # Always create a NEW plan (don't overwrite existing plans)
                # This preserves plan history and allows iterative refinement
                try:
                    plan = plan_service.create_plan(
                        user_id=user_id,
                        plan_date=plan_date,
                        notes=notes,
                        generation_id=generation_id,
                    )
                except Exception as e:
                    print(f"[generate_plan] Failed to create plan for {plan_date}: {e}")
                    continue

                # Process entries and create AI tasks (if any)
                for entry in entries:
                    time_allotted = entry.get("time_allotted", "")
                    task_name = entry.get("task_name", "")
                    subject_name = entry.get("subject_name/project_name", "")
                    difficulty = entry.get("difficulty", 3)
                    priority = entry.get("priority", 5)

                    # Clamp values to valid ranges
                    difficulty = max(1, min(5, difficulty))
                    priority = max(1, min(10, priority))

                    # Find subject by name
                    subject_id = subject_map.get(subject_name.lower())
                    if not subject_id:
                        # Try partial matching
                        for key, sid in subject_map.items():
                            if subject_name.lower() in key or key in subject_name.lower():
                                subject_id = sid
                                break

                    if not subject_id:
                        # Skip if no matching subject found
                        continue

                    # Create AI task
                    ai_task = AITask()
                    ai_task.time_allotted = time_allotted
                    ai_task.ai_task_name = task_name
                    ai_task.difficulty = difficulty
                    ai_task.priority = priority
                    ai_task.plan_id = plan.id
                    ai_task.task_id = subject_id
                    ai_task_repo.add(ai_task)

                session.flush()
                session.refresh(plan)
                created_plans.append(plan)

            if not created_plans:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create any plans from the generated AI response"
                )

            # Return the latest generation (which includes the plans we just created)
            latest_generation = plan_service.get_latest_generation(user_id)
            
            return GeneratedPlanResponse(
                plans=[PlanResponse.from_plan(p) for p in latest_generation],
                message=f"Successfully generated {len(latest_generation)} plan(s) with AI tasks"
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate plan: {str(e)}"
            )


@router.post("/reschedule", response_model=GeneratedPlanResponse, status_code=status.HTTP_201_CREATED)
def reschedule_plan(user_id: int):
    """
    Regenerate an AI plan for the user based on current and last feedback.
    Uses the AI Rescheduler to adjust the previous plan according to feedback.
    """
    from ai_system.orchestrator.ai_reschedule import AiRescheduler

    with get_session() as session:
        user_repo = UserRepository(session)
        subject_repo = SubjectRepository(session)
        plan_repo = PlanRepository(session)
        ai_task_repo = AITaskRepository(session)

        # Check if user exists
        user = user_repo.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if user has subjects
        subjects = subject_repo.list_for_user(user_id)
        if not subjects:
            raise HTTPException(
                status_code=400,
                detail="No subjects found for this user. Add subjects before rescheduling."
            )

        # Create subject name to id mapping for fast lookup
        subject_map = {}
        for s in subjects:
            subject_map[s.name.lower()] = s.id
            subject_map[s.title.lower()] = s.id

        try:
            # Initialize rescheduler and generate rescheduled plan
            rescheduler = AiRescheduler()
            ai_plan = rescheduler.generate_plan_for_user(user_id, save_to_backend=False)

            if not ai_plan or "calendar" not in ai_plan:
                raise HTTPException(
                    status_code=500,
                    detail="AI rescheduler failed to generate a valid plan"
                )

            # Generate a new unique generation_id for this rescheduled schedule
            generation_id = str(uuid4())

            created_plans = []
            plan_service = PlanService(plan_repo, user_repo)
            ai_task_service = AITaskService(ai_task_repo, subject_repo, plan_repo)

            # Process each day in the rescheduled calendar
            for day_plan in ai_plan.get("calendar", []):
                plan_date_str = day_plan.get("date")
                if not plan_date_str:
                    continue

                try:
                    plan_date = datetime.strptime(plan_date_str, "%Y-%m-%d").date()
                except ValueError:
                    continue

                notes = day_plan.get("notes", "")
                entries = day_plan.get("entries", [])

                # Create plan even if it has no entries (can be empty/rest day)
                # Always create a NEW plan with NEW generation_id (don't overwrite the old one)
                # This preserves the history and allows users to see the evolution of their schedules
                try:
                    plan = plan_service.create_plan(
                        user_id=user_id,
                        plan_date=plan_date,
                        notes=notes,
                        generation_id=generation_id,
                    )
                except Exception as e:
                    print(f"[reschedule_plan] Failed to create plan for {plan_date}: {e}")
                    continue

                # Process entries and create AI tasks (if any)
                for entry in entries:
                    time_allotted = entry.get("time_allotted", "")
                    task_name = entry.get("task_name", "")
                    subject_name = entry.get("subject_name/project_name", "")
                    difficulty = entry.get("difficulty", 3)
                    priority = entry.get("priority", 5)

                    # Clamp values to valid ranges
                    difficulty = max(1, min(5, difficulty))
                    priority = max(1, min(10, priority))

                    # Find subject by name
                    subject_id = subject_map.get(subject_name.lower())
                    if not subject_id:
                        # Try partial matching
                        for key, sid in subject_map.items():
                            if subject_name.lower() in key or key in subject_name.lower():
                                subject_id = sid
                                break

                    if not subject_id:
                        # Skip if no matching subject found
                        continue

                    # Create AI task
                    ai_task = AITask()
                    ai_task.time_allotted = time_allotted
                    ai_task.ai_task_name = task_name
                    ai_task.difficulty = difficulty
                    ai_task.priority = priority
                    ai_task.plan_id = plan.id
                    ai_task.task_id = subject_id
                    ai_task_repo.add(ai_task)

                session.flush()
                session.refresh(plan)
                created_plans.append(plan)

            if not created_plans:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create any rescheduled plans from the AI response"
                )

            # Return the latest generation (which includes the plans we just created)
            latest_generation = plan_service.get_latest_generation(user_id)
            
            return GeneratedPlanResponse(
                plans=[PlanResponse.from_plan(p) for p in latest_generation],
                message=f"Successfully rescheduled {len(latest_generation)} plan(s) based on feedback"
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to reschedule plan: {str(e)}"
            )
