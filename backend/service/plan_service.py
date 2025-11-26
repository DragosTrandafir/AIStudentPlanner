from __future__ import annotations
from datetime import date
from typing import List, Optional

from backend.domain.plan import Plan
from backend.repository.plan_repository import PlanRepository
from backend.repository.user_repository import UserRepository


class PlanService:
    def __init__(self, plan_repo: PlanRepository, user_repo: UserRepository):
        self.plan_repo = plan_repo
        self.user_repo = user_repo

    def create_plan(
        self,
        *,
        user_id: int,
        plan_date: date,
        notes: Optional[str] = None,
    ) -> Plan:
        # Validate user exists
        if not self.user_repo.get(user_id):
            raise ValueError("User does not exist")

        # Check if plan already exists for this date
        existing_plan = self.plan_repo.get_by_date(user_id, plan_date)
        if existing_plan:
            raise ValueError(f"Plan already exists for date {plan_date}")

        plan = Plan()
        plan.user_id = user_id
        plan.plan_date = plan_date
        plan.notes = notes

        self.plan_repo.add(plan)
        self.plan_repo.session.flush()
        self.plan_repo.session.refresh(plan)
        return plan

    def get_plan(self, plan_id: int) -> Optional[Plan]:
        return self.plan_repo.get(plan_id)

    def get_plan_by_date(self, user_id: int, plan_date: date) -> Optional[Plan]:
        return self.plan_repo.get_by_date(user_id, plan_date)

    def list_all(self, offset: int = 0, limit: int = 100) -> List[Plan]:
        return self.plan_repo.list_all(offset, limit)

    def list_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Plan]:
        return self.plan_repo.list_for_user(user_id, offset=offset, limit=limit)

    def update_plan(
        self,
        *,
        plan_id: int,
        user_id: int,
        plan_date: Optional[date] = None,
        notes: Optional[str] = None,
    ) -> Optional[Plan]:
        plan = self.plan_repo.get(plan_id)
        if not plan:
            return None

        # Verify ownership
        if plan.user_id != user_id:
            raise ValueError("Plan does not belong to this user")

        if plan_date is not None:
            # Check if another plan exists for the new date
            existing = self.plan_repo.get_by_date(user_id, plan_date)
            if existing and existing.id != plan_id:
                raise ValueError(f"Plan already exists for date {plan_date}")
            plan.plan_date = plan_date

        if notes is not None:
            plan.notes = notes

        return plan

    def delete_plan(self, *, plan_id: int, user_id: int) -> bool:
        plan = self.plan_repo.get(plan_id)
        if not plan:
            return False

        # Verify ownership
        if plan.user_id != user_id:
            raise ValueError("Plan does not belong to this user")

        self.plan_repo.delete(plan)
        return True