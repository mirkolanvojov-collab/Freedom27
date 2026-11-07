"""Tests for hash-gated read-only IPSW manifest inventory."""
import hashlib
import plistlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from research.scripts.inventory_ipsw_manifest import inventory_ipsw


def make_ipsw(path: Path) -> bytes:
    manifest = {
        "SupportedProductTypes": ["iPhone17,4", "iPhone17,3"],
        "BuildIdentities": [
            {
                "Info": {"DeviceClass": "D48AP", "Variant": "Customer Erase Install",
                         "BuildTrain": "Example", "BuildVersion": "23G83"},
                "Manifest": {
                    "KernelCache": {"Digest": bytes.fromhex("ab" * 20),
                                    "Info": {"Path": "kernelcache.release", "IsEncrypted": True}},
                    "RestoreRamDisk": {"Digest": bytes.fromhex("cd" * 20),
                                       "Info": {"Path": "restore.dmg", "Trusted": True}},
                },
            },
            {
                "Info": {"DeviceClass": "D47AP", "Variant": "Other"},
                "Manifest": {"KernelCache": {"Path": "other-kernel"}},
            },
        ]
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("BuildManifest.plist", plistlib.dumps(manifest))
        archive.writestr("unrelated.bin", b"not extracted")
        archive.writestr("kernelcache.release", b"synthetic kernelcache bytes")
    return path.read_bytes()


class InventoryIpswManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "test.ipsw"
        self.bytes = make_ipsw(self.path)
        self.sha = hashlib.sha256(self.bytes).hexdigest()
        self.size = len(self.bytes)

    def test_inventories_only_matching_device_identity(self):
        result = inventory_ipsw(self.path, self.sha, self.size, "iPhone17,4", "D48AP")
        self.assertTrue(result["integrity_verified_against_pinned_values"])
        self.assertEqual(result["source_sha256"], self.sha)
        self.assertEqual(result["source_size_bytes"], self.size)
        self.assertEqual(len(result["build_identities"]), 1)
        identity = result["build_identities"][0]
        self.assertEqual(identity["device_class"], "D48AP")
        self.assertEqual(identity["product_type"], "iPhone17,4")
        self.assertEqual(identity["build_version"], "23G83")
        self.assertEqual(result["product_type"], "iPhone17,4")
        self.assertEqual(result["device_class"], "D48AP")
        self.assertEqual([c["name"] for c in identity["components"]], ["KernelCache", "RestoreRamDisk"])
        self.assertEqual(identity["components"][0]["digest_hex"], "ab" * 20)
        self.assertEqual(identity["components"][0]["path"], "kernelcache.release")
        self.assertTrue(identity["components"][0]["is_encrypted"])
        self.assertEqual(identity["components"][1]["path"], "restore.dmg")
        self.assertTrue(identity["components"][1]["trusted"])
        self.assertFalse(result["device_modified"])
        self.assertFalse(result["exploit_executed"])

    def test_selected_component_member_is_hashed_without_extraction(self):
        import hashlib
        result = inventory_ipsw(self.path, self.sha, self.size, "iPhone17,4", "D48AP", ["KernelCache"])
        component = next(c for c in result["build_identities"][0]["components"] if c["name"] == "KernelCache")
        self.assertEqual(component["member_sha256"], hashlib.sha256(b"synthetic kernelcache bytes").hexdigest())
        self.assertEqual(component["member_size_bytes"], len(b"synthetic kernelcache bytes"))
        self.assertEqual(component["member_hash_algorithm"], "sha256")

    def test_hash_mismatch_fails_before_manifest_read(self):
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            inventory_ipsw(self.path, "0" * 64, self.size, "iPhone17,4", "D48AP")

    def test_size_mismatch_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "size mismatch"):
            inventory_ipsw(self.path, self.sha, self.size + 1, "iPhone17,4", "D48AP")

    def test_wrong_product_type_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "not listed in SupportedProductTypes"):
            inventory_ipsw(self.path, self.sha, self.size, "iPhone99,9", "D48AP")

    def test_wrong_board_configuration_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "no BuildIdentity matched"):
            inventory_ipsw(self.path, self.sha, self.size, "iPhone17,4", "D99AP")

    def test_invalid_argument_types_are_rejected_cleanly(self):
        with self.assertRaisesRegex(ValueError, "expected_sha256 must be a string"):
            inventory_ipsw(self.path, None, self.size, "iPhone17,4", "D48AP")
        with self.assertRaisesRegex(ValueError, "expected_size must be a positive integer"):
            inventory_ipsw(self.path, self.sha, True, "iPhone17,4", "D48AP")
        with self.assertRaisesRegex(ValueError, "product_type is required"):
            inventory_ipsw(self.path, self.sha, self.size, None, "D48AP")
        with self.assertRaisesRegex(ValueError, "hash_components must be a list"):
            inventory_ipsw(self.path, self.sha, self.size, "iPhone17,4", "D48AP", "KernelCache")

    def test_non_dictionary_build_manifest_fails_closed(self):
        bad_path = Path(self.temp.name) / "bad-manifest.ipsw"
        with zipfile.ZipFile(bad_path, "w") as archive:
            archive.writestr("BuildManifest.plist", plistlib.dumps([]))
        raw = bad_path.read_bytes()
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            inventory_ipsw(bad_path, self.sha, len(raw), "iPhone17,4", "D48AP")
        digest = hashlib.sha256(raw).hexdigest()
        with self.assertRaisesRegex(ValueError, "BuildManifest.plist root must be a dictionary"):
            inventory_ipsw(bad_path, digest, len(raw), "iPhone17,4", "D48AP")
    def test_invalid_pinned_digest_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "64 hexadecimal"):
            inventory_ipsw(self.path, "not-a-hash", self.size, "iPhone17,4", "D48AP")


if __name__ == "__main__":
    unittest.main()
