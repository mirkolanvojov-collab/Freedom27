"""Regression tests for metadata-only IPSW manifest comparisons."""
import unittest

from research.scripts.compare_ipsw_manifest_inventories import compare_inventories


def inventory(build, components, product="iPhone17,4", verified=True):
    return {
        "integrity_verified_against_pinned_values": verified,
        "product_type": product,
        "source_file_name": f"build-{build}.ipsw",
        "source_sha256": ("a" if build == "23G83" else "b") * 64,
        "source_size_bytes": 100,
        "build_identities": [{
            "build_version": build,
            "components": components,
        }],
    }


class CompareIpswManifestInventoriesTests(unittest.TestCase):
    def test_reports_manifest_metadata_changes_without_claiming_binary_diff(self):
        before = inventory("23G83", [
            {"name": "KernelCache", "path": "kernel.old", "digest_hex": "a" * 40,
             "is_encrypted": True},
            {"name": "OldComponent", "path": "old.bin"},
        ])
        after = inventory("24A437", [
            {"name": "KernelCache", "path": "kernel.new", "digest_hex": "b" * 40,
             "is_encrypted": True},
            {"name": "NewComponent", "path": "new.bin"},
        ])
        result = compare_inventories(before, after)
        self.assertEqual(result["metadata_change_count"], 3)
        self.assertFalse(result["interpretation"]["component_payload_bytes_compared"])
        self.assertFalse(result["interpretation"]["cve_attribution_performed"])
        statuses = {item["name"]: item["status"] for item in result["changes"]}
        self.assertEqual(statuses["KernelCache"], "metadata_changed")
        self.assertEqual(statuses["OldComponent"], "absent_in_after")
        self.assertEqual(statuses["NewComponent"], "added_in_after")

    def test_rejects_cross_device_comparison(self):
        with self.assertRaisesRegex(ValueError, "product_type mismatch"):
            compare_inventories(inventory("23G83", []), inventory("24A437", [], "iPhone18,1"))

    def test_rejects_unverified_input(self):
        with self.assertRaisesRegex(ValueError, "before inventory is not hash-verified"):
            compare_inventories(inventory("23G83", [], verified=False), inventory("24A437", []))


if __name__ == "__main__":
    unittest.main()
