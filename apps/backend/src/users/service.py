"""Users service."""

from typing import Optional

from sqlalchemy.orm import Session

from apps.backend.src.core.exceptions import ResourceNotFoundException
from apps.backend.src.core.models import User
from apps.backend.src.core.schemas import (
    UserPreferences,
    UserProfileResponse,
    UserResponse,
    UserUpdate,
)


class UsersService:
    """Users service."""

    @staticmethod
    def get_user(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResourceNotFoundException("User", user_id)
        return user

    @staticmethod
    def update_profile(
        db: Session, user_id: str, update_data: UserUpdate
    ) -> UserResponse:
        """Update user profile."""
        user = UsersService.get_user(db, user_id)

        if update_data.display_name:
            user.display_name = update_data.display_name
        if update_data.avatar_url is not None:
            user.avatar_url = update_data.avatar_url
        if update_data.time_zone:
            user.time_zone = update_data.time_zone
        if update_data.language:
            user.language = update_data.language

        db.commit()
        db.refresh(user)

        return UserResponse.from_orm(user)

    @staticmethod
    def get_profile(db: Session, user_id: str) -> UserProfileResponse:
        """Get user profile with roles and teams."""
        user = UsersService.get_user(db, user_id)

        roles = []
        teams = []

        # Get roles from team memberships
        for team in user.teams:
            # Get role from team_members table
            from sqlalchemy import text

            from apps.backend.src.db.database import SessionLocal

            db_session = SessionLocal()
            try:
                result = db_session.execute(
                    text(
                        "SELECT role FROM team_members WHERE user_id = :user_id AND team_id = :team_id"
                    ),
                    {"user_id": user_id, "team_id": team.id},
                )
                row = result.first()
                if row:
                    roles.append(str(row[0]))
                teams.append(team.id)
            finally:
                db_session.close()

        return UserProfileResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            time_zone=user.time_zone,
            language=user.language,
            is_active=user.is_active,
            is_verified=user.is_verified,
            theme=user.theme,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            roles=roles or ["user"],
            teams=teams,
        )

    @staticmethod
    def update_preferences(
        db: Session, user_id: str, preferences: UserPreferences
    ) -> UserResponse:
        """Update user preferences."""
        user = UsersService.get_user(db, user_id)

        if preferences.theme:
            user.theme = preferences.theme
        if preferences.language:
            user.language = preferences.language
        if preferences.time_zone:
            user.time_zone = preferences.time_zone

        db.commit()
        db.refresh(user)

        return UserResponse.from_orm(user)

    @staticmethod
    def get_preferences(db: Session, user_id: str) -> UserPreferences:
        """Get user preferences."""
        user = UsersService.get_user(db, user_id)

        return UserPreferences(
            theme=user.theme,
            language=user.language,
            time_zone=user.time_zone,
            notification_preferences={
                "assignment": True,
                "updates": True,
                "comments": True,
                "mentions": True,
                "overdue": True,
            },
        )
