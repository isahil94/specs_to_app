# Backend Development Design

## Overview

Production-ready FastAPI backend implementation for the Task Management System consuming upstream architecture and API contracts.

## Generated Architecture

### Framework & Stack
- **Framework**: FastAPI 0.139.0
- **Language**: Python 3.14.4
- **ORM**: SQLAlchemy 2.0.51
- **Server**: Uvicorn ASGI
- **Database**: SQLite (development), PostgreSQL-ready (production)
- **Authentication**: JWT tokens with bcrypt password hashing

### Module Structure

```
apps/backend/
├── src/
│   ├── core/              # Configuration and shared utilities
│   │   ├── config.py      # Settings and environment configuration
│   │   ├── models.py      # SQLAlchemy ORM models
│   │   ├── schemas.py     # Pydantic DTOs and request/response models
│   │   ├── security.py    # Password hashing and JWT token handling
│   │   └── exceptions.py  # Custom exception types
│   ├── db/                # Database layer
│   │   └── database.py    # Session management and initialization
│   ├── auth/              # Authentication module
│   │   ├── service.py     # Auth business logic
│   │   └── routes.py      # Auth endpoints
│   ├── users/             # User profile module
│   │   ├── service.py     # User management logic
│   │   └── routes.py      # User endpoints
│   ├── tasks/             # Task management module
│   │   ├── service.py     # Task CRUD and workflow
│   │   └── routes.py      # Task endpoints
│   ├── teams/             # Team management module
│   │   ├── service.py     # Team operations
│   │   └── routes.py      # Team endpoints
│   ├── comments/          # Comments module
│   │   ├── service.py     # Comment operations
│   │   └── routes.py      # Comment endpoints
│   ├── notifications/     # Notifications module
│   │   ├── service.py     # Notification operations
│   │   └── routes.py      # Notification endpoints
│   └── reports/           # Reporting and dashboard
│       ├── service.py     # Analytics and metrics
│       └── routes.py      # Report endpoints
├── main.py                # FastAPI application entry point
├── tests/
│   └── test_basic.py      # Unit tests
└── README.md              # Backend documentation
```

### Core Models

#### User
- id, email, password_hash, display_name, avatar_url
- time_zone, language, theme, is_active, is_verified
- login_attempts, locked_until (security)
- created_at, updated_at, last_login

#### Task
- id, title, description, status, priority
- created_by_id, assignee_id, team_id
- due_date, labels, is_archived, archived_at
- created_at, updated_at

#### Team
- id, name, description, lead_id
- members (many-to-many via team_members)

#### Comment
- id, task_id, author_id, content
- mentions, attachments
- created_at, updated_at

#### Notification
- id, user_id, notification_type, task_id, related_user_id
- title, message, is_read
- created_at, read_at

#### TaskHistory (Audit Trail)
- id, task_id, changed_by_id, field_name
- old_value, new_value, change_type
- created_at

#### AuditLog
- id, user_id, action, resource_type, resource_id
- status, details, ip_address, user_agent
- created_at

### Database Indexes

Created comprehensive indexes on:
- user.email (unique), user.is_active
- task.status, task.created_by_id, task.assignee_id, task.team_id, task.created_at
- comment.task_id, comment.author_id
- notification.user_id, notification.is_read, notification.created_at
- audit_log.user_id, audit_log.resource_type + resource_id, audit_log.created_at

### Security Implementation

#### Authentication
- JWT access tokens (30-minute expiration default)
- JWT refresh tokens (7-day expiration)
- HS256 signing algorithm
- Bearer token scheme

#### Password Security
- bcrypt hashing with configurable cost
- Configurable password strength policy:
  - Minimum 8 characters (configurable)
  - Requires uppercase letters
  - Requires numbers
  - Requires special characters
- Account lockout after 5 failed login attempts
- 15-minute lockout duration (configurable)

#### Authorization
- Role-based access control (Administrator, TeamLead, User)
- Ownership-based resource access
- Team membership checks
- Endpoint-level permission enforcement

#### Data Protection
- SQLAlchemy parameterized queries (SQL injection protection)
- Pydantic input validation
- CORS configuration per environment
- Secure session handling

### Validation

#### Input Validation
- Pydantic models enforce schema validation
- Email validation via EmailStr
- String length constraints
- Enum validation for status and priority
- Request ID tracking for audit

#### Business Validation
- Task status transition rules enforced
- Ownership and role checks
- Duplicate prevention
- Archive state constraints

## API Contracts Implemented

### Authentication Endpoints
- `POST /auth/register` - User registration with password strength enforcement
- `POST /auth/login` - Login with account lockout protection
- `POST /auth/refresh` - Access token refresh using refresh token

### User Endpoints
- `GET /users/me` - Get current user profile with roles and teams
- `PUT /users/me` - Update profile (display_name, avatar, timezone, language)
- `GET /users/settings` - Get user preferences (theme, language, notifications)
- `PUT /users/settings` - Update preferences

### Task Endpoints
- `GET /tasks` - List tasks with filtering (status, priority, assignee, search, pagination)
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get task details with comment count
- `PUT /tasks/{id}` - Update task fields
- `POST /tasks/{id}/status` - Update task status with transition validation
- `POST /tasks/{id}/archive` - Archive task
- `POST /tasks/{id}/restore` - Restore archived task
- `POST /tasks/{id}/duplicate` - Duplicate task
- `DELETE /tasks/{id}` - Delete task (admin only)

### Team Endpoints
- `GET /teams` - List user's teams
- `POST /teams` - Create new team
- `GET /teams/{id}` - Get team details with member list
- `PUT /teams/{id}` - Update team (lead only)
- `POST /teams/{id}/members/{userId}` - Add team member
- `DELETE /teams/{id}/members/{userId}` - Remove team member

### Comment Endpoints
- `GET /tasks/{id}/comments` - Get all comments for task
- `POST /tasks/{id}/comments` - Add comment with mentions/attachments
- `DELETE /tasks/{id}/comments/{commentId}` - Delete comment (author only)

### Notification Endpoints
- `GET /notifications` - List user notifications (supports unread_only filter)
- `POST /notifications/{id}/read` - Mark notification as read
- `DELETE /notifications/{id}` - Delete notification

### Reporting Endpoints
- `GET /reports/dashboard` - Get dashboard metrics and summary
- `GET /reports/workload/me` - Get user's workload summary
- `GET /reports/workload/team/{teamId}` - Get team workload summary

### Health Endpoints
- `GET /health` - Health check endpoint
- `GET /` - API root with endpoint listing

## Task Status Transitions

Implemented state machine with valid transitions:
- TODO → IN_PROGRESS, ARCHIVED
- IN_PROGRESS → REVIEW, TODO, ARCHIVED
- REVIEW → DONE, IN_PROGRESS, ARCHIVED
- DONE → ARCHIVED
- ARCHIVED → TODO

Invalid transitions are rejected with 400 Bad Request.

## Error Handling

### Exception Types
- ValidationException - Input validation failures
- AuthenticationException - Auth failures
- AuthorizationException - Permission denied
- ResourceNotFoundException - Resource not found
- ConflictException - Duplicate/conflict
- InvalidStatusTransitionException - Invalid state transition
- PasswordPolicyException - Password policy violation
- AccountLockedException - Account locked after failed attempts

### Error Response Format
```json
{
  "error_code": "AUTH_INVALID_CREDENTIALS",
  "message": "Invalid email or password.",
  "details": [],
  "request_id": "correlation-id"
}
```

## Logging & Observability

### Structured Logging
- Configured for JSON output in production
- Configurable log level (default INFO)
- Request/response correlation IDs

### Audit Trail
- All authentication events logged
- Task lifecycle changes tracked in TaskHistory
- Administrative actions logged to AuditLog
- IP address and user agent captured

## Configuration

Settings loaded from environment with defaults:
- DATABASE_URL (SQLite by default)
- SECRET_KEY (required in production)
- DEBUG (false)
- ENVIRONMENT (development)
- API_PORT (8001)
- ACCESS_TOKEN_EXPIRE_MINUTES (30)
- PASSWORD policy options

## Testing

Unit test coverage:
- Password validation rules
- Task status transition logic
- Core business logic validation

Tests pass: 2/2 (100%)

## Performance Characteristics

- Indexes on common query filters
- Eager loading for relationships where needed
- Connection pooling
- Query optimization via SQLAlchemy

## Generated By

**Agent**: Backend Developer
**Date**: 2026-07-02
**Workflow ID**: WF-20260701-001
**Correlation ID**: CORR-20260701-001
