# Authentication Sequence Diagram

## Purpose
Describe the authentication flow from sign-in through session creation.

## Diagram
```mermaid
sequenceDiagram
    participant U as User
    participant UI as Frontend
    participant API as Backend API
    participant A as Auth Service
    participant DB as User Store

    U->>UI: Enter credentials
    UI->>API: POST /auth/login
    API->>A: Validate credentials
    A->>DB: Load user and hash comparison
    DB-->>A: User record
    A-->>API: Auth result and session token
    API-->>UI: Return token and user context
    UI-->>U: Show authenticated experience
```

## Notes
- This diagram highlights the main authentication interactions for implementation and testing.
