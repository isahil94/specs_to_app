"""Notifications routes."""

from typing import List

from fastapi import APIRouter, Depends, Query, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from apps.backend.src.auth.service import AuthService
from apps.backend.src.core.exceptions import AppException
from apps.backend.src.core.schemas import NotificationResponse
from apps.backend.src.db.database import get_db
from apps.backend.src.notifications.service import NotificationsService

router = APIRouter(prefix="/notifications", tags=["notifications"])
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


@router.get("", response_model=List[NotificationResponse])
async def list_notifications(
    unread_only: bool = Query(False),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get notifications for current user."""
    try:
        return NotificationsService.get_user_notifications(db, current_user.id, unread_only)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark notification as read."""
    try:
        return NotificationsService.mark_as_read(db, notification_id, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        status_code = 404 if "not found" in e.message.lower() else 403
        raise HTTPException(status_code=status_code, detail=e.message)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a notification."""
    try:
        NotificationsService.delete_notification(db, notification_id, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        status_code = 404 if "not found" in e.message.lower() else 403
        raise HTTPException(status_code=status_code, detail=e.message)
