from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


def _extract_figma_url(spec_text: str) -> Optional[str]:
    patterns = [
        r'https://www\.figma\.com/[A-Za-z0-9/_?&=-]+',
        r'https://figma\.com/[A-Za-z0-9/_?&=-]+',
    ]
    for pattern in patterns:
        match = re.search(pattern, spec_text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None


def _extract_screens(spec_text: str) -> list[str]:
    screens: list[str] = []
    valid_screens = {
        "login",
        "register",
        "dashboard",
        "task list",
        "task details",
        "create task",
        "edit task",
        "profile",
        "settings",
    }
    for line in spec_text.splitlines():
        stripped = line.strip()
        if re.match(r'^[-*]\s+', stripped):
            candidate = re.sub(r'^[-*]\s+', '', stripped).strip()
            if candidate.lower() in valid_screens and candidate not in screens:
                screens.append(candidate)
        elif re.match(r'^\d+\.\s+', stripped):
            candidate = re.sub(r'^\d+\.\s+', '', stripped).strip()
            if candidate.lower() in valid_screens and candidate not in screens:
                screens.append(candidate)
    return screens


def generate_design_intake_artifact(spec_path: Path, output_dir: Optional[Path] = None) -> Path:
    spec_path = Path(spec_path)
    if output_dir is None:
        output_dir = spec_path.parent

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    spec_text = spec_path.read_text(encoding="utf-8")
    figma_url = _extract_figma_url(spec_text)
    screens = _extract_screens(spec_text)

    output_path = output_dir / "figma_design_intake.md"
    sections = [
        "# Figma Design Intake",
        "",
        "## Metadata",
        f"- Source Specification: {spec_path.name}",
        f"- Design Extraction Status: {'Direct export unavailable; URL only' if figma_url else 'Pending'}",
        f"- Figma Reference: {figma_url or 'Not provided'}",
        "",
        "## Visual Spec Summary",
        "- Typography: To be interpreted from the Figma reference during UI implementation; exact type scale and weights are not available from the specification alone.",
        "- Spacing: To be interpreted from the Figma reference during UI implementation; exact spacing scale and layout grid are not available from the specification alone.",
        "- Color Tokens: To be interpreted from the Figma reference during UI implementation; exact palette and semantic tokens are not available from the specification alone.",
        "- Iconography: To be interpreted from the Figma reference during UI implementation; exact icon set and usage patterns are not available from the specification alone.",
        "- Component States: To be interpreted from the Figma reference during UI implementation; hover, focus, active, disabled, selected, loading, empty, and error states must be reviewed in the design source.",
        "",
        "## Screen Coverage",
    ]
    if screens:
        sections.extend(f"- {screen}" for screen in screens)
    else:
        sections.append("- No screen list detected in specification")

    sections.extend([
        "",
        "## Screen Specifications",
        "- Screen Name: [name]",
        "- Primary Purpose: [purpose]",
        "- Expected Layout: [layout summary]",
        "- Core Components: [list of major components]",
        "- Interaction Notes: [primary interaction expectations]",
        "- Responsive Notes: [breakpoints and adaptation expectations]",
        "- Accessibility Notes: [contrast, focus, semantics, motion expectations]",
        "",
        "## Frontend Handoff Guidance",
        "- Treat the Figma URL as the authoritative visual source when available.",
        "- Record any deviation from the design in the workflow openlog and handoff artifacts.",
        "- Use this intake artifact as the bridge between requirements and UI implementation.",
        "- If direct Figma inspection is unavailable, mark the missing visual details explicitly and avoid claiming pixel-perfect parity.",
    ])

    output_path.write_text("\n".join(sections) + "\n", encoding="utf-8")
    return output_path
