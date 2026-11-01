import hashlib
import plistlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from research.scripts.verify_restore_manifest import verify


class RestoreManifestTests(unittest.TestCase):
    def fixture(self, root, **overrides):
        manifest = {
            "ProductVersion": "26.6.1",
            "ProductBuildVersion": "23G83",
            "SupportedProductTypes": ["iPhone17,4"],
            "BuildIdentities": [
                {"Info": {"DeviceClass": "D94AP", "Variant": "Customer Upgrade Install"},
                 "ApChipID": 0x1234, "ApBoardID": 0x56}
            ],
        }
        manifest.update(overrides)
        path = root / "BuildManifest.plist"
        path.write_bytes(plistlib.dumps(manifest))
        return path

    def test_accepts_exact_device_and_build(self):
        with tempfile.TemporaryDirectory() as directory:
            report = verify(self.fixture(Path(directory)), "iPhone17,4", "26.6.1", "23G83")
            self.assertEqual(report["verification"], "passed")
            self.assertEqual(report["manifest_identity"]["supported_product_types"], ["iPhone17,4"])
            self.assertEqual(len(report["manifest_identity"]["build_identities"]), 1)
            self.assertEqual(len(report["manifest_sha256"]), 64)
            self.assertIsNone(report["restore_image"])

    def test_binds_full_restore_image_digest_and_embedded_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.fixture(root)
            image = root / "fixture.ipsw"
            with zipfile.ZipFile(image, "w", compression=zipfile.ZIP_STORED) as archive:
                archive.write(manifest, "BuildManifest.plist")
                archive.writestr("dummy.bin", b"firmware bytes")
            report = verify(manifest, "iPhone17,4", "26.6.1", "23G83", image)
            self.assertTrue(report["restore_image"]["archive_manifest_matches"])
            self.assertEqual(report["restore_image"]["manifest_member"], "BuildManifest.plist")
            self.assertEqual(report["restore_image"]["sha256"], hashlib.sha256(image.read_bytes()).hexdigest())
            self.assertEqual(report["restore_image"]["size_bytes"], image.stat().st_size)

    def test_rejects_embedded_manifest_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.fixture(root)
            image = root / "fixture.ipsw"
            with zipfile.ZipFile(image, "w") as archive:
                archive.writestr("BuildManifest.plist", b"not the verified manifest")
            with self.assertRaisesRegex(ValueError, "differs byte-for-byte"):
                verify(manifest, "iPhone17,4", "26.6.1", "23G83", image)

    def test_rejects_missing_embedded_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.fixture(root)
            image = root / "fixture.ipsw"
            with zipfile.ZipFile(image, "w") as archive:
                archive.writestr("other.plist", b"x")
            with self.assertRaisesRegex(ValueError, "no root BuildManifest"):
                verify(manifest, "iPhone17,4", "26.6.1", "23G83", image)

    def test_rejects_wrong_build(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "ProductBuildVersion mismatch"):
                verify(self.fixture(Path(directory)), "iPhone17,4", "26.6.1", "23G90")

    def test_rejects_wrong_product(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "SupportedProductTypes"):
                verify(self.fixture(Path(directory)), "iPhone17,3", "26.6.1", "23G83")

    def test_rejects_missing_build_identities(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "BuildIdentities"):
                verify(self.fixture(Path(directory), BuildIdentities=[]), "iPhone17,4", "26.6.1", "23G83")


if __name__ == "__main__":
    unittest.main()
