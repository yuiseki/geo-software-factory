import http.server
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from functools import partial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run_eval  # noqa: E402

GOOD = {"type": "FeatureCollection", "features": [
    {"type": "Feature", "properties": {"name": "上野駅"}, "geometry": {"type": "Point", "coordinates": [139.777, 35.713]}},
    {"type": "Feature", "properties": {"name": "浅草寺"}, "geometry": {"type": "Point", "coordinates": [139.797, 35.715]}},
]}
SWAPPED = {"type": "FeatureCollection", "features": [
    {"type": "Feature", "properties": {"name": "上野駅"}, "geometry": {"type": "Point", "coordinates": [35.713, 139.777]}},
]}
SECRET_THRESHOLD = 7357  # a number that appears only in a scenario, never in feedback


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.site, self.app, self.scen, self.out = root / "site", root / "app", root / "scenarios", root / "out"
        for d in (self.site, self.app, self.scen, self.out):
            d.mkdir()
        (self.site / "index.html").write_text("<html>OpenStreetMap contributors</html>", encoding="utf-8")
        (self.site / "good.geojson").write_text(json.dumps(GOOD), encoding="utf-8")
        (self.site / "swapped.geojson").write_text(json.dumps(SWAPPED), encoding="utf-8")
        subprocess.run(["git", "init", "-q", str(self.app)], check=True)
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=str(self.site)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def scenario(self, sid, symptom, checks, name="利用者が上野の名所を地図で見つける"):
        (self.scen / f"{sid}.json").write_text(json.dumps(
            {"id": sid, "name": name, "symptom": symptom, "checks": checks}, ensure_ascii=False), encoding="utf-8")

    def run_eval(self, **kw):
        args = dict(scenarios=self.scen, base=self.base, app_repo=self.app, report=self.out / "report.json",
                    feedback=self.app / "eval-feedback.md")
        args.update(kw)
        return run_eval.run(**args)


class SeparationTest(Base):
    def test_refuses_scenarios_inside_the_app_repo(self):
        inside = self.app / "scenarios"
        inside.mkdir()
        with self.assertRaises(run_eval.Refused):
            self.run_eval(scenarios=inside)

    def test_refuses_a_report_inside_the_app_repo(self):
        with self.assertRaises(run_eval.Refused):
            self.run_eval(report=self.app / "report.json")

    def test_refuses_feedback_outside_the_app_repo(self):
        with self.assertRaises(run_eval.Refused):
            self.run_eval(feedback=self.out / "eval-feedback.md")


class JudgingTest(Base):
    def test_all_pass(self):
        self.scenario("S1", "名所が地図に出ない", [
            {"kind": "http", "path": "/", "status": 200, "contains": "OpenStreetMap"},
            {"kind": "geojson", "path": "/good.geojson", "bbox": [139.7, 35.6, 139.9, 35.8], "min_features": 2,
             "require": ["name"]},
        ])
        r = self.run_eval()
        self.assertTrue(r["ok"])
        self.assertEqual(r["scenarios"][0]["result"], "pass")
        self.assertIn("合格", (self.app / "eval-feedback.md").read_text(encoding="utf-8"))

    def test_failures_are_judged(self):
        self.scenario("S1", "名所の位置が海の上に出る", [
            {"kind": "geojson", "path": "/swapped.geojson", "bbox": [139.7, 35.6, 139.9, 35.8]}])
        self.scenario("S2", "帰属表示が見えない", [{"kind": "http", "path": "/", "contains": "Natural Earth"}])
        self.scenario("S3", "一覧が開けない", [{"kind": "http", "path": "/missing", "status": 200}])
        r = self.run_eval()
        self.assertFalse(r["ok"])
        self.assertEqual([s["result"] for s in r["scenarios"]], ["fail", "fail", "fail"])

    def test_command_check_uses_exit_code_and_only_observed_lines(self):
        script = self.scen / "s1_check.py"
        script.write_text(
            f"print('assert count >= {SECRET_THRESHOLD}')\nprint('OBSERVED: 地図の上に印が 0 個')\nraise SystemExit(1)\n",
            encoding="utf-8")
        self.scenario("S1", "名所の印が出ない", [{"kind": "command", "run": [sys.executable, "-I", str(script)]}])
        r = self.run_eval()
        self.assertEqual(r["scenarios"][0]["result"], "fail")
        fb = (self.app / "eval-feedback.md").read_text(encoding="utf-8")
        self.assertIn("地図の上に印が 0 個", fb)
        self.assertNotIn(str(SECRET_THRESHOLD), fb)
        # the full output stays in the evaluator's report
        self.assertIn(str(SECRET_THRESHOLD), (self.out / "report.json").read_text(encoding="utf-8"))

    def test_command_runs_with_the_base_url(self):
        script = self.scen / "env_check.py"
        script.write_text("import os\nraise SystemExit(0 if os.environ['EVAL_BASE_URL'].startswith('http') else 1)\n",
                          encoding="utf-8")
        self.scenario("S1", "x", [{"kind": "command", "run": [sys.executable, "-I", str(script)]}])
        self.assertTrue(self.run_eval()["ok"])

    def test_unknown_kind_is_an_error_not_a_pass(self):
        self.scenario("S1", "x", [{"kind": "telepathy"}])
        r = self.run_eval()
        self.assertEqual(r["scenarios"][0]["result"], "error")
        self.assertFalse(r["ok"])

    def test_no_scenarios_is_not_ok(self):
        self.assertFalse(self.run_eval()["ok"])


class LeakTest(Base):
    def test_feedback_has_symptoms_but_no_scenario_text_or_thresholds(self):
        self.scenario("S1", "名所の数が足りない", [
            {"kind": "geojson", "path": "/good.geojson", "min_features": SECRET_THRESHOLD,
             "bbox": [139.0, 35.0, 140.0, 36.0], "require": ["secret_property_name"]},
            {"kind": "http", "path": "/", "contains": "secret-needle-text"},
        ], name="秘密のシナリオの名前")
        self.run_eval()
        fb = (self.app / "eval-feedback.md").read_text(encoding="utf-8")
        self.assertIn("名所の数が足りない", fb)
        self.assertIn("/good.geojson", fb)
        for leaked in (str(SECRET_THRESHOLD), "秘密のシナリオの名前", "secret-needle-text", "secret_property_name",
                       "139.0", str(self.scen)):
            self.assertNotIn(leaked, fb)

    def test_feedback_names_the_version_judged(self):
        subprocess.run(["git", "-C", str(self.app), "-c", "user.email=t@example.invalid", "-c", "user.name=t",
                        "commit", "-q", "--allow-empty", "-m", "x"], check=True)
        rev = subprocess.run(["git", "-C", str(self.app), "rev-parse", "--short", "HEAD"], capture_output=True,
                             text=True, check=True).stdout.strip()
        self.scenario("S1", "x", [{"kind": "http", "path": "/"}])
        self.run_eval()
        self.assertIn(rev, (self.app / "eval-feedback.md").read_text(encoding="utf-8"))


class ContainerModeTest(Base):
    """In the isolated setup the evaluator has no app repo: the version comes from the implementer's request."""

    def test_runs_without_an_app_repo_and_names_the_given_version(self):
        self.scenario("S1", "x", [{"kind": "http", "path": "/"}])
        fb = self.out.parent / "feedback" / "eval-feedback.md"
        fb.parent.mkdir()
        r = self.run_eval(app_repo=None, feedback=fb, version="abc1234")
        self.assertTrue(r["ok"])
        self.assertIn("abc1234", fb.read_text(encoding="utf-8"))

    def test_without_an_app_repo_refuses_feedback_beside_the_scenarios_or_report(self):
        for bad in (self.scen / "eval-feedback.md", self.out / "eval-feedback.md"):
            with self.assertRaises(run_eval.Refused):
                self.run_eval(app_repo=None, feedback=bad, version="abc1234")

    def test_needs_a_version_from_somewhere(self):
        with self.assertRaises(run_eval.Refused):
            self.run_eval(app_repo=None, feedback=None)


if __name__ == "__main__":
    unittest.main()
