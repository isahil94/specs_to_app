"""Custom exceptions."""

from fastapi import HTTPException, status


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR"):
        """Initialize exception."""
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationException(AppException):
    """Validation exception."""

    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        """Initialize exception."""
        super().__init__(message, error_code)


class AuthenticationException(AppException):
    """Authentication exception."""

    def __init__(
        self, message: str = "Invalid credentials", error_code: str = "AUTH_FAILED"
    ):
        """Initialize exception."""
        super().__init__(message, error_code)


class AuthorizationException(AppException):
    """Authorization exception."""

    def __init__(
        self, message: str = "Unauthorized", error_code: str = "AUTH_UNAUTHORIZED"
    ):
        """Initialize exception."""
        super().__init__(message, error_code)


class ResourceNotFoundException(AppException):
    """Resource not found exception."""

    def __init__(
        self, resource_type: str, resource_id: str, error_code: str = "NOT_FOUND"
    ):
        """Initialize exception."""
        message = f"{resource_type} with id {resource_id} not found."
        super().__init__(message, error_code)


class ConflictException(AppException):
    """Conflict exception."""

    def __init__(self, message: str, error_code: str = "CONFLICT"):
        """Initialize exception."""
        super().__init__(message, error_code)


class InvalidStatusTransitionException(AppException):
    """Invalid status transition exception."""

    def __init__(
        self, current_status: str, target_status: str, reason: str = ""
    ):
        """Initialize exception."""
        message = f"Cannot transition from {current_status} to {target_status}."
        if reason:
            message += f" {reason}"
        super().__init__(message, "INVALID_STATUS_TRANSITION")


class PasswordPolicyException(AppException):
    """Password policy exception."""

    def __init__(self, message: str):
        """Initialize exception."""
        super().__init__(message, "PASSWORD_POLICY_VIOLATION")


class AccountLockedException(AppException):
    """Account locked exception."""

    def __init__(self, locked_until: str):
        """Initialize exception."""
        message = f"Account is locked until {locked_until}."
        super().__init__(message, "ACCOUNT_LOCKED")


def http_exception(status_code: int, detail: str) -> HTTPException:
    """Create HTTP exception."""
    return HTTPException(status_code=status_code, detail=detail)
