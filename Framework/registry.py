from urllib.parse import urlparse


def validate_entry(entry: dict) -> list[str]:
    if not isinstance(entry, dict):
        return ["entry must be an object"]
    errors = []
    for key in ("id", "title", "source_url", "status"):
        if not isinstance(entry.get(key), str) or not entry[key].strip():
            errors.append(f"{key} must be a non-empty string")
    status = entry.get("status")
    allowed = {"unverified", "under-review", "verified", "not-applicable"}
    if not isinstance(status, str) or status not in allowed:
        errors.append(f"status must be one of: {', '.join(sorted(allowed))}")
    source_url = entry.get("source_url")
    if isinstance(source_url, str) and source_url:
        try:
            parsed = urlparse(source_url)
            valid_url = (
                parsed.scheme == "https" and bool(parsed.hostname)
                and not parsed.username and not parsed.password
            )
            if valid_url:
                _ = parsed.port  # Reject malformed port values.
        except ValueError:
            valid_url = False
        if not valid_url:
            errors.append("source_url must be a valid HTTPS URL without embedded credentials")
    return errors
