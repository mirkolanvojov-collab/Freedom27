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
                    "KernelCache": {"Path": "kernelcache.release", "Digest": bytes.fromhex("ab" * 20),
                                    "IsEncrypted": True},
                    "RestoreRamDisk": {"Path": "restore.dmg", "Digest": bytes.fromhex("cd" * 20),
                                       "Trusted": True},
                },
            },
            {
                "ProductType": "iPhone17,3",
                "Info": {"DeviceClass": "D47AP", "Variant": "Other"},
                "Manifest": {"KernelCache": {"Path": "other-kernel"}},
            },
        ]
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("BuildManifest.plist", plistlib.dumps(manifest))
        archive.writestr("unrelated.bin", b"not extracted")
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
        self.assertEqual(identity["components"][0]["digest_algorithm"], "sha1")
        self.assertFalse(result["device_modified"])
        self.assertFalse(result["exploit_executed"])

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
            inventory_ipsw(self.path, self.sha, self.size, "iPhone17,4", "D47AP")

    def test_invalid_pinned_digest_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "64 hexadecimal"):
            inventory_ipsw(self.path, "not-a-hash", self.size, "iPhone17,4", "D48AP")


if __name__ == "__main__":
    unittest.main()
