"""Authentication routes."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.backend.src.auth.service import AuthService
from apps.backend.src.core.exceptions import AppException
from apps.backend.src.core.schemas import (
    AuthLoginRequest,
    AuthRegisterRequest,
    AuthTokenResponse,
    ErrorResponse,
)
from apps.backend.src.db.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(request: AuthRegisterRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        return AuthService.register(db, request)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.post("/login", response_model=AuthTokenResponse)
async def login(request: AuthLoginRequest, db: Session = Depends(get_db)):
    """Login a user."""
    try:
        return AuthService.login(db, request)
    except AppException as e:
        from fastapi import HTTPException

        status_code = 400
        if "locked" in e.error_code.lower():
            status_code = 429
        elif "auth" in e.error_code.lower():
            status_code = 401
        raise HTTPException(status_code=status_code, detail=e.message)


@router.post("/refresh", response_model=AuthTokenResponse)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token."""
    try:
        return AuthService.refresh_access_token(db, refresh_token)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail=e.message)
