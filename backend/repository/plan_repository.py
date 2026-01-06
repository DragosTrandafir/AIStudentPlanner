from __future__ import annotations
from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.domain.plan import Plan
from backend.domain.ai_task import AITask
from .base import BaseRepository


class PlanRepository(BaseRepository[Plan]):
    def __init__(self, session: Session):
        super().__init__(Plan, session)

    def get(self, entity_id: int):
        """Override to eagerly load ai_tasks and their subjects."""
        stmt = select(Plan).where(Plan.id == entity_id).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        )
        return self.session.scalar(stmt)

    def list_all(self, offset: int = 0, limit: int = 100) -> List[Plan]:
        stmt = select(Plan).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        ).offset(offset).limit(limit).order_by(Plan.plan_date.desc())
        return list(self.session.scalars(stmt).unique().all())

    def list_for_user(self, user_id: int, *, offset: int = 0, limit: int = 100) -> List[Plan]:
        stmt = select(Plan).where(Plan.user_id == user_id).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        ).offset(offset).limit(limit).order_by(Plan.plan_date.desc())
        return list(self.session.scalars(stmt).unique().all())

    def get_by_date(self, user_id: int, plan_date: date) -> Optional[Plan]:
        stmt = select(Plan).where(Plan.user_id == user_id, Plan.plan_date == plan_date).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        )
        return self.session.scalar(stmt)

    def get_latest_generation(self, user_id: int) -> List[Plan]:
        """Get all plans from the latest generation (same generation_id) for a user."""
        stmt = select(Plan.generation_id).where(
            Plan.user_id == user_id,
            Plan.generation_id.isnot(None)
        ).order_by(Plan.generation_id.desc()).limit(1)
        latest_gen_id = self.session.scalar(stmt)
        
        if not latest_gen_id:
            return []
        
        stmt = select(Plan).where(
            Plan.user_id == user_id,
            Plan.generation_id == latest_gen_id
        ).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        ).order_by(Plan.plan_date.asc())
        return list(self.session.scalars(stmt).unique().all())

    def get_last_two_generations(self, user_id: int) -> tuple[Optional[List[Plan]], Optional[List[Plan]]]:
        """Get the last two schedules (by generation_id) for a user. Returns (latest, second_latest)."""
        # Get last 2 unique generation_ids
        stmt = select(Plan.generation_id).where(
            Plan.user_id == user_id,
            Plan.generation_id.isnot(None)
        ).distinct().order_by(Plan.generation_id.desc()).limit(2)
        gen_ids = self.session.scalars(stmt).all()
        
        if len(gen_ids) == 0:
            return None, None
        
        latest_gen_id = gen_ids[0]
        second_latest_gen_id = gen_ids[1] if len(gen_ids) > 1 else None
        
        # Fetch latest generation
        stmt_latest = select(Plan).where(
            Plan.user_id == user_id,
            Plan.generation_id == latest_gen_id
        ).options(
            joinedload(Plan.ai_tasks).joinedload(AITask.subject)
        ).order_by(Plan.plan_date.asc())
        latest_plans = list(self.session.scalars(stmt_latest).unique().all())
        
        # Fetch second latest generation if exists
        second_latest_plans = None
        if second_latest_gen_id:
            stmt_second = select(Plan).where(
                Plan.user_id == user_id,
                Plan.generation_id == second_latest_gen_id
            ).options(
                joinedload(Plan.ai_tasks).joinedload(AITask.subject)
            ).order_by(Plan.plan_date.asc())
            second_latest_plans = list(self.session.scalars(stmt_second).unique().all())
        
        return latest_plans, second_latest_plans