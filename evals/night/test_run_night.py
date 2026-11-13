import json
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
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

    def test_agent_setup_supports_all_five_providers(self):
        (self.root / "codex-home").mkdir()
        with unittest.mock.patch.dict("os.environ", {"EVAL_CODEX_HOME": str(self.root / "codex-src")}):
            (self.root / "codex-src").mkdir()
            (self.root / "codex-src" / "auth.json").write_text("{}", encoding="utf-8")
            img, cmd, mdir, mtgt, env, sec = run_night.agent_setup("codex", self.root, 30, "gpt-6-luna", "medium")
            self.assertEqual(img, "geo-software-factory-evals-codex")
            self.assertIn("codex exec", cmd[-1])
        with unittest.mock.patch.dict("os.environ", {"GEMINI_API_KEY": "k1", "EVAL_GEMINI_HOME": str(self.root / "no-g")}):
            img, cmd, mdir, mtgt, env, sec = run_night.agent_setup("gemini", self.root, 30, "gemini-3.8-flash-low", "medium")
            self.assertEqual(img, "geo-software-factory-evals-gemini")
            self.assertEqual(env.get("GEMINI_API_KEY"), "k1")
            self.assertIn("agy", cmd[-1])
        with unittest.mock.patch.dict("os.environ", {"EVAL_CLAUDE_HOME": str(self.root / "claude-src")}):
            (self.root / "claude-src").mkdir()
            (self.root / "claude-src" / "oauth_token").write_text("tok1", encoding="utf-8")
            img, cmd, mdir, mtgt, env, sec = run_night.agent_setup("claude", self.root, 30, "claude-sonnet-5-5", "medium")
            self.assertEqual(img, "geo-software-factory-evals-claude")
            self.assertEqual(env.get("CLAUDE_CODE_OAUTH_TOKEN"), "tok1")
            self.assertIn("claude -p", cmd[-1])
        img, cmd, mdir, mtgt, env, sec = run_night.agent_setup("opencode", self.root, 30, "opencode/mimo", "medium")
        self.assertEqual(img, "geo-software-factory-evals-opencode")
        self.assertIn("opencode run", cmd[-1])
        with unittest.mock.patch.dict("os.environ", {"EVAL_QODER_HOME": str(self.root / "qoder-src")}):
            (self.root / "qoder-src").mkdir()
            (self.root / "qoder-src" / "pat").write_text("pat1", encoding="utf-8")
            img, cmd, mdir, mtgt, env, sec = run_night.agent_setup("qoder", self.root, 30, "Auto", "medium")
            self.assertEqual(img, "geo-software-factory-evals-qoder")
            self.assertEqual(env.get("QODER_PERSONAL_ACCESS_TOKEN"), "pat1")
            self.assertIn("qodercli -p", cmd[-1])


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

    def test_write_morning_reports_creates_eval_and_morning_markdown(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for sub in ("app", "scenarios", "out", "feedback", "handoff"):
                (root / sub).mkdir()
            (root / "app" / "product-brief.md").write_text(
                "# プロダクト概要: 台東区の名所マップ\n\n## 夜に決めたこと\n\n- MapLibre を採用した\n\n## 止まったこと\n\n- なし\n",
                encoding="utf-8",
            )
            (root / "out" / "final.json").write_text(json.dumps({
                "when": "2026-11-13T01:20:00+00:00",
                "base": "http://implementer:8787",
                "version": "def5678",
                "ok": True,
                "satisfaction": 1.0,
                "split_scenarios": [],
                "low_confidence_scenarios": [],
                "scenarios": [{
                    "id": "S1", "name": "名所表示", "symptom": "名所が出ない", "result": "pass",
                    "checks": [{"ok": True, "observed": {"kind": "http", "path": "/", "status": 200}}],
                }],
            }, ensure_ascii=False), encoding="utf-8")
            summary = {"final_version": "def5678", "commits_after_day": 2, "left_dirty": False,
                       "deploy_ready": True, "minutes": 12.5}
            paths = run_night.write_reports(root, summary)
            self.assertTrue(Path(paths["eval_report"]).is_file())
            self.assertTrue(Path(paths["morning_report"]).is_file())
            self.assertIn("MapLibre を採用した", Path(paths["morning_report"]).read_text(encoding="utf-8"))


class TokyoEvacuationTaskTest(unittest.TestCase):
    def test_task_paths_and_prepare_app_for_tokyo_evacuation(self):
        tdir, sdir = run_night.task_paths("tokyo-evacuation")
        self.assertTrue((tdir / "product-brief.md").is_file())
        self.assertTrue((sdir / "S3-spatial-filter.json").is_file())
        with tempfile.TemporaryDirectory() as d:
            app = Path(d) / "app"
            run_night.prepare_app(app, "baseline", task_dir=tdir)
            self.assertTrue((app / "data" / "shelters.csv").is_file())
            self.assertTrue((app / "data" / "hazard_zones.geojson").is_file())

    def test_eval_of_eval_on_tokyo_evacuation_reference(self):
        import os
        import time
        tdir, sdir = run_night.task_paths("tokyo-evacuation")
        serve = tdir.parent / "reference" / "serve.py"
        procs = []
        urls = {}
        try:
            for brk in ("none", "osm", "swap", "bbox", "nearest", "guard"):
                port = run_night.dark_factory.free_port()
                p = subprocess.Popen([sys.executable, str(serve)],
                                     env={**os.environ, "PORT": str(port), "REF_BREAK": brk})
                procs.append(p)
                urls[brk] = f"http://127.0.0.1:{port}"
            time.sleep(0.4)
            with tempfile.TemporaryDirectory() as d:
                rep = run_night.dark_factory.eval_of_eval(
                    sdir, urls["none"], {k: v for k, v in urls.items() if k != "none"}, Path(d) / "eoe.json"
                )
                self.assertTrue(rep["ok"], rep)
                self.assertEqual(rep["breaks"]["osm"]["failed_scenarios"], ["S1"])
                self.assertEqual(rep["breaks"]["bbox"]["failed_scenarios"], ["S3"])
                self.assertEqual(rep["breaks"]["nearest"]["failed_scenarios"], ["S4"])
                self.assertEqual(rep["breaks"]["guard"]["failed_scenarios"], ["S5"])
        finally:
            for p in procs:
                p.terminate()
                p.wait(timeout=3)


if __name__ == "__main__":
    unittest.main()
