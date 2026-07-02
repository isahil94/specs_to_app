from pathlib import Path

from scripts.design_intake import generate_design_intake_artifact


def test_generate_design_intake_artifact_extracts_figma_details(tmp_path):
    spec_path = tmp_path / "specification.md"
    spec_path.write_text(
        """# Task Management System

## UI Design

**Figma URL**
https://www.figma.com/make/abc123/Task-Management-System-Screens

### Available Screens
- Login
- Dashboard
- Task Details
""",
        encoding="utf-8",
    )

    output_path = generate_design_intake_artifact(spec_path, tmp_path)

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "https://www.figma.com/make/abc123/Task-Management-System-Screens" in content
    assert "Login" in content
    assert "Dashboard" in content
    assert "Task Details" in content
    assert "Design Extraction Status" in content
    assert "URL only" in content
