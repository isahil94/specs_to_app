# Screen Elements

## Purpose
Describe the core screens and interactive elements for the Task Management System using business terminology only.

## Metadata
- Version: 1.0.0
- Author: Business Analyst
- Date: 2026-07-02
- Status: Draft
- Workflow ID: WF-20260701-001
- Related Artifacts: requirements_spec.md, user_stories.md, ui_observations.md

## Screens

### Screen Name: Sign In
- Purpose: Authenticate a returning user.
- Component or Section: Authentication

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Email | Input | Email | Enter your email | Yes | Must be a valid email address | None | Always visible | Enabled when the form is active | Account access requires a known email | Must be keyboard accessible |
| Password | Input | Password | Enter your password | Yes | Must meet password policy | None | Always visible | Enabled when the form is active | Password strength is required | Must support screen readers |
| Sign In | Button | Sign In | None | Yes | None | None | Always visible | Enabled when inputs are complete | Authenticated access is granted for valid credentials | Must have clear focus state |
| Forgot Password | Link | Forgot Password | None | No | None | None | Always visible | Enabled | Supports recovery workflow | Must be keyboard accessible |

### Screen Name: Dashboard
- Purpose: Provide an overview of work, deadlines, and team activity.
- Component or Section: Workspace Overview

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
| Summary Cards | Read-only Text | Summary | None | No | None | None | Always visible | Enabled | Shows overdue, due soon, and completion metrics | Must be readable by assistive tech |
| Task List | Read-only Text | Tasks | None | No | None | None | Always visible | Enabled | Displays current workload and status | Must support screen reader navigation |
| Filter Controls | Select | Filter | None | No | None | All tasks | Always visible | Enabled | Filters by status, owner, and team | Must have descriptive labels |

### Screen Name: Task Detail
- Purpose: Review and update a task's details and activity.
- Component or Section: Task Work Item

#### Elements
| Element Name | Element Type | Label | Placeholder | Required | Validation Rules | Default Value | Visibility Rules | Enabled/Disabled Rules | Business Rules | Accessibility Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Title | Input | Title | Enter task title | Yes | Required, max 100 characters | None | Always visible | Enabled for editable tasks | Task titles are required | Must be keyboard accessible |
| Description | Input | Description | Add details | No | Max 2000 characters | None | Always visible | Enabled for editable tasks | Descriptions may be optional | Must support large text input |
| Status | Select | Status | None | Yes | Restricted to approved values | Todo | Always visible | Enabled for authorized users | Status must follow approved lifecycle values | Must expose clear labels |
| Priority | Select | Priority | None | Yes | Restricted to approved values | Medium | Always visible | Enabled for authorized users | Priority reflects business urgency | Must be understandable by screen readers |
| Assignee | Select | Assignee | None | No | None | None | Always visible | Enabled for authorized users | Assignee may be updated by permitted roles | Must expose current selection |
| Comments | Input | Comment | Add a comment | No | Max 1000 characters | None | Always visible | Enabled for authorized users | Comments support collaboration and audit context | Must support keyboard entry |
| Archive | Button | Archive | None | No | None | None | Visible when task is active | Enabled for allowed users | Archived tasks become read-only | Must provide a clear confirmation state |

## Notes
- Keep content business-focused and implementation-agnostic.
- Capture every interactive element that affects user decisions or business outcomes.
- If an element is not applicable, record "Not applicable" rather than omitting it.
