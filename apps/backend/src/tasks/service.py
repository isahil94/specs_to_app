"""Tasks service."""

import uuid
from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from apps.backend.src.core.exceptions import (
    AuthorizationException,
    InvalidStatusTransitionException,
    ResourceNotFoundException,
)
from apps.backend.src.core.models import (
    Task,
    TaskHistory,
    TaskPriority,
    TaskStatus,
    User,
)
from apps.backend.src.core.schemas import (
    TaskCreate,
    TaskDetailResponse,
    TaskListResponse,
    TaskResponse,
    TaskStatusUpdate,
    TaskUpdate,
)


class TasksService:
    """Tasks service."""

    # Valid status transitions
    STATUS_TRANSITIONS = {
        TaskStatus.TODO: [TaskStatus.IN_PROGRESS, TaskStatus.ARCHIVED],
        TaskStatus.IN_PROGRESS: [TaskStatus.REVIEW, TaskStatus.TODO, TaskStatus.ARCHIVED],
        TaskStatus.REVIEW: [TaskStatus.DONE, TaskStatus.IN_PROGRESS, TaskStatus.ARCHIVED],
        TaskStatus.DONE: [TaskStatus.ARCHIVED],
        TaskStatus.ARCHIVED: [TaskStatus.TODO],
    }

    @staticmethod
    def create_task(
        db: Session, creator_id: str, task_data: TaskCreate
    ) -> TaskResponse:
        """Create a new task."""
        task = Task(
            id=str(uuid.uuid4()),
            title=task_data.title,
            description=task_data.description,
            status=TaskStatus(task_data.status or TaskStatus.TODO),
            priority=TaskPriority(task_data.priority or TaskPriority.MEDIUM),
            created_by_id=creator_id,
            assignee_id=task_data.assignee_id,
            team_id=task_data.team_id,
            due_date=task_data.due_date,
            labels=",".join(task_data.labels) if task_data.labels else None,
        )

        db.add(task)
        db.flush()

        # Create history entry
        history = TaskHistory(
            id=str(uuid.uuid4()),
            task_id=task.id,
            changed_by_id=creator_id,
            field_name="status",
            new_value=task.status.value,
            change_type="created",
        )
        db.add(history)
        db.commit()
        db.refresh(task)

        return TaskResponse.from_orm(task)

    @staticmethod
    def get_task(db: Session, task_id: str, user_id: str) -> Optional[Task]:
        """Get task by ID with authorization check."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ResourceNotFoundException("Task", task_id)

        # Check authorization (can view if owner, assignee, or in same team)
        if not TasksService._can_access_task(db, task, user_id):
            raise AuthorizationException(
                "You do not have permission to access this task."
            )

        return task

    @staticmethod
    def list_tasks(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 50,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> TaskListResponse:
        """List tasks with filtering."""
        query = db.query(Task).filter(Task.is_archived == False)

        # Filter by user's tasks or assigned to user
        query = query.filter(
            or_(Task.created_by_id == user_id, Task.assignee_id == user_id)
        )

        if status:
            query = query.filter(Task.status == TaskStatus(status))
        if priority:
            query = query.filter(Task.priority == TaskPriority(priority))
        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)
        if search:
            query = query.filter(
                or_(
                    Task.title.ilike(f"%{search}%"),
                    Task.description.ilike(f"%{search}%"),
                )
            )

        total_count = query.count()
        tasks = query.offset(skip).limit(limit).all()

        return TaskListResponse(
            items=[TaskResponse.from_orm(task) for task in tasks],
            total_count=total_count,
            page=skip // limit + 1,
            page_size=limit,
        )

    @staticmethod
    def update_task(
        db: Session, task_id: str, user_id: str, update_data: TaskUpdate
    ) -> TaskResponse:
        """Update task."""
        task = TasksService.get_task(db, task_id, user_id)

        # Check if task is archived
        if task.is_archived:
            raise AuthorizationException("Cannot modify archived tasks.")

        # Check authorization (only creator or assignee can update)
        if task.created_by_id != user_id and task.assignee_id != user_id:
            raise AuthorizationException("You do not have permission to update this task.")

        # Update fields
        if update_data.title:
            task.title = update_data.title
        if update_data.description is not None:
            task.description = update_data.description
        if update_data.status:
            current_status = TaskStatus(task.status.value)
            new_status = TaskStatus(update_data.status)
            if not TasksService._can_transition(current_status, new_status):
                raise InvalidStatusTransitionException(
                    current_status.value, new_status.value
                )
            task.status = new_status
        if update_data.priority:
            task.priority = TaskPriority(update_data.priority)
        if update_data.assignee_id is not None:
            task.assignee_id = update_data.assignee_id
        if update_data.due_date is not None:
            task.due_date = update_data.due_date
        if update_data.labels is not None:
            task.labels = ",".join(update_data.labels) if update_data.labels else None

        db.commit()
        db.refresh(task)

        return TaskResponse.from_orm(task)

    @staticmethod
    def update_task_status(
        db: Session, task_id: str, user_id: str, status_update: TaskStatusUpdate
    ) -> TaskResponse:
        """Update task status with transition validation."""
        task = TasksService.get_task(db, task_id, user_id)

        current_status = TaskStatus(task.status.value)
        new_status = TaskStatus(status_update.status)

        if not TasksService._can_transition(current_status, new_status):
            raise InvalidStatusTransitionException(current_status.value, new_status.value)

        task.status = new_status

        # Create history entry
        history = TaskHistory(
            id=str(uuid.uuid4()),
            task_id=task.id,
            changed_by_id=user_id,
            field_name="status",
            old_value=current_status.value,
            new_value=new_status.value,
            change_type="status_changed",
        )
        db.add(history)
        db.commit()
        db.refresh(task)

        return TaskResponse.from_orm(task)

    @staticmethod
    def archive_task(db: Session, task_id: str, user_id: str) -> TaskResponse:
        """Archive a task."""
        task = TasksService.get_task(db, task_id, user_id)

        if task.is_archived:
            raise AuthorizationException("Task is already archived.")

        task.is_archived = True
        task.archived_at = datetime.utcnow()

        history = TaskHistory(
            id=str(uuid.uuid4()),
            task_id=task.id,
            changed_by_id=user_id,
            field_name="archived",
            new_value="true",
            change_type="archived",
        )
        db.add(history)
        db.commit()
        db.refresh(task)

        return TaskResponse.from_orm(task)

    @staticmethod
    def restore_task(db: Session, task_id: str, user_id: str) -> TaskResponse:
        """Restore an archived task."""
        task = TasksService.get_task(db, task_id, user_id)

        if not task.is_archived:
            raise AuthorizationException("Task is not archived.")

        task.is_archived = False
        task.archived_at = None
        task.status = TaskStatus.TODO

        history = TaskHistory(
            id=str(uuid.uuid4()),
            task_id=task.id,
            changed_by_id=user_id,
            field_name="archived",
            new_value="false",
            change_type="restored",
        )
        db.add(history)
        db.commit()
        db.refresh(task)

        return TaskResponse.from_orm(task)

    @staticmethod
    def duplicate_task(db: Session, task_id: str, user_id: str) -> TaskResponse:
        """Duplicate a task."""
        task = TasksService.get_task(db, task_id, user_id)

        new_task = Task(
            id=str(uuid.uuid4()),
            title=f"{task.title} (Copy)",
            description=task.description,
            status=TaskStatus.TODO,
            priority=task.priority,
            created_by_id=user_id,
            assignee_id=None,
            team_id=task.team_id,
            due_date=task.due_date,
            labels=task.labels,
        )

        db.add(new_task)
        db.flush()

        history = TaskHistory(
            id=str(uuid.uuid4()),
            task_id=new_task.id,
            changed_by_id=user_id,
            field_name="status",
            new_value=new_task.status.value,
            change_type="created",
        )
        db.add(history)
        db.commit()
        db.refresh(new_task)

        return TaskResponse.from_orm(new_task)

    @staticmethod
    def delete_task(db: Session, task_id: str, user_id: str) -> None:
        """Delete a task (admin only)."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ResourceNotFoundException("Task", task_id)

        # Only admins can permanently delete
        db.delete(task)
        db.commit()

    @staticmethod
    def _can_transition(current: TaskStatus, target: TaskStatus) -> bool:
        """Check if status transition is valid."""
        allowed = TasksService.STATUS_TRANSITIONS.get(current, [])
        return target in allowed

    @staticmethod
    def _can_access_task(db: Session, task: Task, user_id: str) -> bool:
        """Check if user can access task."""
        return (
            task.created_by_id == user_id
            or task.assignee_id == user_id
            or (task.team_id and user_id in [u.id for u in db.query(User).filter(User.teams.any()).all()])
        )
