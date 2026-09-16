import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / ".github/skills/custom-release-notes"


class SkillPackageTest(unittest.TestCase):
    def test_frontmatter_name_matches_folder(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.search(r"^name:\s*([^\n]+)$", skill, re.MULTILINE)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1).strip(), SKILL_ROOT.name)

    def test_referenced_resources_exist(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        paths = re.findall(
            r"`((?:references|scripts|templates)/[^`\s]+)`",
            skill,
        )
        missing = [path for path in paths if not (SKILL_ROOT / path).is_file()]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()