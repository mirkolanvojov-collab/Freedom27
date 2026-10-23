import unittest

from Framework.research_triage import triage


class ResearchTriageTests(unittest.TestCase):
    def setUp(self):
        self.target = {
            "device_model": "iPhone 16 Plus",
            "model_identifier": "iPhone17,4",
            "exact_os_version": "iOS 26.6.1",
            "build_number": "23G83",
        }

    def test_separates_hardware_demo_and_patched_leads(self):
        registry = {"entries": [
            {"id": "older", "title": "Older device", "status": "unverified", "source_url": "https://example.com/a"},
            {"id": "demo", "title": "Different device demo", "status": "unverified", "source_url": "https://example.com/b"},
            {"id": "patched", "title": "Patched issue", "status": "unverified", "source_url": "https://example.com/c"},
        ]}
        ledger = {"entries": [
            {"id": "older", "target_applicability": "older_hardware_only", "patch_state": "unknown", "reproduction_status": "upstream_claim_only"},
            {"id": "demo", "target_applicability": "reported_single_device_build", "patch_state": "unknown", "reproduction_status": "reported_demo_not_independently_reproduced", "exact_target_build": "iPhone 18 Pro / iOS 27.0.1 / build 24A446"},
            {"id": "patched", "target_applicability": "not_established", "patch_state": "patched_for_reported_scope", "reproduction_status": "not_reproduced_by_Freedom27"},
        ]}
        report = triage(self.target, registry, ledger)
        categories = {row["id"]: row["category"] for row in report["results"]}
        self.assertEqual(categories["older"], "hardware-mismatch")
        self.assertEqual(categories["demo"], "different-device-demo")
        self.assertEqual(categories["patched"], "historical-or-patched")
        self.assertEqual(report["summary"]["joined_entries"], 3)
        self.assertEqual(report["summary"]["reproduced_by_freedom27"], 0)
        self.assertIn("Metadata triage only", report["warning"])

    def test_verified_claim_without_exact_target_reproduction_is_flagged(self):
        report = triage(
            self.target,
            {"entries": [{"id": "overstated", "title": "Unsubstantiated claim", "status": "verified", "source_url": "https://example.com/source"}]},
            {"entries": [{"id": "overstated", "target_applicability": "not_established", "patch_state": "unknown", "reproduction_status": "upstream_claim_only", "exact_target_build": ""}]}
        )
        row = report["results"][0]
        self.assertEqual(row["category"], "verified-claim-evidence-gap")
        self.assertIn("Downgrade", row["next_action"])

    def test_flags_unmatched_records(self):
        report = triage(self.target, {"entries": [{"id": "only-registry"}]},
                        {"entries": [{"id": "only-ledger"}]})
        self.assertEqual(report["summary"]["unmatched_registry_entries"], 1)
        self.assertEqual(report["summary"]["unmatched_ledger_entries"], 1)
        self.assertEqual(len(report["results"]), 2)


if __name__ == "__main__":
    unittest.main()
