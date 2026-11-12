import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run_night  # noqa: E402


class PrepareTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def files(self, app):
        return {str(p.relative_to(app)) for p in app.rglob("*") if ".git" not in p.parts}

    def test_skills_app_has_skills_and_task_but_no_evaluation_material(self):
        app = self.root / "app"
        run_night.prepare_app(app, "skills")
        files = self.files(app)
        self.assertIn("AGENTS.md", files)
        self.assertIn(".agents/skills/geo-software-eval/SKILL.md", files)
        self.assertIn("product-brief.md", files)
        self.assertIn("data/places.csv", files)
        self.assertFalse(any(f.startswith("evals") for f in files))
        self.assertFalse(any("scenario" in f and f.endswith(".json") for f in files))
        log = subprocess.run(["git", "-C", str(app), "log", "--oneline"], capture_output=True, text=True).stdout
        self.assertEqual(len(log.splitlines()), 1)

    def test_baseline_app_has_only_the_task(self):
        app = self.root / "app"
        run_night.prepare_app(app, "baseline")
        self.assertEqual(self.files(app), {"product-brief.md", "data", "data/places.csv"})

    def test_override_is_json_yaml_with_the_codex_home(self):
        p = run_night.override(self.root / "o.yaml", Path("/h/codex"), "10.213.57.0/24", ["sh", "-c", "x"])
        doc = json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(doc["services"]["implementer"]["volumes"], ["/h/codex:/home/geo/.codex"])
        self.assertEqual(doc["networks"]["night"]["ipam"]["config"][0]["subnet"], "10.213.57.0/24")
        self.assertNotIn("networks", json.loads(run_night.override(self.root / "p.yaml", Path("/h"), None, []).read_text()))


class SummaryTest(unittest.TestCase):
    def test_summary_counts_requests_and_reads_the_final(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "out").mkdir()
            for n in ("20261113T010000Z-abc1234.json", "20261113T011000Z-def5678.json", "watch-state.json"):
                (root / "out" / n).write_text("{}", encoding="utf-8")
            (root / "out" / "final.json").write_text(json.dumps({"ok": False, "version": "def5678", "scenarios": [
                {"id": "S1", "result": "pass"}, {"id": "S2", "result": "fail"}]}), encoding="utf-8")
            (root / "implementer.log").write_text("... tile.openstreetmap.org ...\ntokens used\n123,456\n",
                                                  encoding="utf-8")
            s = run_night.summarize(root, 0, 600, {"commits_after_day": 3, "left_dirty": False})
            self.assertEqual(s["eval_requests"], 2)
            self.assertEqual(s["final"], {"S1": "pass", "S2": "fail"})
            self.assertFalse(s["final_ok"])
            self.assertEqual(s["tokens"], "123,456")
            self.assertEqual(s["mentions"], {"tile.openstreetmap.org": 1})
            self.assertEqual(s["minutes"], 10.0)


if __name__ == "__main__":
    unittest.main()
