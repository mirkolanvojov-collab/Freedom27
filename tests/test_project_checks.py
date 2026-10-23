import json
import tempfile
import unittest
from pathlib import Path

from Framework.project_checks import check_project


class ProjectCheckTests(unittest.TestCase):
    def make_root(self, root: Path) -> None:
        (root / "research").mkdir()
        (root / "config.json").write_text(json.dumps({
            "project": "Freedom27",
            "target_os": "iOS 27 (planned; not verified)",
            "package_manager_preference": "Cydia (goal; integration unverified)",
            "project_status": "research-scaffold",
            "working_jailbreak": False,
        }), encoding="utf-8")
        (root / "research" / "vulnerability_registry.json").write_text(
            json.dumps({"schema_version": 1, "entries": []}), encoding="utf-8"
        )

    def test_valid_scaffold_metadata_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_root(root)
            self.assertEqual(check_project(root), [])

    def test_claiming_working_jailbreak_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_root(root)
            config_path = root / "config.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["working_jailbreak"] = True
            config_path.write_text(json.dumps(config), encoding="utf-8")
            self.assertTrue(any("working_jailbreak must be false" in item
                                for item in check_project(root)))

    def test_duplicate_registry_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_root(root)
            path = root / "research" / "vulnerability_registry.json"
            entry = {"id": "same", "title": "Example", "source_url": "https://example.org",
                     "status": "unverified"}
            path.write_text(json.dumps({"schema_version": 1, "entries": [entry, entry]}),
                            encoding="utf-8")
            self.assertTrue(any("duplicate id" in item for item in check_project(root)))


if __name__ == "__main__":
    unittest.main()
