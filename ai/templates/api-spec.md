# API Specification Template

## Purpose
Define API contracts in a clear, versioned, and testable format.

## Downstream Readiness Expectations
- Produce an API contract package detailed enough for frontend, backend, QA, and documentation agents to implement without follow-up clarification.
- Define endpoints, auth requirements, request/response payloads, validation rules, status codes, pagination/filtering/sorting, idempotency, and audit expectations explicitly.
- Make this artifact the single authoritative API source for downstream implementation and testing.

## Metadata
- Version: [Version]
- Author: [Author]
- Date: [Date]
- Status: [Draft | In Review | Approved]
- API ID: [API ID]
- Service: [Service Name]
- Traceability: [Requirements, Architecture, Contracts]

## API Overview
[Purpose and usage summary]

## API Contract Header
- Purpose: [Purpose]
- Consumer: [Consumer]
- Provider: [Provider]
- Endpoint: [Path]
- HTTP Method: [Method]

## Coverage Mapping
- [Epic ID | Feature ID | User Story ID | API Contract ID | Status]

## Endpoints
- [Method | Path | Purpose]

## Request Models
- [Model Name | Field | Type | Required | Description]

## Request Structure
- [Headers | Body Shape | Constraints]

## Response Models
- [Model Name | Field | Type | Required | Description]

## Response Structure
- [Status Code | Body Shape | Business Meaning]

## Error Model
- [Error Code | Meaning | Handling]

## Error Responses and Status Codes
- [Status Code | Error Scenario | Response Contract]

## Authentication and Authorization
[Applicable access model]

## Pagination, Filtering, Sorting
- Pagination: [Approach or N/A]
- Filtering: [Supported filters or N/A]
- Sorting: [Supported sort fields/order or N/A]

## Idempotency
- [Operation | Idempotency expectation | Condition or N/A]

## Versioning and Compatibility
[Compatibility expectations]

## Audit Requirements
- [Auditable API events and traceability requirements]

## Validation Rules
- [Validation rule]

## Integration Contracts
- [Integration ID | Provider | Consumer | Protocol | Contract | Failure Handling]

## Data Contracts
- [Data Contract ID | Producer | Consumer | Schema Reference | Version]

## Error Handling Contract
- [Scenario | Error Category | Expected Response | Recovery Strategy]

## Architectural Constraints
- [Constraint ID | Security/Authorization/Performance/Observability Requirement | Applies To]

## Dependencies
- [Dependency]

## Open Questions
Record unresolved API and integration questions in `openlog.md`.

## Approval
- Prepared By: [Name]
- Reviewed By: [Name]
- Approved By: [Name]
