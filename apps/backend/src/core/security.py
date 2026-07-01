"""Security utilities."""

import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from apps.backend.src.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password."""
    return pwd_context.verify(plain_password, hashed_password)


# JWT Token handling
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode JWT token."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def generate_random_token(length: int = 32) -> str:
    """Generate random token."""
    return secrets.token_urlsafe(length)


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength."""
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        return (
            False,
            f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters.",
        )

    if settings.PASSWORD_REQUIRE_UPPERCASE and not any(
        c.isupper() for c in password
    ):
        return False, "Password must contain at least one uppercase letter."

    if settings.PASSWORD_REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."

    if settings.PASSWORD_REQUIRE_SPECIAL and not any(
        c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password
    ):
        return False, "Password must contain at least one special character."

    return True, None
