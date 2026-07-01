"""Tasks routes."""

from fastapi import APIRouter, Depends, Query, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from apps.backend.src.auth.service import AuthService
from apps.backend.src.core.exceptions import AppException
from apps.backend.src.core.schemas import (
    TaskCreate,
    TaskDetailResponse,
    TaskListResponse,
    TaskResponse,
    TaskStatusUpdate,
    TaskUpdate,
)
from apps.backend.src.db.database import get_db
from apps.backend.src.tasks.service import TasksService

router = APIRouter(prefix="/tasks", tags=["tasks"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)
):
    """Get current authenticated user."""
    token = credentials.credentials
    user = AuthService.verify_token(db, token)
    if not user:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Invalid token")
    return user


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: str = Query(None),
    priority: str = Query(None),
    assignee_id: str = Query(None),
    search: str = Query(None),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List tasks with filtering."""
    try:
        return TasksService.list_tasks(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            status=status,
            priority=priority,
            assignee_id=assignee_id,
            search=search,
        )
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task."""
    try:
        return TasksService.create_task(db, current_user.id, task_data)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.get("/{task_id}", response_model=TaskDetailResponse)
async def get_task(
    task_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get task details."""
    try:
        task = TasksService.get_task(db, task_id, current_user.id)
        comments_count = len(task.comments) if task.comments else 0
        return TaskDetailResponse(
            **{**TaskResponse.from_orm(task).dict(), "comments_count": comments_count}
        )
    except AppException as e:
        from fastapi import HTTPException

        status_code = 404 if "not found" in e.message.lower() else 403
        raise HTTPException(status_code=status_code, detail=e.message)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    update_data: TaskUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a task."""
    try:
        return TasksService.update_task(db, task_id, current_user.id, update_data)
    except AppException as e:
        from fastapi import HTTPException

        status_code = 404 if "not found" in e.message.lower() else 400
        raise HTTPException(status_code=status_code, detail=e.message)


@router.post("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: str,
    status_update: TaskStatusUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update task status."""
    try:
        return TasksService.update_task_status(db, task_id, current_user.id, status_update)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.post("/{task_id}/archive", response_model=TaskResponse)
async def archive_task(
    task_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Archive a task."""
    try:
        return TasksService.archive_task(db, task_id, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.post("/{task_id}/restore", response_model=TaskResponse)
async def restore_task(
    task_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Restore an archived task."""
    try:
        return TasksService.restore_task(db, task_id, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.post("/{task_id}/duplicate", response_model=TaskResponse)
async def duplicate_task(
    task_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Duplicate a task."""
    try:
        return TasksService.duplicate_task(db, task_id, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a task (admin only)."""
    try:
        TasksService.delete_task(db, task_id, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=403, detail=e.message)
