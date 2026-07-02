# Business Process Flows

## Purpose
Capture the main business workflows and process steps for the Task Management System.

## Metadata
- Version: 1.0.0
- Author: Business Analyst
- Date: 2026-07-02
- Status: Draft
- Workflow ID: WF-20260701-001
- Related Artifacts: requirements_spec.md, user_stories.md, acceptance_criteria.md

## Core Flows

### Flow: User Sign-In
1. User opens the sign-in screen.
2. User enters valid credentials.
3. System authenticates the user.
4. System presents the dashboard or appropriate landing page.

### Flow: Create and Manage a Task
1. User selects the task creation action.
2. User enters task details and assigns ownership.
3. System validates the task data.
4. System creates the task and records it for tracking.
5. User or team members can update, comment, archive, or complete the task.

### Flow: Review and Complete Work
1. Assigned user updates task progress.
2. Team lead or reviewer validates status and completion readiness.
3. Task moves through the business lifecycle until final completion or archival.
4. System records activity history and notifications.

### Flow: Team and Role Administration
1. Administrator manages users, teams, and role assignments.
2. Team lead manages membership and team-level work.
3. System enforces role-based access and visibility rules.

## Flow Diagrams

### Authentication Flow
```mermaid
flowchart TD
    A[User Opens Sign In] --> B{Has account?}
    B -->|Yes| C[Enter Credentials]
    B -->|No| D[Register Account]
    D --> C
    C --> E[Validate Credentials]
    E -->|Valid| F[Create Session]
    E -->|Invalid| G[Show Error]
    F --> H[Redirect to Dashboard]
    G --> I[Offer Password Recovery]
    I --> J[Recover Password]
    J --> K[Reset Password]
    K --> C
```

### Task Lifecycle Flow
```mermaid
flowchart TD
    A[User Authenticated] --> B[Open Dashboard]
    B --> C{Create or Select Task}
    C -->|Create| D[Enter Task Details]
    C -->|Select| E[Open Task Details]
    D --> F[Validate Task Data]
    E --> G[Review Task State]
    F --> H[Create Task Record]
    G --> I{Action}
    I -->|Update| J[Modify Task]
    I -->|Comment| K[Add Comment]
    I -->|Archive| L[Archive Task]
    I -->|Complete| M[Complete Task]
    J --> N[Persist Changes]
    K --> N
    L --> O[Set Read-Only State]
    M --> P[Record Completion]
    H --> Q[Notify Relevant Users]
    N --> Q
    O --> Q
    P --> Q
```
