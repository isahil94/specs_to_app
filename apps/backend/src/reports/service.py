"""Reports and Dashboard service."""

from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from apps.backend.src.core.models import Task, TaskPriority, TaskStatus
from apps.backend.src.core.schemas import (
    DashboardMetrics,
    DashboardResponse,
    TaskResponse,
)


class ReportsService:
    """Reports and Dashboard service."""

    @staticmethod
    def get_dashboard(db: Session, user_id: str) -> DashboardResponse:
        """Get dashboard for a user."""
        # Get metrics
        total_tasks = (
            db.query(func.count(Task.id))
            .filter(
                (Task.created_by_id == user_id) | (Task.assignee_id == user_id),
                Task.is_archived == False,
            )
            .scalar()
        )

        completed_tasks = (
            db.query(func.count(Task.id))
            .filter(
                (Task.created_by_id == user_id) | (Task.assignee_id == user_id),
                Task.status == TaskStatus.DONE,
            )
            .scalar()
        )

        overdue_tasks = (
            db.query(func.count(Task.id))
            .filter(
                (Task.created_by_id == user_id) | (Task.assignee_id == user_id),
                Task.due_date < datetime.utcnow(),
                Task.status != TaskStatus.DONE,
            )
            .scalar()
        )

        in_progress_tasks = (
            db.query(func.count(Task.id))
            .filter(
                (Task.created_by_id == user_id) | (Task.assignee_id == user_id),
                Task.status == TaskStatus.IN_PROGRESS,
            )
            .scalar()
        )

        assigned_to_me = (
            db.query(func.count(Task.id))
            .filter(Task.assignee_id == user_id, Task.is_archived == False)
            .scalar()
        )

        metrics = DashboardMetrics(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            overdue_tasks=overdue_tasks,
            in_progress_tasks=in_progress_tasks,
            assigned_to_me=assigned_to_me,
        )

        # Get recent tasks
        recent_tasks = (
            db.query(Task)
            .filter(
                (Task.created_by_id == user_id) | (Task.assignee_id == user_id),
                Task.is_archived == False,
            )
            .order_by(Task.updated_at.desc())
            .limit(10)
            .all()
        )

        # Get overdue tasks
        overdue = (
            db.query(Task)
            .filter(
                (Task.created_by_id == user_id) | (Task.assignee_id == user_id),
                Task.due_date < datetime.utcnow(),
                Task.status != TaskStatus.DONE,
            )
            .order_by(Task.due_date)
            .limit(10)
            .all()
        )

        # Team summary (placeholder - would be more detailed in production)
        team_summary = []

        return DashboardResponse(
            metrics=metrics,
            recent_tasks=[TaskResponse.from_orm(task) for task in recent_tasks],
            overdue_tasks=[TaskResponse.from_orm(task) for task in overdue],
            team_summary=team_summary,
        )

    @staticmethod
    def get_user_workload(db: Session, user_id: str) -> dict:
        """Get user workload summary."""
        by_status = (
            db.query(Task.status, func.count(Task.id))
            .filter(Task.assignee_id == user_id, Task.is_archived == False)
            .group_by(Task.status)
            .all()
        )

        by_priority = (
            db.query(Task.priority, func.count(Task.id))
            .filter(Task.assignee_id == user_id, Task.is_archived == False)
            .group_by(Task.priority)
            .all()
        )

        return {
            "by_status": {str(status): count for status, count in by_status},
            "by_priority": {str(priority): count for priority, count in by_priority},
        }

    @staticmethod
    def get_team_workload(db: Session, team_id: str) -> dict:
        """Get team workload summary."""
        tasks = db.query(Task).filter(Task.team_id == team_id, Task.is_archived == False).all()

        total = len(tasks)
        completed = len([t for t in tasks if t.status == TaskStatus.DONE])
        in_progress = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
        overdue = len([t for t in tasks if t.due_date and t.due_date < datetime.utcnow()])

        return {
            "total_tasks": total,
            "completed": completed,
            "in_progress": in_progress,
            "overdue": overdue,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
        }
