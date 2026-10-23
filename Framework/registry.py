def validate_entry(entry: dict) -> list[str]:
    if not isinstance(entry, dict):
        return ["entry must be an object"]
    errors = []
    for key in ("id", "title", "source_url", "status"):
        if not isinstance(entry.get(key), str) or not entry[key].strip():
            errors.append(f"{key} must be a non-empty string")
    allowed = {"unverified", "under-review", "verified", "not-applicable"}
    if entry.get("status") not in allowed:
        errors.append(f"status must be one of: {', '.join(sorted(allowed))}")
    return errors
