import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "hub_links.py"
sys.path.insert(0, str(SCRIPT.parent))

from hub_links import find_violations, repair  # noqa: E402


NEW_TAB = 'target="_blank" rel="noopener noreferrer"'


class HubLinksTest(unittest.TestCase):
    def run_script(self, repo_root, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo-root", str(repo_root), *arguments],
            capture_output=True,
            text=True,
        )

    def write_hub(self, root, html):
        hub = root / "generated/ajo/2026/09/test/hub.html"
        hub.parent.mkdir(parents=True)
        hub.write_text(html, encoding="utf-8")
        return hub

    def test_flags_only_external_links_without_new_tab(self):
        html = (
            '<a href="#september" onclick="showTab(\'september\')">Tab</a>\n'
            '<a href="mailto:team@adobe.com">Mail</a>\n'
            f'<a href="https://example.com/ok" {NEW_TAB}>Ok</a>\n'
            '<a href="https://example.com/framed">Framed</a>\n'
            '<a href="http://example.com/no-rel" target="_blank">No rel</a>\n'
            '<a href="https://example.com/self" target="_self" rel="noopener noreferrer">Self</a>'
        )
        self.assertEqual(
            find_violations(html),
            [
                (4, "https://example.com/framed"),
                (5, "http://example.com/no-rel"),
                (6, "https://example.com/self"),
            ],
        )

    def test_repair_adds_attributes_and_preserves_others(self):
        html = (
            '<p><a class="learn" href="https://example.com/a">A</a> '
            '<a href="https://example.com/b" target="_self" rel="author">B</a> '
            '<a href="#soon">C</a></p>'
        )
        repaired, changed = repair(html)
        self.assertTrue(changed)
        self.assertEqual(
            repaired,
            f'<p><a class="learn" href="https://example.com/a" {NEW_TAB}>A</a> '
            '<a href="https://example.com/b" target="_blank" '
            'rel="author noopener noreferrer">B</a> '
            '<a href="#soon">C</a></p>',
        )
        self.assertEqual(find_violations(repaired), [])

    def test_repair_is_idempotent(self):
        repaired, _ = repair('<a href="https://example.com">A</a>')
        self.assertEqual(repair(repaired), (repaired, False))

    def test_check_fails_then_fix_repairs_hubs(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            hub = self.write_hub(root, '<a href="https://example.com/framed">A</a>')

            check = self.run_script(root, "check")
            self.assertNotEqual(check.returncode, 0)
            self.assertIn("generated/ajo/2026/09/test/hub.html:1", check.stderr)
            self.assertIn("https://example.com/framed", check.stderr)

            fix = self.run_script(root, "fix")
            self.assertEqual(fix.returncode, 0, fix.stderr)
            self.assertIn(NEW_TAB, hub.read_text(encoding="utf-8"))
            self.assertEqual(self.run_script(root, "check").returncode, 0)

    def test_published_hubs_open_external_links_in_new_tab(self):
        result = self.run_script(REPO_ROOT, "check")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
