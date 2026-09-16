import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "new_request.py"


class NewRequestTest(unittest.TestCase):
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

    def test_creates_versioned_request_and_output_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            repo_root = Path(temporary_directory)
            result = self.run_script(
                repo_root,
                "--products",
                "ajo",
                "aep",
                "--year",
                "2026",
                "--month",
                "9",
                "--slug",
                "loyalty-admin",
                "--theme",
                "Loyalty",
                "--persona",
                "Admin",
                "--deliverables",
                "hub",
                "toast",
                "--surface",
                "ajo-aep",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            request_path = (
                repo_root
                / "requests/ajo-aep/2026/09/loyalty-admin.json"
            )
            output_path = repo_root / "generated/ajo-aep/2026/09/loyalty-admin"
            self.assertTrue(request_path.is_file())
            self.assertTrue(output_path.is_dir())
            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(request["products"], ["ajo", "aep"])
            self.assertEqual(request["output_directory"], "generated/ajo-aep/2026/09/loyalty-admin/")
            self.assertEqual(request["toast"]["surface"], "ajo-aep")

    def test_rejects_non_kebab_case_slug(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = self.run_script(
                temporary_directory,
                "--products",
                "ajo",
                "--slug",
                "Loyalty Admin",
                "--theme",
                "Loyalty",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("lowercase ASCII kebab-case", result.stderr)

    def test_toast_defaults_surface_and_adds_hub(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = self.run_script(
                temporary_directory,
                "--products",
                "ajo",
                "--slug",
                "general",
                "--theme",
                "General",
                "--deliverables",
                "toast",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            request_path = Path(temporary_directory) / "requests/ajo/2026/09/general.json"
            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(request["toast"]["surface"], "ajo")
            self.assertEqual(request["deliverables"], ["hub", "toast"])


if __name__ == "__main__":
    unittest.main()