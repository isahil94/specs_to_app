# Business Rules

## Purpose
Capture canonical business rules for the Task Management System in a structured, traceable form that can drive validation, QA, and downstream implementation decisions.

## Metadata
- Version: 1.0.1
- Author: Business Analyst
- Date: 2026-07-02
- Status: Draft
- Workflow ID: WF-20260701-001
- Related Artifacts: requirements_spec.md, user_stories.md, acceptance_criteria.md, screen_elements.md

## Scope
These rules define business expectations for task ownership, access control, lifecycle behavior, collaboration, notifications, and account protection.

## Rule Catalog

### Rule ID: BR-001
- Rule Name: Task Ownership and Assignment
- Description: Every task must have one primary owner and may have one current assignee.
- Business Justification: Ensures accountability and clear responsibility for delivery.
- Applies To: Tasks
- Validation: Ownership and assignment fields are required for task creation and update flows.
- Exception: Administrative migration or bulk operations may require temporary ownership reassignment.
- Priority: High
- Related Stories: US-002, US-003

### Rule ID: BR-002
- Rule Name: Task Deletion Authority
- Description: Only administrators may permanently delete tasks.
- Business Justification: Prevents accidental loss of work records and preserves governance controls.
- Applies To: Tasks
- Validation: Delete actions require an administrator role and explicit confirmation.
- Exception: Archived tasks may be restored rather than permanently deleted.
- Priority: High
- Related Stories: US-002

### Rule ID: BR-003
- Rule Name: Archival Read-Only Mode
- Description: Archived tasks remain searchable but become read-only for non-administrators unless restored.
- Business Justification: Preserves history and prevents uncontrolled edits after archival.
- Applies To: Archived Tasks
- Validation: Update and delete actions on archived tasks are blocked unless a restoration action is authorized.
- Exception: Administrators may restore archived tasks and re-enable editing when approved.
- Priority: High
- Related Stories: US-002, US-004

### Rule ID: BR-004
- Rule Name: Status Lifecycle
- Description: Task status transitions must follow the approved business lifecycle values: Todo, In Progress, Review, Completed, and Blocked.
- Business Justification: Keeps execution states consistent, auditable, and understandable across roles.
- Applies To: Task Lifecycle
- Validation: Status values are restricted to approved business values.
- Exception: Custom status values require explicit business approval.
- Priority: High
- Related Stories: US-003

### Rule ID: BR-005
- Rule Name: Immutable History
- Description: Task history is immutable and must capture changes with audit context.
- Business Justification: Supports accountability, compliance, and reviewability.
- Applies To: Task Activity History
- Validation: Audit trail entries are created for task changes, status changes, comments, and admin actions.
- Exception: System maintenance activities may be logged separately.
- Priority: High
- Related Stories: US-005

### Rule ID: BR-006
- Rule Name: Password Strength
- Description: Passwords must meet minimum security strength requirements.
- Business Justification: Protects user accounts and business data.
- Applies To: Authentication
- Validation: Password policy is enforced during registration and password changes.
- Exception: SSO or enterprise identity integrations may use alternative validation.
- Priority: High
- Related Stories: US-001

### Rule ID: BR-007
- Rule Name: Notification Awareness
- Description: Users must receive notifications for assignment changes, comments, due-date proximity, and overdue task states.
- Business Justification: Improves collaboration and reduces missed work.
- Applies To: Notifications
- Validation: Notification events are generated when the triggering business condition occurs.
- Exception: Users may mute or customize notification preferences.
- Priority: Medium
- Related Stories: US-005, US-007

### Rule ID: BR-008
- Rule Name: Team Scope Visibility
- Description: Users may view and act on work only within the scope permitted by their role and team membership.
- Business Justification: Protects confidentiality and aligns with role-based collaboration.
- Applies To: Team and Workspace Visibility
- Validation: Access rules are enforced per role and team boundary.
- Exception: Administrators may access broader scopes when required for governance.
- Priority: High
- Related Stories: US-006, US-007

## Implementation Notes
- These rules should be treated as business truth for QA and downstream architecture artifacts.
- Any exceptions or policy disputes should be captured in the openlog and handoff artifacts.
