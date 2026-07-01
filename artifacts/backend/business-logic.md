# Backend Business Logic & Validation Rules

## Task Management Rules

### Task Lifecycle States

| Status | Allowed Transitions | Business Rules |
|--------|-------------------|-----------------|
| TODO | IN_PROGRESS, ARCHIVED | Initial state; waiting to start |
| IN_PROGRESS | REVIEW, TODO, ARCHIVED | Work in progress; can revert to TODO |
| REVIEW | DONE, IN_PROGRESS, ARCHIVED | Pending approval; can go back to work |
| DONE | ARCHIVED | Completed; no further changes except archive |
| ARCHIVED | TODO | Can be restored to active workflow |

### Task Immutability Rules

- **Archived Tasks**: Cannot be edited (read-only except for restoration)
- **Completed Tasks**: Only administrators can edit after completion
- **Task Deletion**: Only administrators can permanently delete tasks
- **Soft Delete**: Archive operation is preferred over deletion

### Task Ownership & Access

- **Creator**: Can view, edit, archive their own tasks
- **Assignee**: Can view and edit assigned tasks
- **Team Member**: Can view tasks within their team
- **Non-Members**: Cannot access tasks outside their teams

## Authentication Rules

### Registration

1. Email must be unique (no duplicate emails)
2. Password must meet strength requirements:
   - Minimum 8 characters
   - At least one uppercase letter
   - At least one number
   - At least one special character (! @ # $ % ^ & * ( ) _ + - = [ ] { } | ; : , . < >)
3. Account created in active state
4. Email verification optional (is_verified flag)

### Login

1. Credentials validated (email + password)
2. Password verified using bcrypt
3. Account must be active (is_active = true)
4. Failed attempt counter incremented
5. After 5 failed attempts:
   - Account locked for 15 minutes
   - locked_until timestamp set
6. Successful login:
   - Failed attempt counter reset to 0
   - last_login timestamp updated
   - JWT tokens issued

### Token Management

- **Access Token**: 30-minute expiration (configurable)
- **Refresh Token**: 7-day expiration (configurable)
- **Token Signing**: HS256 algorithm with SECRET_KEY
- **Bearer Scheme**: Required for all protected endpoints

## Authorization Rules

### Role-Based Access Control

| Role | Capabilities |
|------|---|
| Administrator | All operations; user management; team management; audit access |
| TeamLead | Create/edit team; manage team membership; view team tasks |
| User | Create/edit own tasks; assign to team members; comment; participate |

### Resource-Level Access Control

| Resource | Access Rule |
|----------|---|
| Own Task | Creator and assignee can view and edit |
| Team Task | Team members can view; assignee can edit |
| Team | Lead can manage; members can view |
| Comment | Author can delete; all task viewers can read |
| Notification | User can only access own notifications |
| Profile | User can only modify own profile |

## Comment & Mention Rules

### Comment Creation

1. Comment must belong to an existing task
2. Comment content required (non-empty string)
3. Author must be authenticated
4. Mentions are tracked (user IDs)
5. Attachments are URLs (stored as strings)

### Comment Deletion

1. Only comment author can delete their comments
2. Deletion is permanent (hard delete)
3. Comments from deleted users are orphaned (preserved for audit)

### Mention Notifications

- When user is mentioned in comment, notification created
- Notification includes task and comment context
- User can mark notification as read

## Team Management Rules

### Team Creation

1. Team name required (non-empty string)
2. Lead must be active user
3. Creator automatically added as member
4. Team created in active state

### Team Membership

1. Users can be added by team lead only
2. Same user cannot be added twice
3. All members are stored in team_members table with role
4. Role is stored per membership (can differ per team)

### Team Lead Changes

1. Only administrators can change team lead
2. New lead must be active user
3. Lead can manage team membership

## Notification Rules

### Notification Types

| Type | Trigger | Recipients |
|------|---------|---|
| assignment | Task assigned to user | Assigned user |
| updated | Task updated | Watchers |
| commented | Comment added to task | Watchers + mentions |
| mentioned | User mentioned in comment | Mentioned user |
| overdue | Task approaching/past due date | Task creator + assignee |
| reminder | Scheduled reminder | Assigned user |

### Notification Lifecycle

1. **Created**: When event occurs
2. **Unread**: Default state
3. **Read**: User marks as read (read_at timestamp set)
4. **Deleted**: User deletes notification

## Dashboard & Reporting Rules

### Dashboard Metrics

Calculated for authenticated user:

| Metric | Calculation | Includes |
|--------|---|---|
| total_tasks | Count of active tasks | Owner or assignee |
| completed_tasks | Count of DONE tasks | Owner or assignee |
| in_progress_tasks | Count of IN_PROGRESS tasks | Owner or assignee |
| overdue_tasks | Count of tasks with past due_date (not DONE) | Owner or assignee |
| assigned_to_me | Count of assigned tasks (assignee_id = user_id) | Only assigned tasks |

### Recent Tasks

- Last 10 active tasks modified by user
- Ordered by updated_at descending
- Excludes archived tasks

### Workload Summary

- Tasks grouped by status
- Tasks grouped by priority
- Completion percentage (done / total)
- Overdue count

## Audit & Compliance Rules

### Audit Logging

Events logged to AuditLog:

| Event | Resource | Details |
|-------|----------|---------|
| User Registration | user | user_id, email |
| Login Success | user | user_id, timestamp |
| Login Failure | user | user_id, reason, attempt_count |
| Account Locked | user | user_id, locked_until |
| Password Changed | user | user_id |
| Profile Updated | user | user_id, fields changed |
| Task Created | task | task_id, creator_id |
| Task Status Changed | task | task_id, old_status, new_status |
| Task Archived | task | task_id |
| Task Deleted | task | task_id |
| Team Created | team | team_id, lead_id |
| Member Added | team | team_id, user_id, role |
| Member Removed | team | team_id, user_id |

### Audit Trail for Tasks

TaskHistory model tracks:
- What changed (field_name)
- Old and new values
- Who made the change (changed_by_id)
- When (created_at)
- Change type (created, updated, status_changed, archived, restored)

## Validation Rules

### Email Validation

- Must be valid email format
- Must be unique across all users
- Case-insensitive comparison

### Task Fields

| Field | Rules |
|-------|-------|
| title | Required, 1-255 characters |
| description | Optional, up to 5000 chars |
| status | Enum value, valid transition |
| priority | Enum value (low, medium, high, urgent) |
| due_date | ISO 8601 datetime format |
| labels | String array, comma-separated storage |

### Pagination

- Default page_size: 50
- Maximum page_size: 100
- Minimum page_size: 1
- Page numbering: 1-indexed

## Date/Time Rules

### Timezone Handling

- User timezone stored in preference (default: UTC)
- due_date in ISO 8601 format
- Server stores all times in UTC
- Client responsible for timezone conversion

### Created/Updated Timestamps

- Automatically set to current UTC time
- Updated on each modification
- Immutable after creation (not user-editable)

## Business Hours & SLA

- Dashboard response SLA: < 2 seconds
- Task search SLA: < 500ms
- Comment thread load SLA: < 1 second
- Acceptable concurrency: 500+ users

## Data Retention

- Active tasks: Indefinite
- Archived tasks: Indefinite
- Comments: Indefinite
- Notifications: Until deleted by user
- Audit logs: Minimum 1 year (configurable)
- Failed login attempts: 24 hours

## Conflict Resolution

| Conflict | Resolution |
|----------|---|
| Duplicate email on register | Return 409 Conflict |
| User already in team | Return 409 Conflict |
| Invalid status transition | Return 400 Bad Request |
| Resource already archived | Return 400 Bad Request |
| Unauthorized access | Return 403 Forbidden |

## Concurrency & Race Conditions

- Database constraints prevent duplicate emails
- Optimistic locking via updated_at timestamp (future enhancement)
- Atomic database operations via transactions
- Connection pooling for concurrent access
