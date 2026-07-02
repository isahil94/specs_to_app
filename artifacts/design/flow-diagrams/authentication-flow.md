# Authentication Flow Diagram

## Purpose
Capture the core sign-in, authorization, and password recovery flow for the Task Management System.

## Diagram
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

## Notes
- This flow covers the main access and recovery journeys expected by the business requirements.
