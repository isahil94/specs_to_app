"""Reports routes."""

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from apps.backend.src.auth.service import AuthService
from apps.backend.src.core.schemas import DashboardResponse
from apps.backend.src.db.database import get_db
from apps.backend.src.reports.service import ReportsService

router = APIRouter(prefix="/reports", tags=["reports"])
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


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get dashboard metrics."""
    return ReportsService.get_dashboard(db, current_user.id)


@router.get("/workload/me", response_model=dict)
async def get_my_workload(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get current user workload."""
    return ReportsService.get_user_workload(db, current_user.id)


@router.get("/workload/team/{team_id}", response_model=dict)
async def get_team_workload(
    team_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get team workload."""
    return ReportsService.get_team_workload(db, team_id)
