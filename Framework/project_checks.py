"""Read-only integrity checks for Freedom27 research metadata."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_CONFIG = (
    "project", "target_os", "package_manager_preference",
    "project_status", "working_jailbreak",
)


def load_json(path: Path) -> Any:
    """Load JSON and let callers report malformed files as errors."""
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def check_project(root: Path = ROOT) -> list[str]:
    """Return problems found in metadata; does not inspect or modify any device."""
    errors: list[str] = []
    config_path = root / "config.json"
    registry_path = root / "research" / "vulnerability_registry.json"

    try:
        config = load_json(config_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"config.json could not be loaded: {exc}"]

    if not isinstance(config, dict):
        return ["config.json root must be an object"]
    for key in REQUIRED_CONFIG:
        if key not in config:
            errors.append(f"config.json is missing required key: {key}")
    if config.get("project") != "Freedom27":
        errors.append("config.json project must be Freedom27")
    if config.get("project_status") != "research-scaffold":
        errors.append("project_status must remain research-scaffold until verified")
    if config.get("working_jailbreak") is not False:
        errors.append("working_jailbreak must be false until independently verified")

    try:
        registry = load_json(registry_path)
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [f"vulnerability_registry.json could not be loaded: {exc}"]

    if not isinstance(registry, dict):
        errors.append("vulnerability registry root must be an object")
        return errors
    entries = registry.get("entries")
    if not isinstance(entries, list):
        errors.append("vulnerability registry entries must be a list")
        return errors

    seen_ids: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"registry entry {index} must be an object")
            continue
        entry_errors = validate_registry_entry(entry)
        errors.extend(f"registry entry {index}: {error}" for error in entry_errors)
        entry_id = entry.get("id")
        if isinstance(entry_id, str) and entry_id:
            if entry_id in seen_ids:
                errors.append(f"registry entry {index}: duplicate id {entry_id}")
            seen_ids.add(entry_id)
    return errors


def validate_registry_entry(entry: dict[str, Any]) -> list[str]:
    """Validate a single entry with the project's public-source evidence policy."""
    from .registry import validate_entry
    return validate_entry(entry)
