# Task Update Sequence Diagram

## Purpose
Describe the interactions involved when a user updates a task and the system persists the change.

## Diagram
```mermaid
sequenceDiagram
    participant U as User
    participant UI as Frontend
    participant API as Backend API
    participant S as Task Service
    participant DB as Data Store
    participant N as Notification Service

    U->>UI: Submit task update
    UI->>API: PUT /tasks/{task_id}
    API->>S: Validate request and auth
    S->>DB: Load task and apply update
    DB-->>S: Updated task record
    S->>N: Create history and notifications
    N-->>S: Delivery acknowledgement
    S-->>API: Confirm success
    API-->>UI: Return updated task
    UI-->>U: Show updated state
```

## Notes
- This sequence diagram is intended to guide backend implementation and QA validation.
