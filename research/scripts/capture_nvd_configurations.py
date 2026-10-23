#!/usr/bin/env python3
"""Capture NVD CVE 2.0 and CPE Match 2.0 records for the Freedom27 review set.

Read-only: GET requests only. Importing this module performs no network access,
filesystem writes, or sleeps. It never contacts or modifies an iPhone.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

CVE_IDS = [
    "CVE-2026-84607", "CVE-2026-43689", "CVE-2026-84523",
    "CVE-2026-86876", "CVE-2026-86886", "CVE-2026-84566",
    "CVE-2026-43687", "CVE-2026-43684", "CVE-2026-43686",
    "CVE-2026-65405", "CVE-2026-84622", "CVE-2026-28968",
]
BASE = "https://services.nvd.nist.gov/rest/json"
DEFAULT_OUT = Path("research/nvd_api_capture")
DEFAULT_TIMEOUT = 45


def get_json(url: str, api_key: str = "", timeout: int = DEFAULT_TIMEOUT) -> tuple[int, dict | None, str | None]:
    """GET one JSON endpoint and return status, parsed payload, and any error."""
    headers = {"User-Agent": "Freedom27-read-only-research/1.0"}
    if api_key:
        headers["apiKey"] = api_key
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
            payload = json.loads(raw)
            if not isinstance(payload, dict):
                return response.status, None, "JSON response root was not an object"
            return response.status, payload, None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:2000]
        return exc.code, None, body or str(exc)
    except (OSError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
        return 0, None, f"{type(exc).__name__}: {exc}"


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def capture_records(
    cve_ids: list[str] | tuple[str, ...] = tuple(CVE_IDS),
    output_dir: Path = DEFAULT_OUT,
    api_key: str | None = None,
    request_json: Callable[[str, str], tuple[int, dict | None, str | None]] | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Capture requested records. Inject request/sleep functions for offline tests."""
    key = os.environ.get("NVD_API_KEY", "").strip() if api_key is None else api_key.strip()
    requester = request_json or (lambda url, secret: get_json(url, secret))
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "NVD API 2.0",
        "read_only": True,
        "api_key_present": bool(key),
        "records": [],
    }
    summary_path = output_dir / "capture_summary.json"
    save_json(summary_path, summary)

    for index, cve_id in enumerate(cve_ids):
        if not isinstance(cve_id, str) or not cve_id.startswith("CVE-"):
            raise ValueError(f"invalid CVE identifier: {cve_id!r}")
        print(f"[{index + 1}/{len(cve_ids)}] Capturing {cve_id}", flush=True)
        encoded_id = urllib.parse.quote(cve_id, safe="-")
        cve_url = f"{BASE}/cves/2.0?cveId={encoded_id}"
        cpe_url = f"{BASE}/cpematch/2.0?cveId={encoded_id}"
        entry = {
            "cve_id": cve_id,
            "cve_endpoint": cve_url,
            "cve_http_status": None,
            "cve_saved": False,
            "cpe_match_url": cpe_url,
            "cpe_match_http_status": None,
            "cpe_match_saved": False,
            "errors": [],
        }
        summary["records"].append(entry)
        save_json(summary_path, summary)

        status, payload, error = requester(cve_url, key)
        entry["cve_http_status"] = status
        if payload is not None and 200 <= status < 300:
            save_json(output_dir / f"{cve_id}_cves_2.0.json", payload)
            entry["cve_saved"] = True
            entry["cve_total_results"] = payload.get("totalResults")
            vulns = payload.get("vulnerabilities", [])
            if isinstance(vulns, list):
                entry["configuration_count"] = sum(
                    len(v.get("cve", {}).get("configurations", []))
                    for v in vulns if isinstance(v, dict)
                    and isinstance(v.get("cve"), dict)
                    and isinstance(v["cve"].get("configurations", []), list)
                )
            print(f"  CVE endpoint: HTTP {status}; response saved", flush=True)
        else:
            entry["errors"].append({"endpoint": "cves/2.0", "detail": error or f"unexpected HTTP status {status}"})
            print(f"  CVE endpoint: FAILED (HTTP/status {status})", flush=True)
        save_json(summary_path, summary)
        sleep(6 if key else 7)

        cpe_status, cpe_payload, cpe_error = requester(cpe_url, key)
        entry["cpe_match_http_status"] = cpe_status
        if cpe_payload is not None and 200 <= cpe_status < 300:
            save_json(output_dir / f"{cve_id}_cpematch_2.0.json", cpe_payload)
            entry["cpe_match_saved"] = True
            entry["cpe_match_total_results"] = cpe_payload.get("totalResults")
            print(f"  CPE Match endpoint: HTTP {cpe_status}; response saved", flush=True)
        else:
            entry["errors"].append({"endpoint": "cpematch/2.0", "detail": cpe_error or f"unexpected HTTP status {cpe_status}"})
            print(f"  CPE Match endpoint: FAILED (HTTP/status {cpe_status})", flush=True)
        save_json(summary_path, summary)
        sleep(6 if key else 7)

    summary["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    summary["successful_cve_records"] = sum(r["cve_saved"] for r in summary["records"])
    summary["successful_cpe_match_records"] = sum(r["cpe_match_saved"] for r in summary["records"])
    failed = [r for r in summary["records"] if not r["cve_saved"] or not r["cpe_match_saved"]]
    summary["failed_record_count"] = len(failed)
    save_json(summary_path, summary)
    print(json.dumps({
        "output_directory": str(output_dir),
        "successful_cve_records": summary["successful_cve_records"],
        "successful_cpe_match_records": summary["successful_cpe_match_records"],
        "failed_record_count": len(failed),
        "summary_file": str(summary_path),
    }, indent=2))
    return summary


def main() -> int:
    summary = capture_records()
    failed = summary["failed_record_count"]
    if failed:
        print(
            f"NVD capture incomplete: {failed} of {len(summary['records'])} CVE records "
            "had at least one failed endpoint; inspect capture_summary.json."
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
