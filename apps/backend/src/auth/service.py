"""Authentication service."""

import uuid
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from apps.backend.src.core.config import settings
from apps.backend.src.core.exceptions import (
    AccountLockedException,
    AuthenticationException,
    ConflictException,
    PasswordPolicyException,
    ValidationException,
)
from apps.backend.src.core.models import User, UserRole
from apps.backend.src.core.schemas import (
    AuthLoginRequest,
    AuthRegisterRequest,
    AuthTokenResponse,
)
from apps.backend.src.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    validate_password_strength,
    verify_password,
)


class AuthService:
    """Authentication service."""

    @staticmethod
    def register(db: Session, request: AuthRegisterRequest) -> AuthTokenResponse:
        """Register a new user."""
        # Validate password strength
        is_valid, error_msg = validate_password_strength(request.password)
        if not is_valid:
            raise PasswordPolicyException(error_msg)

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise ConflictException(
                f"User with email {request.email} already exists.",
                "USER_ALREADY_EXISTS",
            )

        # Create new user
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            email=request.email,
            display_name=request.display_name,
            password_hash=hash_password(request.password),
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Generate tokens
        access_token = create_access_token({"sub": user.id, "email": user.email})
        refresh_token = create_refresh_token({"sub": user.id})

        return AuthTokenResponse(
            user_id=user.id,
            email=user.email,
            display_name=user.display_name,
            token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token,
        )

    @staticmethod
    def login(db: Session, request: AuthLoginRequest) -> AuthTokenResponse:
        """Login a user."""
        # Find user by email
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            raise AuthenticationException("Invalid email or password.")

        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise AccountLockedException(user.locked_until.isoformat())

        # Verify password
        if not verify_password(request.password, user.password_hash):
            user.login_attempts += 1
            if user.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                user.locked_until = datetime.utcnow() + timedelta(
                    minutes=settings.LOCKOUT_DURATION_MINUTES
                )
            db.commit()
            raise AuthenticationException("Invalid email or password.")

        # Reset login attempts on successful login
        user.login_attempts = 0
        user.last_login = datetime.utcnow()
        db.commit()

        # Generate tokens
        access_token = create_access_token({"sub": user.id, "email": user.email})
        refresh_token = create_refresh_token({"sub": user.id})

        return AuthTokenResponse(
            user_id=user.id,
            email=user.email,
            display_name=user.display_name,
            token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token,
        )

    @staticmethod
    def verify_token(db: Session, token: str) -> Optional[User]:
        """Verify and decode token, return user if valid."""
        from apps.backend.src.core.security import decode_token

        payload = decode_token(token)
        if not payload:
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            return None

        return user

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> AuthTokenResponse:
        """Refresh access token."""
        from apps.backend.src.core.security import decode_token

        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationException("Invalid refresh token.")

        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AuthenticationException("User not found.")

        # Generate new access token
        access_token = create_access_token({"sub": user.id, "email": user.email})

        return AuthTokenResponse(
            user_id=user.id,
            email=user.email,
            display_name=user.display_name,
            token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    @staticmethod
    def logout(db: Session, user: User) -> None:
        """Logout a user (placeholder for token blacklisting if needed)."""
        pass
