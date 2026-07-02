# API Specifications

## Purpose
Serve as the authoritative API contract catalog for the Task Management System.

## Metadata
- Version: 1.0.0
- Author: Solution Architect
- Date: 2026-07-02
- Status: Draft
- Workflow ID: WF-20260701-001
- Related Artifacts: requirements_spec.md, user_stories.md, architecture-design.md, data-dictionary.md

## API Overview
The API layer provides authenticated access for user management, task operations, comments, team membership, notifications, and dashboard/reporting. It is the single contract source for frontend, backend, QA, and documentation agents.

## Contract Principles
- Use JSON over HTTPS.
- Require authenticated access for protected endpoints.
- Return consistent error payloads with error codes and request IDs.
- Preserve role-based access rules and ownership boundaries.
- Keep request and response structures explicit so implementation agents do not infer behavior.

## Endpoint Catalog

### Authentication
- POST /auth/register
  - Purpose: Register a new user account.
  - Auth: None.
  - Request: email, password, fullName.
  - Success: 201 with user summary and auth token.
  - Errors: 400 validation, 409 duplicate email.

- POST /auth/login
  - Purpose: Authenticate a user.
  - Auth: None.
  - Request: email, password.
  - Success: 200 with auth token and user profile.
  - Errors: 401 invalid credentials.

- POST /auth/recover
  - Purpose: Request password recovery.
  - Auth: None.
  - Request: email.
  - Success: 202 accepted.
  - Errors: 404 unknown email.

### Tasks
- GET /tasks
  - Purpose: List tasks for the current user and visible team context.
  - Auth: Required.
  - Query: status, assignee, project, search, page, pageSize, sort.
  - Success: 200 with task list and pagination metadata.
  - Errors: 400 invalid filters, 403 unauthorized access.

- POST /tasks
  - Purpose: Create a new task.
  - Auth: Required.
  - Request: title, description, projectId, assigneeId, priority, dueDate, labels.
  - Success: 201 with created task.
  - Errors: 400 validation, 403 forbidden, 404 project/assignee not found.

- GET /tasks/{taskId}
  - Purpose: Retrieve a task by ID.
  - Auth: Required.
  - Success: 200 with task details.
  - Errors: 404 not found, 403 forbidden.

- PUT /tasks/{taskId}
  - Purpose: Update task details or status.
  - Auth: Required.
  - Request: partial task update payload.
  - Success: 200 with updated task.
  - Errors: 400 validation, 403 forbidden, 404 not found.

- POST /tasks/{taskId}/archive
  - Purpose: Archive a task.
  - Auth: Required.
  - Success: 200 with archived task state.
  - Errors: 403 forbidden, 404 not found.

### Comments
- GET /tasks/{taskId}/comments
  - Purpose: List comments for a task.
  - Auth: Required.
  - Success: 200 with comment list.

- POST /tasks/{taskId}/comments
  - Purpose: Add a comment.
  - Auth: Required.
  - Request: body.
  - Success: 201 with created comment.

### Teams
- GET /teams
  - Purpose: List visible teams and memberships.
  - Auth: Required.
  - Success: 200 with team list.

- POST /teams
  - Purpose: Create a new team.
  - Auth: Required.
  - Request: name, description.
  - Success: 201 with created team.

### Notifications
- GET /notifications
  - Purpose: List user notifications.
  - Auth: Required.
  - Success: 200 with notification list.

- POST /notifications/{notificationId}/read
  - Purpose: Mark a notification as read.
  - Auth: Required.
  - Success: 200 with updated notification.

## Shared Response Shape
- Success payloads should include id, createdAt, updatedAt, and status metadata where applicable.
- Errors should return code, message, details, and requestId.

## Request Models
### TaskCreateRequest
- `title` (string, required, max 100)
- `description` (string, optional, max 2000)
- `status` (string, required, values: Todo, In Progress, Review, Completed, Blocked)
- `priority` (string, required, values: Low, Medium, High, Critical)
- `assignee_id` (string, optional)
- `due_date` (string, date, optional)
- `labels` (array of strings, optional)
- `team_id` (string, required)
- `attachments` (array of attachment references, optional)

### TaskStatusUpdateRequest
- `status` (string, required)
- `comment` (string, optional)

### CommentCreateRequest
- `content` (string, required, max 1000)
- `mentions` (array of user IDs, optional)
- `attachments` (array of attachment references, optional)

### TeamMembershipRequest
- `user_id` (string, required)
- `role` (string, required, values: Administrator, TeamLead, Member)

### ProfileUpdateRequest
- `display_name` (string, optional)
- `avatar_url` (string, optional)
- `time_zone` (string, optional)
- `language` (string, optional)

## Response Models
### TaskSummary
- `task_id`, `title`, `status`, `priority`, `assignee_id`, `team_id`, `due_date`, `archived`, `updated_at`

### TaskDetail
- All TaskSummary fields plus `description`, `labels`, `creator_id`, `created_at`, `history_summary`, `comments_count`, and `attachments`

### NotificationSummary
- `notification_id`, `type`, `title`, `message`, `created_at`, `read`, `related_task_id`

## Validation Rules
- Required fields must be enforced server-side.
- Email and password formats must be validated.
- Task status transitions must follow approved workflow states.
- Only permitted assignees and team members may act on protected resources.

## Pagination, Filtering, and Sorting
- Pagination: page and pageSize.
- Filtering: status, assignee, project, search.
- Sorting: createdAt, updatedAt, dueDate, priority.

## Authentication and Authorization
- Protected endpoints require a bearer token.
- Role-based access applies to team, task, and admin operations.

## Idempotency and Versioning
- Repeated recovery or status updates with the same request intent should remain safe and idempotent where applicable.
- Backward-incompatible changes should be introduced through a versioned contract path.

## Integration Contracts
- I-001: Notification provider must accept delivery requests in JSON and return success or failure status.
- I-002: Attachment storage provider must return secure upload and download URLs while preserving access control.

## Architectural Constraints
- All endpoints must reject unauthorized access before business logic executes.
- Task state transitions must validate allowed next states.
- Dashboard and report endpoints must scope data to user visibility.

## Error Model
- 400: validation failure
- 401: authentication failure
- 403: authorization failure
- 404: resource not found
- 409: conflict such as duplicate account
- 500: unexpected server error

## Audit Requirements
- Create audit entries for task creation, updates, comments, archival, and notification reads.
- Include actor, target resource, action, timestamp, and result.

## Open Questions
- Confirm whether email delivery for recovery is in scope for the initial release.
- Confirm whether team admins can manage memberships directly in the initial release.

## Notes
- This artifact is the single source of truth for API behavior used by backend, frontend, QA, and documentation stages.
