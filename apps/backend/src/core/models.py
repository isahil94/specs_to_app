"""Core domain models."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "administrator"
    TEAM_LEAD = "team_lead"
    USER = "user"


class TaskStatus(str, Enum):
    """Task status enumeration."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    ARCHIVED = "archived"


class TaskPriority(str, Enum):
    """Task priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# Association table for team members
team_members = Table(
    "team_members",
    Base.metadata,
    Column("team_id", String(36), ForeignKey("teams.id"), primary_key=True),
    Column("user_id", String(36), ForeignKey("users.id"), primary_key=True),
    Column("role", SQLEnum(UserRole), default=UserRole.USER),
    Column("joined_at", DateTime, default=datetime.utcnow),
)


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(512), nullable=True)
    time_zone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    theme = Column(String(20), default="light")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    # Relationships
    tasks_owned = relationship("Task", foreign_keys="Task.created_by_id", back_populates="creator")
    tasks_assigned = relationship("Task", foreign_keys="Task.assignee_id", back_populates="assignee")
    teams = relationship("Team", secondary=team_members, back_populates="members")
    comments = relationship("Comment", back_populates="author")
    notifications = relationship("Notification", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_is_active", "is_active"),
    )


class Team(Base):
    """Team model."""

    __tablename__ = "teams"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    lead_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    members = relationship("User", secondary=team_members, back_populates="teams")
    tasks = relationship("Task", back_populates="team")
    lead = relationship("User", foreign_keys=[lead_id])

    __table_args__ = (
        Index("idx_team_lead_id", "lead_id"),
    )


class Task(Base):
    """Task model."""

    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO, index=True)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, index=True)
    created_by_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    assignee_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=True, index=True)
    due_date = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    archived_at = Column(DateTime, nullable=True)
    is_archived = Column(Boolean, default=False, index=True)
    labels = Column(String(512), nullable=True)  # Comma-separated labels

    # Relationships
    creator = relationship("User", foreign_keys=[created_by_id], back_populates="tasks_owned")
    assignee = relationship("User", foreign_keys=[assignee_id], back_populates="tasks_assigned")
    team = relationship("Team", back_populates="tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    history = relationship("TaskHistory", back_populates="task", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_task_status", "status"),
        Index("idx_task_created_by", "created_by_id"),
        Index("idx_task_assignee", "assignee_id"),
        Index("idx_task_team", "team_id"),
        Index("idx_task_created_at", "created_at"),
    )


class TaskHistory(Base):
    """Task history/audit model."""

    __tablename__ = "task_history"

    id = Column(String(36), primary_key=True, index=True)
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False)
    changed_by_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    field_name = Column(String(100), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    change_type = Column(String(20), nullable=False)  # created, updated, status_changed, archived
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    task = relationship("Task", back_populates="history")
    changed_by = relationship("User", foreign_keys=[changed_by_id])

    __table_args__ = (
        Index("idx_task_history_task_id", "task_id"),
        Index("idx_task_history_created_at", "created_at"),
    )


class Comment(Base):
    """Comment model."""

    __tablename__ = "comments"

    id = Column(String(36), primary_key=True, index=True)
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    mentions = Column(String(512), nullable=True)  # Comma-separated user IDs
    attachments = Column(String(512), nullable=True)  # Comma-separated attachment URLs
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")

    __table_args__ = (
        Index("idx_comment_task_id", "task_id"),
        Index("idx_comment_author_id", "author_id"),
    )


class Notification(Base):
    """Notification model."""

    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    notification_type = Column(String(50), nullable=False)  # assigned, updated, commented, mentioned, overdue
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=True)
    related_user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    read_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="notifications", foreign_keys=[user_id])
    task = relationship("Task", foreign_keys=[task_id])

    __table_args__ = (
        Index("idx_notification_user_id", "user_id"),
        Index("idx_notification_is_read", "is_read"),
        Index("idx_notification_created_at", "created_at"),
    )


class AuditLog(Base):
    """Audit log model."""

    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)  # user, task, team, etc.
    resource_id = Column(String(36), nullable=True)
    status = Column(String(20), nullable=False)  # success, failure
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    __table_args__ = (
        Index("idx_audit_log_user_id", "user_id"),
        Index("idx_audit_log_resource", "resource_type", "resource_id"),
        Index("idx_audit_log_created_at", "created_at"),
    )
