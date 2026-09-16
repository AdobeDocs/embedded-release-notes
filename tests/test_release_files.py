import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "release_files.py"


class ReleaseFilesTest(unittest.TestCase):
    def run_script(self, repo_root, *arguments):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repo-root",
                str(repo_root),
                *arguments,
            ],
            capture_output=True,
            text=True,
        )

    def create_release(self, root):
        request_path = root / "requests/ajo/2026/09/smoke-test.json"
        request_path.parent.mkdir(parents=True)
        output_path = root / "generated/ajo/2026/09/smoke-test"
        output_path.mkdir(parents=True)
        (output_path / "hub.html").write_text(
            "<!DOCTYPE html><title>Test</title>",
            encoding="utf-8",
        )
        request = {
            "slug": "smoke-test",
            "status": "generated",
            "deliverables": ["hub", "toast"],
            "output_directory": "generated/ajo/2026/09/smoke-test/",
            "toast": {"surface": "ajo"},
        }
        request_path.write_text(json.dumps(request), encoding="utf-8")
        registry = {
            "schema_version": 1,
            "surfaces": {
                "ajo": {
                    "id": "ajo-2026-06-smoke-test",
                    "surface": "ajo",
                    "release": {
                        "year": 2026,
                        "month": 6,
                        "slug": "smoke-test",
                        "label": "June '26",
                    },
                    "action": {
                        "label": "See all updates",
                        "href": "generated/ajo/2026/09/smoke-test/hub.html",
                    },
                    "source_request": "requests/ajo/2026/09/smoke-test.json",
                }
            },
        }
        (root / "toast.json").write_text(json.dumps(registry), encoding="utf-8")
        return request_path

    def test_rename_updates_request_output_and_toast_reference(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.create_release(root)
            result = self.run_script(
                root,
                "rename",
                "--request",
                "requests/ajo/2026/09/smoke-test.json",
                "--new-slug",
                "general-release",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            new_request = root / "requests/ajo/2026/09/general-release.json"
            self.assertTrue(new_request.is_file())
            self.assertTrue((root / "generated/ajo/2026/09/general-release").is_dir())
            request = json.loads(new_request.read_text(encoding="utf-8"))
            self.assertEqual(request["slug"], "general-release")
            registry = json.loads((root / "toast.json").read_text(encoding="utf-8"))
            toast = registry["surfaces"]["ajo"]
            self.assertEqual(toast["id"], "ajo-2026-06-general-release")
            self.assertEqual(
                toast["source_request"],
                "requests/ajo/2026/09/general-release.json",
            )
            self.assertEqual(
                toast["action"]["href"],
                "generated/ajo/2026/09/general-release/hub.html",
            )

    def test_validate_detects_missing_source_request(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.create_release(root)
            (root / "requests/ajo/2026/09/smoke-test.json").unlink()
            result = self.run_script(root, "validate")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("references missing request", result.stderr)

    def test_generated_request_requires_hub_and_toast_route(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.create_release(root)
            (root / "generated/ajo/2026/09/smoke-test/hub.html").unlink()
            (root / "toast.json").write_text(
                '{"schema_version": 1, "surfaces": {}}',
                encoding="utf-8",
            )
            result = self.run_script(root, "validate")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("generated request is missing hub", result.stderr)
            self.assertIn("requires exactly one surface entry", result.stderr)


if __name__ == "__main__":
    unittest.main()