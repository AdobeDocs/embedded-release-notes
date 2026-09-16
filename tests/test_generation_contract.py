import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NEW_REQUEST = REPO_ROOT / "scripts" / "new_request.py"
TOAST_REGISTRY = REPO_ROOT / "scripts" / "toast_registry.py"


class GenerationContractTest(unittest.TestCase):
    def run_command(self, *arguments):
        return subprocess.run(
            [sys.executable, *map(str, arguments)],
            capture_output=True,
            text=True,
        )

    def create_release(self, root, month, slug):
        result = self.run_command(
            NEW_REQUEST,
            "--repo-root",
            root,
            "--products",
            "ajo",
            "--deliverables",
            "hub",
            "toast",
            "--year",
            "2026",
            "--month",
            str(month),
            "--slug",
            slug,
            "--theme",
            "General",
            "--persona",
            "Generic",
            "--surface",
            "ajo",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        request_path = root / f"requests/ajo/2026/{month:02d}/{slug}.json"
        request = json.loads(request_path.read_text(encoding="utf-8"))
        hub_path = root / request["output_directory"] / "hub.html"
        hub_path.write_text("<!DOCTYPE html><title>Release</title>", encoding="utf-8")

        entry = {
            "id": f"ajo-2026-{month:02d}-{slug}",
            "surface": "ajo",
            "release": {
                "year": 2026,
                "month": month,
                "slug": slug,
                "label": f"2026-{month:02d}",
            },
            "title": "What's new for Journey Optimizer",
            "items": [
                {
                    "icon": {"name": "journey", "foreground": "#4B3CB7", "background": "#8174E8"},
                    "title": "First",
                    "description": "First update.",
                },
                {
                    "icon": {"name": "optimize", "foreground": "#8D153A", "background": "#ED4776"},
                    "title": "Second",
                    "description": "Second update.",
                },
            ],
            "action": {
                "label": "See all updates",
                "href": f"{request['output_directory']}hub.html",
            },
            "dismiss": {"label": "Dismiss"},
            "source_request": request_path.relative_to(root).as_posix(),
        }
        entry_path = root / f"{slug}.json"
        entry_path.write_text(json.dumps(entry), encoding="utf-8")
        return entry_path

    def test_request_hub_and_toast_route_are_consistent(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry = root / "toast.json"
            registry.write_text(
                '{"schema_version": 1, "surfaces": {}}\n',
                encoding="utf-8",
            )

            first = self.create_release(root, 9, "first")
            upsert_first = self.run_command(
                TOAST_REGISTRY,
                "--registry",
                registry,
                "upsert",
                "--entry",
                first,
            )
            self.assertEqual(upsert_first.returncode, 0, upsert_first.stderr)

            second = self.create_release(root, 10, "second")
            upsert_second = self.run_command(
                TOAST_REGISTRY,
                "--registry",
                registry,
                "upsert",
                "--entry",
                second,
            )
            self.assertEqual(upsert_second.returncode, 0, upsert_second.stderr)

            validation = self.run_command(
                TOAST_REGISTRY,
                "--registry",
                registry,
                "validate",
            )
            self.assertEqual(validation.returncode, 0, validation.stderr)
            surfaces = json.loads(registry.read_text(encoding="utf-8"))["surfaces"]
            self.assertEqual(len(surfaces), 1)
            toast = surfaces["ajo"]
            self.assertEqual(toast["id"], "ajo-2026-10-second")
            self.assertTrue((root / toast["action"]["href"]).is_file())


if __name__ == "__main__":
    unittest.main()