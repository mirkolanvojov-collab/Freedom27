import plistlib
import tempfile
import unittest
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
