# Backend Validation Rules

## Input Validation Layer

### Email Validation
- **Pattern**: RFC 5322 compliant email format
- **Uniqueness**: Enforced at database level (UNIQUE constraint)
- **Scope**: Case-insensitive comparison
- **Implementation**: Pydantic EmailStr validator
- **DTO Location**: UserCreate.email, AuthRegisterRequest.email, UserUpdate.email

### Password Validation
- **Minimum Length**: 8 characters
- **Character Requirements**:
  - At least 1 uppercase letter (A-Z)
  - At least 1 lowercase letter (a-z)
  - At least 1 digit (0-9)
  - At least 1 special character: `! @ # $ % ^ & * ( ) _ + - = [ ] { } | ; : , . < >`
- **Maximum Length**: 128 characters
- **Implementation**: `validate_password_strength()` in `core/security.py`
- **Location**: AuthRegisterRequest.password, UserUpdate.password
- **Error Type**: PasswordPolicyException (400 Bad Request)

### Task Title Validation
- **Required**: Yes (cannot be null or empty)
- **Type**: String
- **Length**: 1-255 characters
- **Trimming**: Leading/trailing whitespace removed
- **Implementation**: Pydantic Field with min_length=1, max_length=255
- **DTO Location**: TaskCreate.title, TaskUpdate.title

### Task Description Validation
- **Required**: No (optional field)
- **Type**: String
- **Length**: 0-5000 characters
- **Trimming**: Leading/trailing whitespace removed
- **Implementation**: Pydantic Field with max_length=5000
- **DTO Location**: TaskCreate.description, TaskUpdate.description

### Task Status Validation
- **Allowed Values**: `TODO`, `IN_PROGRESS`, `REVIEW`, `DONE`, `ARCHIVED`
- **Type**: Enum (TaskStatus)
- **State Machine**: See status-transition matrix in business-logic.md
- **Implementation**: Enum type in models.py, validated via `_can_transition()` in tasks/service.py
- **Error Type**: InvalidStatusTransitionException (400 Bad Request)

### Task Priority Validation
- **Allowed Values**: `LOW`, `MEDIUM`, `HIGH`, `URGENT`
- **Type**: Enum (TaskPriority)
- **Default**: MEDIUM
- **Implementation**: Enum type in models.py

### Task Due Date Validation
- **Required**: No (optional field)
- **Type**: DateTime (ISO 8601)
- **Constraint**: Must be in future (optional business rule)
- **Format**: `YYYY-MM-DDTHH:MM:SS.sssZ`
- **Implementation**: Pydantic datetime field
- **DTO Location**: TaskCreate.due_date, TaskUpdate.due_date

### Comment Content Validation
- **Required**: Yes
- **Type**: String
- **Length**: 1-10000 characters
- **Trimming**: Leading/trailing whitespace removed
- **Implementation**: Pydantic Field with min_length=1, max_length=10000
- **DTO Location**: CommentCreate.content

### Team Name Validation
- **Required**: Yes
- **Type**: String
- **Length**: 1-255 characters
- **Uniqueness**: Not enforced at database level (multiple teams can have same name)
- **Trimming**: Leading/trailing whitespace removed
- **Implementation**: Pydantic Field with min_length=1, max_length=255
- **DTO Location**: TeamCreate.name, TeamUpdate.name

### User Display Name Validation
- **Required**: No
- **Type**: String
- **Length**: 0-255 characters
- **Implementation**: Pydantic Field with max_length=255
- **DTO Location**: UserUpdate.display_name

## Pagination Validation

### Page Size Constraints
- **Minimum**: 1
- **Maximum**: 100
- **Default**: 50
- **Type**: Integer query parameter `page_size`
- **Implementation**: Pydantic Query with ge=1, le=100, default=50
- **Error Type**: ValidationException (400 Bad Request)

### Page Number Constraints
- **Minimum**: 1 (1-indexed)
- **Type**: Integer query parameter `page`
- **Default**: 1
- **Implementation**: Pydantic Query with ge=1, default=1

## Business Rule Validation

### Task State Transitions
**Validation Logic** (from tasks/service.py `_can_transition()`):
- From TODO: Can transition to IN_PROGRESS, ARCHIVED
- From IN_PROGRESS: Can transition to REVIEW, TODO, ARCHIVED
- From REVIEW: Can transition to DONE, IN_PROGRESS, ARCHIVED
- From DONE: Can transition to ARCHIVED only
- From ARCHIVED: Can transition to TODO only (restore)

**Error Type**: InvalidStatusTransitionException (400 Bad Request)  
**Implementation**: Service-layer validation before database update

### Task Access Control
**Validation Logic** (from tasks/service.py `_can_access_task()`):
- **Creator**: Can access own tasks
- **Assignee**: Can access assigned tasks
- **Team Member**: Can access tasks in their team (readonly unless assignee)
- **Admin**: Can access all tasks
- **Non-Member**: Denied access

**Error Type**: AuthorizationException (403 Forbidden)

### Team Membership Validation
- **Duplicate Check**: User cannot be added to team twice
- **Unique Constraint**: (team_id, user_id) composite key in database
- **Error Type**: ConflictException (409 Conflict)

### Comment Author Validation
- **Requirement**: Comment must belong to existing task
- **Requirement**: Author must be authenticated user
- **Requirement**: Author must have access to task
- **Validation**: Task existence check + access control check
- **Error Type**: ResourceNotFoundException or AuthorizationException

### Notification Owner Validation
- **Requirement**: User can only read/delete own notifications
- **Implementation**: Filter by `notification.user_id == current_user.id`
- **Error Type**: AuthorizationException (403 Forbidden)

### Account Lockout Validation
- **Rule**: Lock after 5 consecutive failed login attempts
- **Duration**: 15 minutes (900 seconds)
- **Check**: Compare current time with user.locked_until
- **Reset**: Failed counter resets on successful login
- **Error Type**: AccountLockedException (429 Too Many Requests)

### Email Uniqueness Validation
- **Scope**: All users across entire system
- **Implementation**: Database UNIQUE constraint on User.email
- **Constraint Type**: UNIQUE INDEX on email column
- **Error Type**: ConflictException (409 Conflict)
- **Trigger**: Registration, profile update email change

## DTO Validation Rules

### AuthRegisterRequest
```python
- email: EmailStr (required, must be valid email)
- password: str (required, must pass password strength rules)
- display_name: str (optional, max 255 chars)
```

### AuthLoginRequest
```python
- email: EmailStr (required)
- password: str (required)
```

### TaskCreate
```python
- title: str (required, 1-255 chars)
- description: str (optional, 0-5000 chars)
- priority: TaskPriority (optional, default=MEDIUM)
- due_date: datetime (optional)
- assignee_id: UUID (optional, must reference existing user)
- team_id: UUID (required, must reference existing team)
- labels: List[str] (optional, max 10 items, 50 chars each)
```

### TaskUpdate
```python
- title: str (optional, 1-255 chars if provided)
- description: str (optional, 0-5000 chars if provided)
- priority: TaskPriority (optional)
- status: TaskStatus (optional, must follow state machine)
- due_date: datetime (optional)
- assignee_id: UUID (optional, must reference existing user or null)
- labels: List[str] (optional, max 10 items, 50 chars each)
```

### CommentCreate
```python
- content: str (required, 1-10000 chars)
- mentions: List[UUID] (optional, must reference existing users)
- attachments: List[str] (optional, valid URLs)
```

### TeamCreate
```python
- name: str (required, 1-255 chars)
- description: str (optional, 0-5000 chars)
- lead_id: UUID (required, must reference existing active user)
```

### UserUpdate
```python
- display_name: str (optional, 0-255 chars)
- email: EmailStr (optional, must be unique if provided)
- avatar_url: str (optional, valid URL)
- time_zone: str (optional, valid IANA timezone)
- theme: str (optional, 'light' or 'dark')
- language: str (optional, ISO 639-1 code)
```

## Cross-Field Validation

### Task Assignment
- **Rule**: If assignee_id provided, must reference valid user
- **Rule**: Assignee must not be task creator (business rule - can be relaxed)
- **Rule**: Assignee must be member of task's team
- **Implementation**: Validate in tasks/service.py before database insert/update
- **Error Type**: ValidationException (400 Bad Request)

### Task Dates
- **Rule**: due_date must be after created_at (system rule)
- **Rule**: due_date should be in future (business preference, not enforced)
- **Implementation**: Validated in tasks/service.py

### User Timezone
- **Rule**: Must be valid IANA timezone string
- **Examples**: UTC, America/New_York, Europe/London, Asia/Tokyo
- **Validation**: Check against pytz or zoneinfo database
- **Error Type**: ValidationException (400 Bad Request)

## Null/Empty Validation

### Required Fields
- email: NOT NULL
- password_hash: NOT NULL
- task.title: NOT NULL
- task.team_id: NOT NULL
- task.created_by_id: NOT NULL
- comment.content: NOT NULL
- comment.task_id: NOT NULL
- comment.author_id: NOT NULL
- team.name: NOT NULL
- team.lead_id: NOT NULL

### Optional Fields (Can be NULL)
- task.description
- task.due_date
- task.assignee_id
- user.display_name
- user.avatar_url
- comment.attachments
- team.description

## Enum Validation

### TaskStatus Values
- `TODO` - Initial state
- `IN_PROGRESS` - Work started
- `REVIEW` - Awaiting review
- `DONE` - Completed
- `ARCHIVED` - Soft deleted

### TaskPriority Values
- `LOW` - Can wait
- `MEDIUM` - Standard priority (default)
- `HIGH` - Important
- `URGENT` - Immediate attention

### NotificationType Values
- `assignment` - Task assigned to user
- `updated` - Task modified
- `commented` - Comment added
- `mentioned` - User mentioned
- `overdue` - Task past due
- `reminder` - Scheduled reminder

### UserRole Values
- `admin` - Full system access
- `team_lead` - Team management
- `user` - Standard user (default)

## Request Validation Flow

```
HTTP Request
    ↓
FastAPI Parameter Validation (Path, Query, Header)
    ↓
Pydantic DTO Validation (Type, Format, Length)
    ↓
Service Layer Business Validation (State machine, Access control)
    ↓
Database Constraint Validation (Unique, Foreign key, NOT NULL)
    ↓
Success or Error Response
```

## Error Response Format

All validation errors return structured JSON:

```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Validation failed",
  "details": [
    {
      "field": "email",
      "message": "value is not a valid email address"
    }
  ],
  "request_id": "req-uuid"
}
```

## Database-Level Constraints

### Unique Constraints
- `UNIQUE(user.email)`
- `UNIQUE(team_members.team_id, team_members.user_id)`

### Foreign Key Constraints
- `task.created_by_id → user.id` (CASCADE on delete)
- `task.assignee_id → user.id` (SET NULL on delete)
- `task.team_id → team.id` (RESTRICT on delete)
- `comment.task_id → task.id` (CASCADE on delete)
- `comment.author_id → user.id` (SET NULL on delete)
- `notification.user_id → user.id` (CASCADE on delete)
- `team_members.user_id → user.id` (CASCADE on delete)
- `team_members.team_id → team.id` (CASCADE on delete)

### Check Constraints
- `user.login_attempts >= 0`
- `user.login_attempts <= 5`
- `CASE WHEN user.is_locked THEN user.locked_until IS NOT NULL ELSE TRUE END`

## Validation Performance

### Indexed Lookups
- User.email lookup: O(1) via unique index
- Task.id lookup: O(1) via primary key
- Comment.task_id lookup: O(log n) via index
- Notification.user_id lookup: O(log n) via index

### Bulk Validation
- List endpoint page_size validation: Happens before database query
- Filtering validation: Handled before WHERE clause generation

---

**Database constraints enforce final layer of validation**. Application must trust database constraints and handle constraint violation errors appropriately.
