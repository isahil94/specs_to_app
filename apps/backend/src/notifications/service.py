"""Notifications service."""

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from apps.backend.src.core.exceptions import ResourceNotFoundException
from apps.backend.src.core.models import Notification
from apps.backend.src.core.schemas import NotificationResponse


class NotificationsService:
    """Notifications service."""

    @staticmethod
    def create_notification(
        db: Session,
        user_id: str,
        notification_type: str,
        title: str,
        message: str,
        task_id: Optional[str] = None,
        related_user_id: Optional[str] = None,
    ) -> NotificationResponse:
        """Create a notification."""
        notification = Notification(
            id=str(uuid.uuid4()),
            user_id=user_id,
            notification_type=notification_type,
            task_id=task_id,
            related_user_id=related_user_id,
            title=title,
            message=message,
            is_read=False,
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return NotificationResponse.from_orm(notification)

    @staticmethod
    def get_user_notifications(
        db: Session, user_id: str, unread_only: bool = False
    ) -> List[NotificationResponse]:
        """Get notifications for a user."""
        query = db.query(Notification).filter(Notification.user_id == user_id)

        if unread_only:
            query = query.filter(Notification.is_read == False)

        notifications = query.order_by(Notification.created_at.desc()).all()
        return [NotificationResponse.from_orm(n) for n in notifications]

    @staticmethod
    def mark_as_read(db: Session, notification_id: str, user_id: str) -> NotificationResponse:
        """Mark notification as read."""
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            raise ResourceNotFoundException("Notification", notification_id)

        if notification.user_id != user_id:
            from apps.backend.src.core.exceptions import AuthorizationException

            raise AuthorizationException("You can only mark your own notifications as read.")

        notification.is_read = True
        notification.read_at = datetime.utcnow()
        db.commit()
        db.refresh(notification)

        return NotificationResponse.from_orm(notification)

    @staticmethod
    def delete_notification(db: Session, notification_id: str, user_id: str) -> None:
        """Delete a notification."""
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            raise ResourceNotFoundException("Notification", notification_id)

        if notification.user_id != user_id:
            from apps.backend.src.core.exceptions import AuthorizationException

            raise AuthorizationException("You can only delete your own notifications.")

        db.delete(notification)
        db.commit()
