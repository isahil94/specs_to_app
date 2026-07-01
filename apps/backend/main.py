"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from apps.backend.src.auth.routes import router as auth_router
from apps.backend.src.comments.routes import router as comments_router
from apps.backend.src.core.config import settings
from apps.backend.src.core.exceptions import AppException
from apps.backend.src.db.database import init_db
from apps.backend.src.notifications.routes import router as notifications_router
from apps.backend.src.reports.routes import router as reports_router
from apps.backend.src.tasks.routes import router as tasks_router
from apps.backend.src.teams.routes import router as teams_router
from apps.backend.src.users.routes import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context."""
    # Startup
    init_db()
    print("Database initialized")
    yield
    # Shutdown
    print("Application shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Task Management API Backend",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle application exceptions."""
    return JSONResponse(
        status_code=400,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "details": [],
            "request_id": request.headers.get("X-Request-ID", "unknown"),
        },
    )


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# API Routes
@app.get("/", tags=["root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Task Management API",
        "version": settings.APP_VERSION,
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "tasks": "/tasks",
            "teams": "/teams",
            "notifications": "/notifications",
            "reports": "/reports",
        },
    }


# Include routers
app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(users_router, prefix=settings.API_PREFIX)
app.include_router(tasks_router, prefix=settings.API_PREFIX)
app.include_router(teams_router, prefix=settings.API_PREFIX)
app.include_router(comments_router, prefix=settings.API_PREFIX)
app.include_router(notifications_router, prefix=settings.API_PREFIX)
app.include_router(reports_router, prefix=settings.API_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
