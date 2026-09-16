import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / ".github/skills"
CUSTOM_SKILL_ROOT = SKILLS_ROOT / "custom-release-notes"


class SkillPackageTest(unittest.TestCase):
    def test_frontmatter_name_matches_folder(self):
        for skill_root in SKILLS_ROOT.iterdir():
            if not skill_root.is_dir():
                continue
            with self.subTest(skill=skill_root.name):
                skill_path = skill_root / "SKILL.md"
                self.assertTrue(skill_path.is_file())
                skill = skill_path.read_text(encoding="utf-8")
                match = re.search(r"^name:\s*([^\n]+)$", skill, re.MULTILINE)
                self.assertIsNotNone(match)
                self.assertEqual(match.group(1).strip(), skill_root.name)

    def test_referenced_resources_exist(self):
        skill = (CUSTOM_SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        paths = re.findall(
            r"`((?:references|scripts|templates)/[^`\s]+)`",
            skill,
        )
        missing = [
            path for path in paths if not (CUSTOM_SKILL_ROOT / path).is_file()
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()