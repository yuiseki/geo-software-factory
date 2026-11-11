import datetime
import pathlib
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import check  # noqa: E402

DISCLOSURE = "- 利害関係の開示: このスキル集の作者は X に関係している。"


def make_repo(files: dict[str, str]) -> pathlib.Path:
    root = pathlib.Path(tempfile.mkdtemp())
    for path, text in files.items():
        p = root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(textwrap.dedent(text).lstrip("\n"))
    return root


def good_files() -> dict[str, str]:
    return {
        "AGENTS.md": f"# x\n\n{DISCLOSURE}\n",
        ".agents/skills/AGENTS.md": "# rules\n",
        ".agents/skills/TODO.md": "# TODO\n\n- [x] demo (2/2)\n  - [x] SKILL.md\n  - [x] references/a.md\n",
        ".agents/skills/demo/SKILL.md": f"---\nname: demo\ndescription: does demo things\n---\n\n# demo\n\n[a](references/a.md)\n\n{DISCLOSURE}\n",
        ".agents/skills/demo/references/a.md": "# a\n\n| 確かめた日 | 2026-11-10 |\n",
    }


class CheckTest(unittest.TestCase):
    def run_check(self, files, today=datetime.date(2026, 11, 11)):
        return check.check(make_repo(files), today=today, max_age_days=90)

    def test_good_repo_has_no_errors(self):
        errors, warnings = self.run_check(good_files())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_name_must_match_directory_and_description_is_required(self):
        f = good_files()
        f[".agents/skills/demo/SKILL.md"] = "---\nname: other\n---\n# demo\n"
        errors, _ = self.run_check(f)
        self.assertIn(".agents/skills/demo/SKILL.md: name 'other' does not match directory 'demo'", errors)
        self.assertIn(".agents/skills/demo/SKILL.md: missing description", errors)

    def test_skill_md_must_stay_under_200_lines(self):
        f = good_files()
        f[".agents/skills/demo/SKILL.md"] += "x\n" * 200
        errors, _ = self.run_check(f)
        self.assertTrue(any("over 200 lines" in e for e in errors))

    def test_broken_relative_links_are_errors_but_urls_and_anchors_are_not(self):
        f = good_files()
        f[".agents/skills/demo/references/a.md"] += "[x](missing.md) [y](https://example.com/z) [z](#here)\n"
        errors, _ = self.run_check(f)
        self.assertEqual([e for e in errors if "broken link" in e], [".agents/skills/demo/references/a.md: broken link missing.md"])

    def test_em_dash_and_local_paths_are_errors(self):
        f = good_files()
        f[".agents/skills/demo/references/a.md"] += "a — b\nsee /home/someone/x and /Workspaces/y\n"
        f[".agents/skills/demo/references/a.md"] += "fine: https://www.arcgis.com/home/item.html\n"
        errors, _ = self.run_check(f)
        self.assertIn(".agents/skills/demo/references/a.md:4: em dash", errors)
        self.assertIn(".agents/skills/demo/references/a.md:5: local path", errors)
        self.assertEqual(len([e for e in errors if "local path" in e]), 1)

    def test_disclosure_lines_must_match_agents_md(self):
        f = good_files()
        f[".agents/skills/demo/SKILL.md"] = f[".agents/skills/demo/SKILL.md"].replace("X に関係している", "Y に関係している")
        errors, _ = self.run_check(f)
        self.assertIn(".agents/skills/demo/SKILL.md: disclosure differs from AGENTS.md", errors)

    def test_todo_must_list_every_file_with_correct_counts(self):
        f = good_files()
        f[".agents/skills/demo/references/b.md"] = "# b\n"
        f[".agents/skills/TODO.md"] = "# TODO\n\n- [x] demo (1/2)\n  - [x] SKILL.md\n  - [x] references/a.md\n  - [x] references/gone.md\n"
        errors, _ = self.run_check(f)
        self.assertIn("TODO.md: demo is missing references/b.md", errors)
        self.assertIn("TODO.md: demo lists references/gone.md, which does not exist", errors)
        self.assertIn("TODO.md: demo says (1/2) but has 3/3", errors)

    def test_todo_may_list_a_directory_of_data_as_one_entry(self):
        f = good_files()
        f[".agents/skills/demo/assets/cards/one.md"] = "# one\n"
        f[".agents/skills/demo/assets/cards/two.md"] = "# two\n"
        f[".agents/skills/TODO.md"] = "# TODO\n\n- [x] demo (3/3)\n  - [x] SKILL.md\n  - [x] references/a.md\n  - [x] assets/cards/\n"
        errors, _ = self.run_check(f)
        self.assertEqual(errors, [])

    def test_a_listed_directory_must_exist_and_hold_files(self):
        f = good_files()
        f[".agents/skills/TODO.md"] = "# TODO\n\n- [x] demo (3/3)\n  - [x] SKILL.md\n  - [x] references/a.md\n  - [x] assets/cards/\n"
        errors, _ = self.run_check(f)
        self.assertIn("TODO.md: demo lists assets/cards/, which does not exist", errors)

    def test_old_checked_dates_are_warnings(self):
        errors, warnings = self.run_check(good_files(), today=datetime.date(2027, 3, 1))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [".agents/skills/demo/references/a.md: checked 2026-11-10, 111 days ago"])

    def test_unfilled_template_dates_are_ignored(self):
        f = good_files()
        f[".agents/skills/demo/references/a.md"] = "# a\n\n| 確かめた日 | [記入] |\n"
        _, warnings = self.run_check(f, today=datetime.date(2027, 3, 1))
        self.assertEqual(warnings, [])

    def test_every_service_card_states_what_it_is_and_how_it_pays(self):
        f = good_files()
        rows = "".join(f"| {r} | x |\n" for r in check.CARD_ROWS)
        f[".agents/skills/demo/assets/services/README.md"] = "# index\n"
        f[".agents/skills/demo/assets/services/good.md"] = f"# good\n\n| 項目 | 内容 |\n|---|---|\n{rows}"
        f[".agents/skills/demo/assets/services/thin.md"] = "# thin\n\n| 項目 | 内容 |\n|---|---|\n| 一行で | x |\n| 描画 | y |\n"
        f[".agents/skills/TODO.md"] = "# TODO\n\n- [x] demo (3/3)\n  - [x] SKILL.md\n  - [x] references/a.md\n  - [x] assets/services/\n"
        errors, _ = self.run_check(f)
        thin = [e for e in errors if "assets/services/" in e]
        self.assertEqual(thin, [f".agents/skills/demo/assets/services/thin.md: card has no row '{r}'" for r in check.CARD_ROWS if r != "一行で"])

    def test_a_card_row_left_empty_is_an_error(self):
        f = good_files()
        rows = "".join(f"| {r} | {'' if r == '運営' else 'x'} |\n" for r in check.CARD_ROWS)
        f[".agents/skills/demo/assets/services/a.md"] = f"# a\n\n| 項目 | 内容 |\n|---|---|\n{rows}"
        f[".agents/skills/TODO.md"] = "# TODO\n\n- [x] demo (3/3)\n  - [x] SKILL.md\n  - [x] references/a.md\n  - [x] assets/services/\n"
        errors, _ = self.run_check(f)
        self.assertEqual([e for e in errors if "assets/services/" in e], [".agents/skills/demo/assets/services/a.md: card row '運営' is empty"])


if __name__ == "__main__":
    unittest.main()
