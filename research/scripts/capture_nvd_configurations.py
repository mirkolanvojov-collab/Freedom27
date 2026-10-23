#!/usr/bin/env python3
"""Capture NVD CVE 2.0 and CPE Match 2.0 records for the Freedom27 review set.

This is read-only: it performs GET requests only, writes raw JSON evidence, and
never contacts or modifies an iPhone. NVD API key is optional; set NVD_API_KEY
to increase the documented rate limit. Run sequentially to avoid throttling.
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

CVE_IDS = [
    "CVE-2026-84607", "CVE-2026-43689", "CVE-2026-84523",
    "CVE-2026-86876", "CVE-2026-86886", "CVE-2026-84566",
    "CVE-2026-43687", "CVE-2026-43684", "CVE-2026-43686",
    "CVE-2026-65405", "CVE-2026-84622", "CVE-2026-28968",
]
BASE = "https://services.nvd.nist.gov/rest/json"
OUT = Path("research/nvd_api_capture")
OUT.mkdir(parents=True, exist_ok=True)
API_KEY = os.environ.get("NVD_API_KEY", "").strip()


def get_json(url: str) -> tuple[int, dict | None, str | None]:
    headers = {"User-Agent": "Freedom27-read-only-research/1.0"}
    if API_KEY:
        headers["apiKey"] = API_KEY
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            raw = response.read()
            return response.status, json.loads(raw), None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:2000]
        return exc.code, None, body
    except Exception as exc:
        return 0, None, f"{type(exc).__name__}: {exc}"


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


summary = {
    "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    "source": "NVD API 2.0",
    "read_only": True,
    "api_key_present": bool(API_KEY),
    "records": [],
}
for index, cve_id in enumerate(CVE_IDS):
    encoded_id = urllib.parse.quote(cve_id, safe="-")
    cve_url = f"{BASE}/cves/2.0?cveId={encoded_id}"
    status, payload, error = get_json(cve_url)
    entry = {
        "cve_id": cve_id,
        "cve_endpoint": cve_url,
        "cve_http_status": status,
        "cve_saved": False,
        "cpe_match_http_status": None,
        "cpe_match_saved": False,
        "errors": [],
    }
    if payload is not None:
        save_json(OUT / f"{cve_id}_cves_2.0.json", payload)
        entry["cve_saved"] = True
        entry["cve_total_results"] = payload.get("totalResults")
        # Keep the API response's configuration object exactly as returned.
        vulns = payload.get("vulnerabilities", [])
        entry["configuration_count"] = sum(
            len(v.get("cve", {}).get("configurations", [])) for v in vulns
        )
    else:
        entry["errors"].append({"endpoint": "cves/2.0", "detail": error})
    time.sleep(6 if API_KEY else 7)
    cpe_url = f"{BASE}/cpematch/2.0?cveId={encoded_id}"
    cpe_status, cpe_payload, cpe_error = get_json(cpe_url)
    entry["cpe_match_url"] = cpe_url
    entry["cpe_match_http_status"] = cpe_status
    if cpe_payload is not None:
        save_json(OUT / f"{cve_id}_cpematch_2.0.json", cpe_payload)
        entry["cpe_match_saved"] = True
        entry["cpe_match_total_results"] = cpe_payload.get("totalResults")
    else:
        entry["errors"].append({"endpoint": "cpematch/2.0", "detail": cpe_error})
    summary["records"].append(entry)
    save_json(OUT / "capture_summary.json", summary)
    time.sleep(6 if API_KEY else 7)

summary["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
summary["successful_cve_records"] = sum(r["cve_saved"] for r in summary["records"])
summary["successful_cpe_match_records"] = sum(r["cpe_match_saved"] for r in summary["records"])
save_json(OUT / "capture_summary.json", summary)
failed_records = [
    record for record in summary["records"]
    if not record["cve_saved"] or not record["cpe_match_saved"]
]
print(json.dumps({
    "output_directory": str(OUT),
    "successful_cve_records": summary["successful_cve_records"],
    "successful_cpe_match_records": summary["successful_cpe_match_records"],
    "failed_record_count": len(failed_records),
    "summary_file": str(OUT / "capture_summary.json"),
}, indent=2))

# Keep the artifact-upload step running (it uses if: always()), but do not let
# CI report a successful capture when any requested endpoint failed.
if failed_records:
    raise SystemExit(
        f"NVD capture incomplete: {len(failed_records)} of {len(summary['records'])} "
        "CVE records had at least one failed endpoint; inspect capture_summary.json."
    )
