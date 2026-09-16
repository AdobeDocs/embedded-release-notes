import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "toast_registry.py"
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "toast-entry.json"


class ToastRegistryTest(unittest.TestCase):
    def run_script(self, registry, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--registry", str(registry), *arguments],
            capture_output=True,
            text=True,
        )

    def create_registry(self, root):
        registry = root / "toast.json"
        registry.write_text(
            '{"schema_version": 1, "surfaces": {}}\n',
            encoding="utf-8",
        )
        request_path = root / "requests/ajo/2026/09/smoke-test.json"
        request_path.parent.mkdir(parents=True)
        request_path.write_text(
            json.dumps(
                {
                    "products": ["ajo"],
                    "deliverables": ["hub", "toast"],
                    "year": 2026,
                    "month": 6,
                    "slug": "general",
                    "toast": {"surface": "ajo"},
                    "output_directory": "generated/ajo/2026/09/smoke-test/",
                }
            ),
            encoding="utf-8",
        )
        hub_path = root / "generated/ajo/2026/09/smoke-test/hub.html"
        hub_path.parent.mkdir(parents=True)
        hub_path.write_text("<!DOCTYPE html><title>Test</title>", encoding="utf-8")
        return registry

    def test_upsert_adds_and_replaces_surface(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry = self.create_registry(root)
            first = self.run_script(registry, "upsert", "--entry", str(FIXTURE))
            self.assertEqual(first.returncode, 0, first.stderr)

            replacement = json.loads(FIXTURE.read_text(encoding="utf-8"))
            replacement["id"] = "ajo-2026-07-general"
            replacement["release"]["month"] = 7
            replacement["action"]["href"] = "generated/ajo/2026/07/general/hub.html"
            replacement["source_request"] = "requests/ajo/2026/07/general.json"
            replacement_request = root / replacement["source_request"]
            replacement_request.parent.mkdir(parents=True)
            replacement_request.write_text(
                json.dumps(
                    {
                        "products": ["ajo"],
                        "deliverables": ["hub", "toast"],
                        "year": 2026,
                        "month": 7,
                        "slug": "general",
                        "toast": {"surface": "ajo"},
                        "output_directory": "generated/ajo/2026/07/general/",
                    }
                ),
                encoding="utf-8",
            )
            replacement_hub = root / replacement["action"]["href"]
            replacement_hub.parent.mkdir(parents=True)
            replacement_hub.write_text(
                "<!DOCTYPE html><title>Replacement</title>",
                encoding="utf-8",
            )
            entry_path = root / "replacement.json"
            entry_path.write_text(json.dumps(replacement), encoding="utf-8")
            second = self.run_script(registry, "upsert", "--entry", str(entry_path))
            self.assertEqual(second.returncode, 0, second.stderr)

            surfaces = json.loads(registry.read_text(encoding="utf-8"))["surfaces"]
            self.assertEqual(len(surfaces), 1)
            self.assertEqual(surfaces["ajo"]["id"], "ajo-2026-07-general")

    def test_rejects_id_that_does_not_match_release(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            registry = self.create_registry(Path(temporary_directory))
            entry = json.loads(FIXTURE.read_text(encoding="utf-8"))
            entry["id"] = "ajo-2026-06-wrong"
            entry_path = Path(temporary_directory) / "wrong-id.json"
            entry_path.write_text(json.dumps(entry), encoding="utf-8")
            result = self.run_script(registry, "upsert", "--entry", str(entry_path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("id must equal ajo-2026-06-general", result.stderr)

    def test_resolve_returns_the_routed_toast(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry = self.create_registry(root)
            self.assertEqual(
                self.run_script(registry, "upsert", "--entry", str(FIXTURE)).returncode,
                0,
            )
            result = self.run_script(
                registry,
                "resolve",
                "--surface",
                "ajo",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["id"], "ajo-2026-06-general")

    def test_rejects_surface_key_mismatch(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.create_registry(root)
            entry = json.loads(FIXTURE.read_text(encoding="utf-8"))
            registry = root / "toast.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "surfaces": {"aep": entry},
                    }
                ),
                encoding="utf-8",
            )
            result = self.run_script(registry, "validate")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("surface key aep differs from its value", result.stderr)


if __name__ == "__main__":
    unittest.main()