# Frontend Design Intake Workflow

## Purpose
This document describes the end-to-end frontend design handoff path for projects that include a Figma reference.

## Inputs
- Specification document containing the product requirements
- Optional Figma URL in the specification
- Upstream business and architecture artifacts

## Workflow
1. Business Analyst consumes the Figma URL from the specification and creates a structured intake artifact named `figma_design_intake.md`.
2. The intake artifact captures the Figma URL, screen coverage, visual system notes, interaction notes, responsive notes, accessibility notes, and missing design details.
3. The UI/UX Developer consumes the intake artifact along with requirements and architecture outputs.
4. The frontend implementation stage uses the design intake as the structured source for visual implementation guidance and records deviations when the design cannot be reproduced exactly.

## Output Contract
The following artifacts are expected for frontend design handoff:
- `artifacts/requirements/ui_observations.md`
- `artifacts/requirements/figma_design_intake.md`
- `artifacts/frontend/quality-report.md`
- `artifacts/frontend/handoff-contract.md`
- `artifacts/frontend/openlog.md`

## Implementation Notes
- If direct design export data is unavailable, the workflow should still produce the structured intake artifact and explicitly record the missing visual detail as a design gap.
- The frontend implementation should treat the intake artifact as authoritative for screen coverage and visual guidance, while still respecting architecture and accessibility requirements.
