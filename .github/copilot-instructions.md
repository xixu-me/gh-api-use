# GitHub REST API Use - Copilot Instructions

## Project Overview

A collection of standalone Python scripts for GitHub REST API automation tasks. Each script in `uses/` is self-contained and designed to be copied, configured, and run independently.

## Script Architecture Pattern

All scripts follow the same structure:

```python
"""
Docstring with description, usage steps, and requirements
"""

import requests  # Only external dependency

# Configuration block - user replaces these values
TOKEN = "YOUR_PAT"
OWNER = "your-username"
REPO = "your-repo"
# Script-specific settings...

# Standard headers setup
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

# API calls with error handling
# Print results to console
```

## Conventions

### Script Structure

- **Module docstring**: Must include description, numbered usage steps, and requirements
- **Configuration block**: Place all user-configurable constants immediately after imports with placeholder values and inline comments explaining each
- **Error handling**: Check `response.status_code` and print `response.json().get("message", "No error message provided")` on failure
- **Console output**: Use `print()` statements to report progress and results

### API Patterns

- Use `Bearer` token auth: `{"Authorization": f"Bearer {TOKEN}"}`
- Always include `Accept: application/vnd.github+json` header
- Handle pagination via `response.links["next"]` when iterating large datasets (see `delete_a_workflow.py`)
- Date parsing format: `%Y-%m-%dT%H:%M:%SZ` for GitHub timestamps

### Naming

- Script files: `snake_case.py` describing the action (e.g., `close_old_issues.py`)
- Variables: Use descriptive names matching GitHub API terminology (`OWNER`, `REPO`, `TOKEN`)

## Token Scopes Reference

| Operation Type      | Required Scopes     |
| ------------------- | ------------------- |
| Repository content  | `repo`              |
| Workflow operations | `repo` + `workflow` |
| Admin/collaborator  | `repo` + `admin`    |

## Creating New Scripts

1. Copy an existing script as a template
2. Update the docstring with clear usage instructions
3. Define configuration constants with placeholder values
4. Implement API logic with proper error handling and console output
5. Handle pagination if the endpoint returns lists

## Dependencies

- Python 3.6+
- `requests` library only - no other external dependencies
