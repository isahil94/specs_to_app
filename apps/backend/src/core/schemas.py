"""Shared DTOs and schemas."""

from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, Field


# Error Response
class ErrorDetail(BaseModel):
    """Error detail."""

    field: Optional[str] = None
    message: str


class ErrorResponse(BaseModel):
    """Error response."""

    error_code: str
    message: str
    details: List[ErrorDetail] = []
    request_id: str


# User DTOs
class UserBase(BaseModel):
    """User base DTO."""

    email: EmailStr
    display_name: str


class UserCreate(UserBase):
    """User create DTO."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update DTO."""

    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    time_zone: Optional[str] = None
    language: Optional[str] = None


class UserPreferences(BaseModel):
    """User preferences DTO."""

    theme: Optional[str] = None
    language: Optional[str] = None
    time_zone: Optional[str] = None
    notification_preferences: Optional[dict] = None


class UserResponse(UserBase):
    """User response DTO."""

    id: str
    avatar_url: Optional[str] = None
    time_zone: str
    language: str
    is_active: bool
    is_verified: bool
    theme: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        """Pydantic config."""

        from_attributes = True


class UserProfileResponse(UserResponse):
    """User profile response DTO."""

    roles: List[str] = []
    teams: List[str] = []  # Team IDs


# Authentication DTOs
class AuthRegisterRequest(BaseModel):
    """Auth register request."""

    email: EmailStr
    password: str = Field(..., min_length=8)
    display_name: str
    remember_me: bool = False


class AuthLoginRequest(BaseModel):
    """Auth login request."""

    email: EmailStr
    password: str
    remember_me: bool = False


class AuthTokenResponse(BaseModel):
    """Auth token response."""

    user_id: str
    email: str
    display_name: str
    token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class AuthLoginResponse(BaseModel):
    """Auth login response."""

    user_id: str
    token: str
    expires_in: int
    roles: List[str]
    email: str


class AuthRecoverRequest(BaseModel):
    """Auth recover request."""

    email: EmailStr


class AuthResetRequest(BaseModel):
    """Auth reset request."""

    token: str
    new_password: str = Field(..., min_length=8)


# Task DTOs
class TaskCreate(BaseModel):
    """Task create DTO."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    assignee_id: Optional[str] = None
    due_date: Optional[datetime] = None
    labels: Optional[List[str]] = None
    team_id: Optional[str] = None
    attachments: Optional[List[str]] = None


class TaskUpdate(BaseModel):
    """Task update DTO."""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[str] = None
    due_date: Optional[datetime] = None
    labels: Optional[List[str]] = None


class TaskStatusUpdate(BaseModel):
    """Task status update DTO."""

    status: str
    comment: Optional[str] = None


class TaskResponse(BaseModel):
    """Task response DTO."""

    id: str
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    created_by_id: str
    assignee_id: Optional[str] = None
    team_id: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    is_archived: bool
    labels: Optional[List[str]] = None

    class Config:
        """Pydantic config."""

        from_attributes = True


class TaskListResponse(BaseModel):
    """Task list response DTO."""

    items: List[TaskResponse]
    total_count: int
    page: int
    page_size: int


class TaskDetailResponse(TaskResponse):
    """Task detail response DTO."""

    comments_count: int = 0


# Comment DTOs
class CommentCreate(BaseModel):
    """Comment create DTO."""

    content: str = Field(..., min_length=1)
    mentions: Optional[List[str]] = None
    attachments: Optional[List[str]] = None


class CommentResponse(BaseModel):
    """Comment response DTO."""

    id: str
    task_id: str
    author_id: str
    content: str
    mentions: Optional[List[str]] = None
    attachments: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


# Team DTOs
class TeamCreate(BaseModel):
    """Team create DTO."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    lead_user_id: str


class TeamUpdate(BaseModel):
    """Team update DTO."""

    name: Optional[str] = None
    description: Optional[str] = None
    lead_user_id: Optional[str] = None


class TeamResponse(BaseModel):
    """Team response DTO."""

    id: str
    name: str
    description: Optional[str] = None
    lead_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class TeamDetailResponse(TeamResponse):
    """Team detail response DTO."""

    members: List[UserResponse] = []


# Notification DTOs
class NotificationResponse(BaseModel):
    """Notification response DTO."""

    id: str
    user_id: str
    notification_type: str
    task_id: Optional[str] = None
    title: str
    message: str
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        """Pydantic config."""

        from_attributes = True


# Dashboard DTOs
class DashboardMetrics(BaseModel):
    """Dashboard metrics."""

    total_tasks: int
    completed_tasks: int
    overdue_tasks: int
    in_progress_tasks: int
    assigned_to_me: int


class DashboardResponse(BaseModel):
    """Dashboard response DTO."""

    metrics: DashboardMetrics
    recent_tasks: List[TaskResponse]
    overdue_tasks: List[TaskResponse]
    team_summary: List[dict]
