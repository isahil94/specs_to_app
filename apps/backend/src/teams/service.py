"""Teams service."""

import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from apps.backend.src.core.exceptions import (
    AuthorizationException,
    ConflictException,
    ResourceNotFoundException,
)
from apps.backend.src.core.models import Team, User, team_members
from apps.backend.src.core.schemas import (
    TeamCreate,
    TeamDetailResponse,
    TeamResponse,
    TeamUpdate,
)


class TeamsService:
    """Teams service."""

    @staticmethod
    def create_team(db: Session, creator_id: str, team_data: TeamCreate) -> TeamResponse:
        """Create a new team."""
        team = Team(
            id=str(uuid.uuid4()),
            name=team_data.name,
            description=team_data.description,
            lead_id=team_data.lead_user_id,
        )

        db.add(team)
        db.flush()

        # Add creator as member
        creator = db.query(User).filter(User.id == creator_id).first()
        if creator:
            team.members.append(creator)

        db.commit()
        db.refresh(team)

        return TeamResponse.from_orm(team)

    @staticmethod
    def get_team(db: Session, team_id: str) -> Optional[Team]:
        """Get team by ID."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise ResourceNotFoundException("Team", team_id)
        return team

    @staticmethod
    def list_teams(db: Session, user_id: str) -> List[TeamResponse]:
        """List teams for a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResourceNotFoundException("User", user_id)

        teams = user.teams if user.teams else []
        return [TeamResponse.from_orm(team) for team in teams]

    @staticmethod
    def get_team_details(db: Session, team_id: str) -> TeamDetailResponse:
        """Get team details with members."""
        team = TeamsService.get_team(db, team_id)

        return TeamDetailResponse(
            id=team.id,
            name=team.name,
            description=team.description,
            lead_id=team.lead_id,
            created_at=team.created_at,
            updated_at=team.updated_at,
            members=[
                {
                    "id": member.id,
                    "email": member.email,
                    "display_name": member.display_name,
                    "avatar_url": member.avatar_url,
                    "time_zone": member.time_zone,
                    "language": member.language,
                    "is_active": member.is_active,
                    "is_verified": member.is_verified,
                    "theme": member.theme,
                    "created_at": member.created_at,
                    "updated_at": member.updated_at,
                }
                for member in team.members
            ],
        )

    @staticmethod
    def update_team(
        db: Session, team_id: str, user_id: str, update_data: TeamUpdate
    ) -> TeamResponse:
        """Update team."""
        team = TeamsService.get_team(db, team_id)

        # Check authorization (only lead can update)
        if team.lead_id != user_id:
            raise AuthorizationException("Only team lead can update team.")

        if update_data.name:
            team.name = update_data.name
        if update_data.description is not None:
            team.description = update_data.description
        if update_data.lead_user_id:
            team.lead_id = update_data.lead_user_id

        db.commit()
        db.refresh(team)

        return TeamResponse.from_orm(team)

    @staticmethod
    def add_member(db: Session, team_id: str, user_id: str, lead_id: str) -> None:
        """Add member to team."""
        team = TeamsService.get_team(db, team_id)

        # Check authorization
        if team.lead_id != lead_id:
            raise AuthorizationException("Only team lead can add members.")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResourceNotFoundException("User", user_id)

        if user in team.members:
            raise ConflictException("User is already a member of this team.")

        team.members.append(user)
        db.commit()

    @staticmethod
    def remove_member(db: Session, team_id: str, user_id: str, lead_id: str) -> None:
        """Remove member from team."""
        team = TeamsService.get_team(db, team_id)

        # Check authorization
        if team.lead_id != lead_id:
            raise AuthorizationException("Only team lead can remove members.")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResourceNotFoundException("User", user_id)

        if user not in team.members:
            raise ConflictException("User is not a member of this team.")

        team.members.remove(user)
        db.commit()
