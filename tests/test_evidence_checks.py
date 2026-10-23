import json
import tempfile
import unittest
from pathlib import Path

from Framework.evidence_checks import check_evidence


class EvidenceCheckTests(unittest.TestCase):
    def make_root(self, root: Path, rows=None, entries=None):
        research = root / "research"
        research.mkdir()
        (research / "compatibility_matrix.json").write_text(json.dumps({
            "allowed_statuses": ["not-investigated", "experimental", "verified"],
            "rows": rows if rows is not None else [{
                "device_family": "iPhone test", "variant": "base", "os_family": "iOS 27",
                "status": "not-investigated", "notes": "Not yet investigated.",
                "evidence_url": "https://example.org/source"
            }]
        }), encoding="utf-8")
        (research / "evidence_ledger.json").write_text(json.dumps({
            "allowed_values": {
                "evidence_type": ["official_advisory", "news_report"],
                "patch_state": ["unknown", "patched_for_reported_scope"],
                "target_applicability": ["not_established", "reported_single_device_build"],
                "reproduction_status": ["not_reproduced_by_Freedom27", "reported_demo_not_independently_reproduced"]
            },
            "entries": [{
                "id": entry.get("id", "example-lead"),
                "evidence_type": "official_advisory",
                "patch_state": "unknown",
                "target_applicability": "not_established",
                "reproduction_status": "not_reproduced_by_Freedom27",
                "evidence_url": entry.get("source_url", "https://example.org/advisory"),
                "next_action": "Review public evidence."
            } for entry in (entries if entries is not None else [{
                "id": "example-lead", "source_url": "https://example.org/advisory"
            }])]
        }), encoding="utf-8")
        (research / "vulnerability_registry.json").write_text(json.dumps({
            "entries": entries if entries is not None else [{
                "id": "example-lead", "title": "Example lead",
                "source_url": "https://example.org/advisory", "status": "unverified",
                "summary": "Research lead only; not a confirmed jailbreak chain."
            }]
        }), encoding="utf-8")

    def test_valid_uninvestigated_metadata_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_root(root)
            self.assertEqual(check_evidence(root), [])

    def test_verified_requires_exact_build_fields_and_https_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_root(root, rows=[{
                "device_family": "iPhone test", "variant": "base", "os_family": "iOS 27",
                "status": "verified", "notes": "Tested", "evidence_url": "http://example.org"
            }])
            errors = check_evidence(root)
            self.assertTrue(any("requires an HTTPS evidence_url" in e for e in errors))
            self.assertTrue(any("requires model_identifier" in e for e in errors))
            self.assertTrue(any("requires os_version" in e for e in errors))
            self.assertTrue(any("requires build" in e for e in errors))

    def test_demo_only_cannot_be_marked_verified(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_root(root, rows=[{
                "device_family": "iPhone test", "variant": "Pro", "os_family": "iOS 27",
                "status": "verified", "notes": "Reported demonstration only",
                "evidence_url": "https://example.org/source", "model_identifier": "iPhone1,1",
                "os_version": "27.0", "build": "24A1"
            }])
            self.assertTrue(any("demo/report-only" in e for e in check_evidence(root)))

    def test_cve_leads_cannot_be_marked_confirmed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cve = {
                "id": "apple-cve-2026-28968-kernel-lead", "title": "Kernel lead",
                "source_url": "https://support.apple.com/advisory", "status": "verified",
                "summary": "This is not a public jailbreak and is not a confirmed chain."
            }
            self.make_root(root, entries=[cve])
            self.assertTrue(any("must remain unverified" in e for e in check_evidence(root)))

    def test_duplicate_ids_and_non_https_sources_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            entry = {"id": "same", "title": "Example", "source_url": "http://example.org",
                     "status": "unverified", "summary": "Research only."}
            self.make_root(root, entries=[entry, entry])
            errors = check_evidence(root)
            self.assertTrue(any("duplicate id" in e for e in errors))
            self.assertTrue(any("source_url must be HTTPS" in e for e in errors))

    def test_malformed_status_type_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_root(root, rows=[{
                "device_family": "iPhone test", "variant": "base", "os_family": "iOS 27",
                "status": ["verified"], "notes": "Malformed status."
            }])
            errors = check_evidence(root)
            self.assertTrue(any("has disallowed status" in error for error in errors))

    def test_non_object_registry_root_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_root(root)
            (root / "research" / "vulnerability_registry.json").write_text("[]", encoding="utf-8")
            errors = check_evidence(root)
            self.assertTrue(any("registry root must be an object" in e for e in errors))

    def test_non_object_allowed_values_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_root(root)
            path = root / "research" / "evidence_ledger.json"
            ledger = json.loads(path.read_text(encoding="utf-8"))
            ledger["allowed_values"] = []
            path.write_text(json.dumps(ledger), encoding="utf-8")
            errors = check_evidence(root)
            self.assertTrue(any("allowed_values must be an object" in e for e in errors))


if __name__ == "__main__":
    unittest.main()

