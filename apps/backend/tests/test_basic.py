"""Basic unit tests for backend modules."""

import pytest
from sqlalchemy.orm import Session

from apps.backend.src.auth.service import AuthService
from apps.backend.src.core.exceptions import ConflictException, ValidationException
from apps.backend.src.core.models import Task, TaskStatus, Team, User, UserRole
from apps.backend.src.core.schemas import (
    AuthLoginRequest,
    AuthRegisterRequest,
    TaskCreate,
    TeamCreate,
)
from apps.backend.src.core.security import validate_password_strength
from apps.backend.src.tasks.service import TasksService
from apps.backend.src.teams.service import TeamsService


def test_password_validation():
    """Test password validation rules."""
    # Valid password
    valid, msg = validate_password_strength("ValidPass123!")
    assert valid

    # Too short
    valid, msg = validate_password_strength("Short1!")
    assert not valid

    # No uppercase
    valid, msg = validate_password_strength("lowercase123!")
    assert not valid

    # No numbers
    valid, msg = validate_password_strength("NoNumbers!")
    assert not valid

    # No special chars
    valid, msg = validate_password_strength("NoSpecial123")
    assert not valid


def test_task_status_transitions():
    """Test valid task status transitions."""
    # Valid transitions
    assert TasksService._can_transition(TaskStatus.TODO, TaskStatus.IN_PROGRESS)
    assert TasksService._can_transition(TaskStatus.IN_PROGRESS, TaskStatus.REVIEW)
    assert TasksService._can_transition(TaskStatus.REVIEW, TaskStatus.DONE)
    assert TasksService._can_transition(TaskStatus.DONE, TaskStatus.ARCHIVED)

    # Invalid transitions
    assert not TasksService._can_transition(TaskStatus.DONE, TaskStatus.TODO)
    assert not TasksService._can_transition(TaskStatus.REVIEW, TaskStatus.TODO)
