# Backend Service Integration & Implementation

## Service Architecture

### Layered Architecture
```
Routes (Endpoint Handlers)
    ↓ (FastAPI dependencies inject services)
Services (Business Logic)
    ↓ (Service methods call database layer)
ORM/Models (SQLAlchemy)
    ↓
Database (SQLite/PostgreSQL)
```

## Service Interaction Map

### Authentication Service (auth/service.py)

**Dependencies**:
- User model (read/write)
- Security module (password hashing, JWT)

**Key Methods & Interactions**:

| Method | Calls | Interacts With | Database Operations |
|--------|-------|---|---|
| `register(request)` | security.hash_password, security.create_access_token, security.create_refresh_token | User model | INSERT user, return tokens |
| `login(request)` | security.verify_password, security.create_tokens | User model | SELECT user, UPDATE login_attempts, return tokens |
| `verify_token(token)` | security.decode_token | User model | SELECT user by id |
| `refresh_access_token(refresh_token)` | security.decode_token, security.create_access_token | User model | SELECT user, return new token |

**Integration Points**:
- Called by: auth/routes.py
- Provides: JWT tokens for all protected endpoints
- Used by: get_current_user dependency

---

### Users Service (users/service.py)

**Dependencies**:
- User model (read/write)
- Team model (read)

**Key Methods & Interactions**:

| Method | Returns | Queries | Database Impact |
|--------|---------|---------|---|
| `get_user(user_id)` | User entity | Single SELECT by id | Read-only |
| `update_profile(user_id, update_data)` | Updated user | SELECT + UPDATE | Modify user record |
| `get_profile(user_id)` | User + roles + teams | SELECT user, SELECT team_members, SELECT teams | Read-only, 3 queries |
| `update_preferences(user_id, prefs)` | Updated user | SELECT + UPDATE | Modify user preferences |
| `get_preferences(user_id)` | Preferences dict | SELECT user | Read-only |

**Integration Points**:
- Depends on: Authentication (get_current_user)
- Called by: users/routes.py
- No downstream dependencies (doesn't call other services)

---

### Tasks Service (tasks/service.py)

**Dependencies**:
- Task model (read/write)
- TaskHistory model (write-only)
- Comment model (read)
- User model (read)
- Team model (read)

**Key Methods & Interactions**:

| Method | Flow | Service Calls | Database Operations |
|--------|------|---|---|
| `create_task(team_id, request, creator_id)` | Validate team exists → Create task → Create TaskHistory | None (direct queries) | INSERT task, INSERT task_history |
| `list_tasks(team_id, filters)` | Query by team_id + filters → Apply pagination | None | SELECT tasks with filters |
| `get_task(task_id, user_id)` | Check access control → Return task | _can_access_task() | SELECT task, evaluate access |
| `update_task(task_id, update_data, user_id)` | Check access → Validate fields → Update → Create history | _can_access_task() | UPDATE task, INSERT task_history |
| `update_task_status(task_id, new_status, user_id)` | Check access → Validate transition → Update → Create history | _can_transition() | UPDATE task.status, INSERT task_history |
| `archive_task(task_id, user_id)` | Check access → Set is_archived=true → Create history | _can_access_task() | UPDATE task, INSERT task_history |
| `restore_task(task_id, user_id)` | Check access → Set status=TODO, is_archived=false → Create history | _can_access_task() | UPDATE task, INSERT task_history |
| `duplicate_task(task_id, user_id)` | Check access → Copy task data → Create new task | _can_access_task() | INSERT new task, INSERT task_history |
| `delete_task(task_id, user_id)` | Check admin role → Permanent delete | None | DELETE task (hard delete) |

**Helper Methods**:
- `_can_transition(current_status, new_status)` - State machine validation (local, no DB)
- `_can_access_task(task, user_id, user_role)` - Authorization check (local, no DB)

**Integration Points**:
- Called by: tasks/routes.py
- Depends on: Authentication (get_current_user)
- Stores history: TaskHistory model for audit trail
- Related: Comments service (reads comments for task)

---

### Teams Service (teams/service.py)

**Dependencies**:
- Team model (read/write)
- User model (read)
- team_members association (read/write)

**Key Methods & Interactions**:

| Method | Flow | Database Operations |
|--------|------|---|
| `create_team(request, creator_id)` | Create team → Add creator as member | INSERT team, INSERT team_members |
| `get_team(team_id)` | SELECT team | Read-only |
| `list_teams(user_id)` | SELECT teams where user is member (via team_members) | SELECT teams with JOIN |
| `get_team_details(team_id)` | SELECT team + members | SELECT team, SELECT team_members, SELECT users |
| `update_team(team_id, update_data)` | Validate lead exists → UPDATE team | UPDATE team |
| `add_member(team_id, user_id, role)` | Check not duplicate → INSERT team_members | INSERT team_members |
| `remove_member(team_id, user_id)` | DELETE team_members | DELETE team_members |

**Duplicate Prevention**:
- Composite UNIQUE constraint on (team_id, user_id) in team_members table

**Integration Points**:
- Called by: teams/routes.py
- Depends on: Authentication, Task service (for team tasks)
- Used by: Tasks service (validates team_id)

---

### Comments Service (comments/service.py)

**Dependencies**:
- Comment model (read/write)
- Task model (read)
- User model (read)
- Notifications service (async trigger)

**Key Methods & Interactions**:

| Method | Flow | Triggers |
|--------|------|---|
| `create_comment(task_id, request, author_id)` | Validate task exists → Validate access → Create comment → Generate notifications | Trigger: Notifications for mentions, task watchers |
| `get_task_comments(task_id)` | SELECT comments for task | Read-only |
| `delete_comment(comment_id, user_id)` | Validate author → DELETE comment | Hard delete |

**Mention Processing**:
- Parse mentions from content (user IDs)
- Create notification for each mentioned user
- Store mentions array in comment.mentions

**Integration Points**:
- Called by: tasks/routes.py (via GET /tasks/{id}/comments)
- Depends on: Task service (validates access)
- Triggers: Notifications service (create notifications)

---

### Notifications Service (notifications/service.py)

**Dependencies**:
- Notification model (read/write)
- User model (read)
- Task model (read)

**Key Methods & Interactions**:

| Method | Flow | Database Operations |
|--------|------|---|
| `create_notification(user_id, type, task_id, message)` | INSERT notification | INSERT notification |
| `get_user_notifications(user_id, unread_only)` | SELECT notifications for user (filtered by is_read) | SELECT with WHERE |
| `mark_as_read(notification_id, user_id)` | UPDATE is_read=true, set read_at | UPDATE notification |
| `delete_notification(notification_id, user_id)` | DELETE notification | DELETE notification |

**Notification Triggers**:
- Task assignment → create notification
- Task status change → create notification for watchers
- Comment added → create notification for mentions and task watchers
- Task overdue → scheduled notification (future feature)

**Integration Points**:
- Called by: Comments service (mentions)
- Called by: Tasks service (assignment, status changes) [async, future]
- Called by: notifications/routes.py

---

### Reports Service (reports/service.py)

**Dependencies**:
- Task model (read)
- User model (read)
- Team model (read)

**Key Methods & Interactions**:

| Method | Queries | Aggregations |
|--------|---------|---|
| `get_dashboard(user_id)` | SELECT tasks for user (owner or assignee) | COUNT by status, COUNT overdue, get recent 10, get overdue |
| `get_user_workload(user_id)` | SELECT assigned tasks | GROUP by status, GROUP by priority, calculate completion % |
| `get_team_workload(team_id)` | SELECT tasks in team | COUNT by status, calculate metrics |

**Aggregation Operations** (all local, post-query):
- Total tasks count
- Completed tasks count
- Overdue tasks count
- Completion percentage
- Recent tasks (order by updated_at DESC, limit 10)

**Integration Points**:
- Called by: reports/routes.py
- Depends on: Task service models
- Read-only operations

---

## Data Flow Examples

### Use Case 1: User Registers
```
POST /auth/register
    ↓
routes.auth.register()
    ↓
AuthService.register(email, password, display_name)
    ↓
security.hash_password(password)  → bcrypt hash
security.create_access_token()    → JWT token
security.create_refresh_token()   → JWT token
    ↓
INSERT User(email, password_hash, ...)
    ↓
Response: { access_token, refresh_token, user }
```

### Use Case 2: Create and Assign Task
```
POST /tasks
    ↓
routes.tasks.create_task()
    ↓
TaskService.create_task(title, assignee_id, team_id, ...)
    ↓
Validate team exists (SELECT)
Validate assignee exists (SELECT)
Check creator access to team (SELECT team_members)
    ↓
INSERT Task(title, created_by_id, assignee_id, team_id, ...)
INSERT TaskHistory(task_id, field_name, old_value, new_value, 'created')
    ↓
[Async] NotificationService.create_notification(assignee_id, 'assignment', task_id)
    ↓
Response: { task_id, status, ... }
```

### Use Case 3: Update Task Status (with state machine)
```
POST /tasks/{id}/status
    ↓
routes.tasks.update_task_status(new_status)
    ↓
TaskService.update_task_status(task_id, new_status, user_id)
    ↓
SELECT task
_can_access_task(task, user_id)  → AuthorizationException if denied
_can_transition(old_status, new_status) → InvalidStatusTransitionException if invalid
    ↓
UPDATE Task(status = new_status, updated_at = now)
INSERT TaskHistory(task_id, 'status', old_value, new_value, 'status_changed')
    ↓
[Async] NotificationService.create_notification(...) for watchers
    ↓
Response: { task, updated }
```

### Use Case 4: Comment with Mentions
```
POST /tasks/{id}/comments
    ↓
routes.comments.create_comment(content, mentions=[user_id1, user_id2])
    ↓
CommentService.create_comment(task_id, content, mentions, author_id)
    ↓
SELECT task
_can_access_task(task, author_id)  → AuthorizationException if denied
Validate mentioned users exist (SELECT users WHERE id IN (...))
    ↓
INSERT Comment(task_id, content, author_id, mentions=[...], ...)
    ↓
FOR each mentioned_user_id:
    NotificationService.create_notification(mentioned_user_id, 'mentioned', task_id, comment_id)
NotificationService.create_notification(task_owner_id, 'commented', task_id, comment_id)
    ↓
Response: { comment }
```

---

## Service Call Dependencies

### Synchronous Dependencies (Blocking)
- Auth service → Security module (password hashing)
- Tasks service → Tasks model, TaskHistory model
- Teams service → Teams model, team_members table
- Comments service → Comments model, Tasks model (validation)
- Notifications service → Notifications model (write-only)
- Reports service → Tasks model (read aggregations)

### Asynchronous/Deferred Dependencies (Future)
- Comments service → Notifications service (mention notifications)
- Tasks service → Notifications service (assignment, status change notifications)

---

## Error Handling Across Services

### Service Error Propagation
```
Service Method
    ↓
Catch ORM Exception
    ↓
Convert to AppException subclass
    ↓
Return to Routes Layer
    ↓
HTTPException Handler (middleware)
    ↓
JSON Error Response
```

### Common Exception Mappings

| ORM Exception | Service Exception | HTTP Status |
|---|---|---|
| IntegrityError (UNIQUE) | ConflictException | 409 |
| IntegrityError (FK) | ResourceNotFoundException | 404 |
| NoResultFound | ResourceNotFoundException | 404 |
| InvalidStatusTransition | InvalidStatusTransitionException | 400 |
| Unauthorized access | AuthorizationException | 403 |
| Invalid password | AuthenticationException | 401 |
| Locked account | AccountLockedException | 429 |

---

## Database Transaction Scope

### Per-Request Transactions
- Each HTTP request gets one database session (SessionLocal)
- Session context manager handles commit/rollback
- Multiple queries in single transaction (atomic)

### Transaction Examples

**Registration** (atomic):
```
BEGIN TRANSACTION
  INSERT user
  Check UNIQUE email constraint
COMMIT or ROLLBACK
```

**Task Creation with History** (atomic):
```
BEGIN TRANSACTION
  INSERT task
  INSERT task_history
  (All succeeds or all rolls back)
COMMIT
```

---

## Query Optimization Patterns

### N+1 Query Prevention
- `get_profile()`: Loads user + roles + teams in optimized query
- `list_tasks()`: Uses pagination (not loading all tasks)
- `get_team_details()`: Single query with JOINs where possible

### Indexed Lookups
- User.email: UNIQUE index for fast email lookups
- Task.team_id: Index for filtering by team
- Task.created_by_id, Task.assignee_id: Indexes for ownership queries
- Comment.task_id: Index for task-comments relationship
- Notification.user_id: Index for user-notifications filtering

### Lazy Loading Strategy
- SQLAlchemy configured with lazy='select' (explicit loading)
- Relationships loaded on-demand via service methods
- No implicit lazy loading to avoid N+1 queries

---

## Service Ownership Matrix

| Service | Owner | Read Models | Write Models | External Calls |
|---------|-------|---|---|---|
| AuthService | auth/ | User | User | SecurityModule |
| UsersService | users/ | User, Team | User | None |
| TasksService | tasks/ | Task, TaskHistory | Task, TaskHistory | None |
| TeamsService | teams/ | Team, User, team_members | Team, team_members | None |
| CommentsService | comments/ | Comment, Task, User | Comment | NotificationService |
| NotificationsService | notifications/ | Notification, User, Task | Notification | None |
| ReportsService | reports/ | Task, User, Team | None | None |

---

**Database Schema must support all service interactions with appropriate constraints, indexes, and relationships.**
