import json
import tempfile
import unittest
from pathlib import Path

from Framework.claim_checks import check_claim_evidence


class ClaimEvidenceTests(unittest.TestCase):
    def write_data(self, root, registry_entries, ledger_entries=None):
        research = root / "research"
        research.mkdir()
        (research / "vulnerability_registry.json").write_text(
            json.dumps({"entries": registry_entries}), encoding="utf-8"
        )
        (research / "evidence_ledger.json").write_text(
            json.dumps({"entries": ledger_entries if ledger_entries is not None else []}),
            encoding="utf-8",
        )

    def test_unverified_lead_can_lack_exact_target_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_data(root, [{
                "id": "lead", "status": "unverified",
                "source_url": "https://example.org/research"
            }])
            self.assertEqual(check_claim_evidence(root), [])

    def test_verified_claim_requires_exact_device_os_build_and_verification_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_data(root, [{
                "id": "claim", "status": "verified",
                "source_url": "https://example.org/source",
                "target_device": "iPhone test", "target_os_version": "27.0",
                "target_build": ""
            }])
            errors = check_claim_evidence(root)
            self.assertTrue(any("target_build" in error for error in errors))
            self.assertTrue(any("verification_url" in error for error in errors))

    def test_fully_documented_exact_target_claim_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_data(root, [{
                "id": "claim", "status": "verified",
                "source_url": "https://example.org/source",
                "verification_url": "https://example.org/reproduction",
                "target_device": "iPhone test", "target_os_version": "27.0",
                "target_build": "24A123"
            }])
            self.assertEqual(check_claim_evidence(root), [])

    def test_reported_single_device_entry_needs_build_and_demo_label(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_data(root, [], [{
                "id": "demo", "target_applicability": "reported_single_device_build",
                "exact_target_build": "", "reproduction_status": "upstream_claim_only"
            }])
            errors = check_claim_evidence(root)
            self.assertTrue(any("exact_target_build" in error for error in errors))
            self.assertTrue(any("independent reproduction status" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
