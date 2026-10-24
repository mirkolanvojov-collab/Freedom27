"""Regression tests for metadata-only IPSW manifest comparisons."""
import unittest

from research.scripts.compare_ipsw_manifest_inventories import compare_inventories


def inventory(build, components, product="iPhone17,4", device_class="D48AP", verified=True):
    return {
        "integrity_verified_against_pinned_values": verified,
        "product_type": product,
        "device_class": device_class,
        "source_file_name": f"build-{build}.ipsw",
        "source_sha256": ("a" if build == "23G83" else "b") * 64,
        "source_size_bytes": 100,
        "build_identities": [{
            "build_version": build,
            "variant": "Customer Erase Install (IPSW)",
            "components": components,
        }],
    }


class CompareIpswManifestInventoriesTests(unittest.TestCase):
    def test_reports_manifest_digest_changes_without_claiming_binary_diff(self):
        before = inventory("23G83", [
            {"name": "KernelCache", "path": "kernel.old", "digest_hex": "a" * 96,
             "member_sha256": "a" * 64, "member_size_bytes": 100, "member_hash_algorithm": "sha256",
             "is_encrypted": True},
            {"name": "OldComponent", "path": "old.bin"},
        ])
        after = inventory("24A437", [
            {"name": "KernelCache", "path": "kernel.new", "digest_hex": "b" * 96,
             "member_sha256": "b" * 64, "member_size_bytes": 100, "member_hash_algorithm": "sha256",
             "is_encrypted": True},
            {"name": "NewComponent", "path": "new.bin"},
        ])
        result = compare_inventories(before, after)
        self.assertEqual(result["metadata_changed_entry_count"], 1)
        self.assertEqual(result["added_entry_count"], 1)
        self.assertEqual(result["absent_entry_count"], 1)
        self.assertEqual(result["change_record_count"], 3)
        self.assertEqual(result["field_change_counts"], {"digest_hex": 1, "member_sha256": 1, "path": 1})
        self.assertTrue(result["interpretation"]["component_payload_bytes_compared"])
        self.assertEqual(result["interpretation"]["raw_member_hash_comparison_names"], ["KernelCache"])
        self.assertFalse(result["interpretation"]["cve_attribution_performed"])
        statuses = {item["name"]: item["status"] for item in result["changes"]}
        self.assertEqual(statuses["KernelCache"], "metadata_changed")
        self.assertEqual(statuses["OldComponent"], "absent_in_after")
        self.assertEqual(statuses["NewComponent"], "added_in_after")

    def test_separates_same_named_components_by_install_variant(self):
        before = inventory("23G83", [
            {"name": "AVE", "digest_hex": "a" * 96},
        ])
        before["build_identities"].append({
            "build_version": "23G83", "variant": "Recovery Customer Install",
            "components": [{"name": "AVE", "digest_hex": "c" * 96}],
        })
        after = inventory("24A437", [{"name": "AVE", "digest_hex": "b" * 96}])
        after["build_identities"].append({
            "build_version": "24A437", "variant": "Recovery Customer Install",
            "components": [{"name": "AVE", "digest_hex": "d" * 96}],
        })
        result = compare_inventories(before, after)
        self.assertEqual(result["metadata_changed_entry_count"], 2)
        self.assertEqual({item["variant"] for item in result["changes"]}, {
            "Customer Erase Install (IPSW)", "Recovery Customer Install"
        })

    def test_rejects_cross_device_comparison(self):
        with self.assertRaisesRegex(ValueError, "product_type mismatch"):
            compare_inventories(inventory("23G83", []), inventory("24A437", [], "iPhone18,1"))

    def test_rejects_cross_board_comparison(self):
        with self.assertRaisesRegex(ValueError, "device_class mismatch"):
            compare_inventories(inventory("23G83", []), inventory("24A437", [], device_class="D73AP"))

    def test_rejects_unverified_input(self):
        with self.assertRaisesRegex(ValueError, "before inventory is not hash-verified"):
            compare_inventories(inventory("23G83", [], verified=False), inventory("24A437", []))


if __name__ == "__main__":
    unittest.main()
