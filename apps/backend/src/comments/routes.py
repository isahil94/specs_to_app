"""Comments routes."""

from typing import List

from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from apps.backend.src.auth.service import AuthService
from apps.backend.src.comments.service import CommentsService
from apps.backend.src.core.exceptions import AppException
from apps.backend.src.core.schemas import CommentCreate, CommentResponse
from apps.backend.src.db.database import get_db

router = APIRouter(prefix="/tasks", tags=["comments"])
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


@router.get("/{task_id}/comments", response_model=List[CommentResponse])
async def get_task_comments(
    task_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get comments for a task."""
    try:
        return CommentsService.get_task_comments(db, task_id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=e.message)


@router.post("/{task_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    task_id: str,
    comment_data: CommentCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a comment on a task."""
    try:
        return CommentsService.create_comment(db, task_id, current_user.id, comment_data)
    except AppException as e:
        from fastapi import HTTPException

        status_code = 404 if "not found" in e.message.lower() else 400
        raise HTTPException(status_code=status_code, detail=e.message)


@router.delete("/{task_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    task_id: str,
    comment_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a comment."""
    try:
        CommentsService.delete_comment(db, comment_id, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        status_code = 404 if "not found" in e.message.lower() else 403
        raise HTTPException(status_code=status_code, detail=e.message)
