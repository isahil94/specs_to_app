"""Comments service."""

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from apps.backend.src.core.exceptions import (
    AuthorizationException,
    ResourceNotFoundException,
)
from apps.backend.src.core.models import Comment, Task
from apps.backend.src.core.schemas import CommentCreate, CommentResponse


class CommentsService:
    """Comments service."""

    @staticmethod
    def create_comment(
        db: Session, task_id: str, user_id: str, comment_data: CommentCreate
    ) -> CommentResponse:
        """Create a comment on a task."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ResourceNotFoundException("Task", task_id)

        comment = Comment(
            id=str(uuid.uuid4()),
            task_id=task_id,
            author_id=user_id,
            content=comment_data.content,
            mentions=",".join(comment_data.mentions) if comment_data.mentions else None,
            attachments=",".join(comment_data.attachments)
            if comment_data.attachments
            else None,
        )

        db.add(comment)
        db.commit()
        db.refresh(comment)

        return CommentResponse.from_orm(comment)

    @staticmethod
    def get_task_comments(db: Session, task_id: str) -> List[CommentResponse]:
        """Get all comments for a task."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ResourceNotFoundException("Task", task_id)

        comments = db.query(Comment).filter(Comment.task_id == task_id).all()
        return [CommentResponse.from_orm(comment) for comment in comments]

    @staticmethod
    def delete_comment(db: Session, comment_id: str, user_id: str) -> None:
        """Delete a comment (author only)."""
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise ResourceNotFoundException("Comment", comment_id)

        if comment.author_id != user_id:
            raise AuthorizationException("You can only delete your own comments.")

        db.delete(comment)
        db.commit()
