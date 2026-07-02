# Data Requirements

## Purpose
Capture business data expectations for the Task Management System without defining database schema.

## Metadata
- Version: 1.0.1
- Author: Business Analyst
- Date: 2026-07-02
- Status: Draft
- Workflow ID: WF-20260701-001
- Related Artifacts: requirements_spec.md, user_stories.md, business_rules.md, screen_elements.md

## Business Entities

### Entity: Task
- Business Meaning: A unit of work to be created, assigned, tracked, and completed.
- Owner: Team Member or Team Lead
- Required Attributes: title, description, status, priority, owner, created date, due date
- Optional Attributes: assignee, labels, comments, attachments, archived state, reminder preferences
- Relationships: Belongs to a team; may have comments, notifications, and history entries; may be linked to a report or dashboard view
- Lifecycle: Todo, In Progress, Review, Completed, Blocked, Archived
- Retention: Retained for audit and reporting while active or archived
- PII Classification: Internal
- Business Notes: A task is the central object of collaboration and tracking across the solution.

### Entity: User
- Business Meaning: A person who can authenticate and use the system.
- Owner: Administrator
- Required Attributes: email, display name, role, account status
- Optional Attributes: avatar, preferences, time zone, language, notification settings
- Relationships: Member of teams; owns or is assigned tasks; receives notifications
- Lifecycle: Active, Inactive, Suspended
- Retention: Retained while account is active and for audit history where required
- PII Classification: Sensitive
- Business Notes: User accounts form the basis of authentication, authorization, and collaboration.

### Entity: Team
- Business Meaning: A grouping of users collaborating on work.
- Owner: Administrator or Team Lead
- Required Attributes: name, lead user, membership scope
- Optional Attributes: description, settings, notification preferences
- Relationships: Contains users; owns tasks and reports
- Lifecycle: Active, Archived
- Retention: Retained while active or archived for reporting
- PII Classification: Internal
- Business Notes: Teams define the collaboration perimeter for shared work and visibility.

### Entity: Notification
- Business Meaning: A user-visible message about work changes or reminders.
- Owner: System
- Required Attributes: recipient, message type, status
- Optional Attributes: related task, due date context, read timestamp, delivery channel
- Relationships: Related to tasks and users
- Lifecycle: Unread, Read, Dismissed
- Retention: Retained according to notification policy
- PII Classification: Internal
- Business Notes: Notifications keep users aware of assignments, updates, and due-date risk.

### Entity: Comment
- Business Meaning: A business note attached to a task to capture discussion and progress context.
- Owner: Task Participants
- Required Attributes: content, author, task reference, created date
- Optional Attributes: mentions, attachments, edited state
- Relationships: Linked to a task and one or more users
- Lifecycle: Created, Edited, Deleted
- Retention: Retained as part of task history
- PII Classification: Internal
- Business Notes: Comments provide collaboration context and should be preserved as part of the task record.

## Data Quality Expectations
- Required business data must be present before a task or user account becomes active.
- Critical task lifecycle transitions must be traceable to history and user context.
- Notification and preference data must be available for role-aware user experiences.

## Notes
- Keep this document business-focused and implementation-agnostic.
- Do not define tables, columns, keys, SQL, or storage design.
