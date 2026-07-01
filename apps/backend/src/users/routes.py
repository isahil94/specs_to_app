"""Users routes."""

from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from apps.backend.src.auth.service import AuthService
from apps.backend.src.core.exceptions import AppException
from apps.backend.src.core.schemas import (
    UserPreferences,
    UserProfileResponse,
    UserResponse,
    UserUpdate,
)
from apps.backend.src.db.database import get_db
from apps.backend.src.users.service import UsersService

router = APIRouter(prefix="/users", tags=["users"])
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


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get current user profile."""
    try:
        return UsersService.get_profile(db, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=e.message)


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    update_data: UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user profile."""
    try:
        return UsersService.update_profile(db, current_user.id, update_data)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.get("/settings", response_model=UserPreferences)
async def get_user_settings(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get user settings."""
    try:
        return UsersService.get_preferences(db, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.put("/settings", response_model=UserPreferences)
async def update_user_settings(
    preferences: UserPreferences,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user settings."""
    try:
        UsersService.update_preferences(db, current_user.id, preferences)
        return UsersService.get_preferences(db, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)
