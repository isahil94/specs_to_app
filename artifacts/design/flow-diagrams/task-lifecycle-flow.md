# Task Lifecycle Flow Diagram

## Purpose
Capture the business flow for creating, updating, archiving, and completing a task.

## Diagram
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

## Notes
- This flow reflects the business lifecycle and should be used for implementation planning and QA.
