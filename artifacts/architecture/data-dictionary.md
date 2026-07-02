# Data Dictionary

## Purpose
Capture canonical technical data definitions used across the Task Management System.

## Metadata
- Version: 1.0.0
- Author: Solution Architect
- Date: 2026-07-02
- Status: Draft
- Workflow ID: WF-20260701-001
- Related Artifacts: lld.md, api-specifications.md, data_requirements.md

## Core Data Definitions

| Term | Type | Description | Ownership |
|---|---|---|---|
| User | Entity | Authenticated person with assigned roles and preferences | Identity Service |
| Task | Entity | Work item with lifecycle, ownership, comments, and history | Task Service |
| Team | Entity | Grouping of users collaborating on shared work | Team Service |
| Comment | Entity | User-authored update attached to a task | Task Service |
| Notification | Entity | User-visible event or reminder | Notification Service |
| Audit Event | Entity | Immutable log of state changes and administrative actions | Platform Service |

## Notes
- This document is a technical reference for downstream implementation and testing.
