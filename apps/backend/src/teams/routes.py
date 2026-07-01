"""Teams routes."""

from typing import List

from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from apps.backend.src.auth.service import AuthService
from apps.backend.src.core.exceptions import AppException
from apps.backend.src.core.schemas import (
    TeamCreate,
    TeamDetailResponse,
    TeamResponse,
    TeamUpdate,
)
from apps.backend.src.db.database import get_db
from apps.backend.src.teams.service import TeamsService

router = APIRouter(prefix="/teams", tags=["teams"])
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


@router.get("", response_model=List[TeamResponse])
async def list_teams(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    """List teams for current user."""
    try:
        return TeamsService.list_teams(db, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_data: TeamCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new team."""
    try:
        return TeamsService.create_team(db, current_user.id, team_data)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=e.message)


@router.get("/{team_id}", response_model=TeamDetailResponse)
async def get_team(
    team_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get team details."""
    try:
        return TeamsService.get_team_details(db, team_id)
    except AppException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=e.message)


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: str,
    update_data: TeamUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update team."""
    try:
        return TeamsService.update_team(db, team_id, current_user.id, update_data)
    except AppException as e:
        from fastapi import HTTPException

        status_code = 404 if "not found" in e.message.lower() else 403
        raise HTTPException(status_code=status_code, detail=e.message)


@router.post("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_team_member(
    team_id: str,
    user_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add member to team."""
    try:
        TeamsService.add_member(db, team_id, user_id, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        status_code = 404 if "not found" in e.message.lower() else 400
        raise HTTPException(status_code=status_code, detail=e.message)


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_team_member(
    team_id: str,
    user_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove member from team."""
    try:
        TeamsService.remove_member(db, team_id, user_id, current_user.id)
    except AppException as e:
        from fastapi import HTTPException

        status_code = 404 if "not found" in e.message.lower() else 400
        raise HTTPException(status_code=status_code, detail=e.message)
