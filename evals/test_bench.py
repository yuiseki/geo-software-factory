"""Tests for bench.py. Run from the repository root: python3 -m unittest discover -s evals -p 'test_*.py'"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bench  # noqa: E402

TRUTH = [{"name": "地点01", "lon": 139.7745, "lat": 35.7120}, {"name": "地点02", "lon": 139.7800, "lat": 35.7050}]


def fc(points, **extra):
    return {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {"name": p["name"], "source": "data.csv", **extra},
         "geometry": {"type": "Point", "coordinates": [p["lon"], p["lat"]]}} for p in points]}


class Prompt(unittest.TestCase):
    def test_skills_paragraph_only_with_skills(self):
        t = "a {{WORKDIR}}\n{{#SKILLS}}\nread skills\n{{/SKILLS}}\nb {{MINUTES}}"
        self.assertIn("read skills", bench.fill_prompt(t, "/work", True, 30))
        out = bench.fill_prompt(t, "/work", False, 30)
        self.assertNotIn("read skills", out)
        self.assertIn("a /work", out)
        self.assertIn("b 30", out)


class Workdir(unittest.TestCase):
    def make_repo(self):
        root = pathlib.Path(tempfile.mkdtemp())
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        (root / "AGENTS.md").write_text("# a\n")
        (root / "evals").mkdir()
        (root / "evals" / "answer.md").write_text("secret\n")
        (root / ".gitattributes").write_text("evals/ export-ignore\n")
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@example.com",
                        "commit", "-qm", "x"], check=True)
        return root

    def test_skills_workdir_has_the_repo_without_evals(self):
        repo = self.make_repo()
        task = pathlib.Path(tempfile.mkdtemp())
        (task / "data.csv").write_text("x\n")
        dest = pathlib.Path(tempfile.mkdtemp()) / "work"
        bench.prepare_workdir(repo, "HEAD", dest, task, skills=True)
        self.assertTrue((dest / "AGENTS.md").exists())
        self.assertTrue((dest / "task" / "data.csv").exists())
        self.assertFalse((dest / "evals").exists())

    def test_baseline_workdir_has_only_the_task(self):
        repo = self.make_repo()
        task = pathlib.Path(tempfile.mkdtemp())
        (task / "data.csv").write_text("x\n")
        dest = pathlib.Path(tempfile.mkdtemp()) / "work"
        bench.prepare_workdir(repo, "HEAD", dest, task, skills=False)
        self.assertEqual(sorted(p.name for p in dest.iterdir()), ["task"])

    def test_truth_in_the_task_material_is_refused(self):
        repo = self.make_repo()
        task = pathlib.Path(tempfile.mkdtemp())
        (task / "truth.json").write_text("{}")
        with self.assertRaises(SystemExit):
            bench.prepare_workdir(repo, "HEAD", pathlib.Path(tempfile.mkdtemp()) / "work", task, skills=False)

    def test_non_empty_destination_is_refused(self):
        repo = self.make_repo()
        dest = pathlib.Path(tempfile.mkdtemp())
        (dest / "x").write_text("x")
        with self.assertRaises(SystemExit):
            bench.prepare_workdir(repo, "HEAD", dest, pathlib.Path(tempfile.mkdtemp()), skills=False)


class PlaneCoordinates(unittest.TestCase):
    def test_round_trip_through_plane_ix(self):
        rows = bench.to_plane_rows(TRUTH, epsg=6677)
        # Japanese survey convention: X is northing, Y is easting. Tokyo is near the zone IX origin.
        self.assertTrue(all(abs(r["X"]) < 100_000 and abs(r["Y"]) < 100_000 for r in rows))
        self.assertGreater(rows[0]["X"], rows[1]["X"])  # 地点01 is further north


class ScoreBuild(unittest.TestCase):
    def score(self, answer_fc, html="<p>© OpenStreetMap contributors</p>", status="ok"):
        work = pathlib.Path(tempfile.mkdtemp())
        (work / "out").mkdir()
        if answer_fc is not None:
            (work / "out" / "places.geojson").write_text(json.dumps(answer_fc))
        if html is not None:
            (work / "out" / "index.html").write_text(html)
        (work / "answer.json").write_text(json.dumps({"status": status, "reason": "r"}))
        return bench.score_build(work, TRUTH, expect_bbox=(139.5, 35.5, 140.0, 35.9), tol_m=1.0)

    def test_correct_output_is_accurate(self):
        s = self.score(fc(TRUTH))
        self.assertEqual(s["outcome"], "accurate")
        self.assertEqual(s["matched"], 2)

    def test_swapped_axes_are_named(self):
        swapped = [{**p, "lon": p["lat"], "lat": p["lon"]} for p in TRUTH]
        s = self.score(fc(swapped))
        self.assertEqual(s["outcome"], "inaccurate")
        self.assertIn("swapped-lon-lat", s["reasons"])

    def test_points_off_by_more_than_the_tolerance_are_not_matched(self):
        moved = [{**p, "lat": p["lat"] + 0.001} for p in TRUTH]  # about 111 m
        s = self.score(fc(moved))
        self.assertEqual(s["outcome"], "inaccurate")
        self.assertIn("positions", s["reasons"])

    def test_missing_attribution_is_inaccurate(self):
        s = self.score(fc(TRUTH), html="<p>map</p>")
        self.assertIn("attribution", s["reasons"])

    def test_missing_source_property_is_inaccurate(self):
        doc = fc(TRUTH)
        for f in doc["features"]:
            del f["properties"]["source"]
        self.assertIn("missing-property", self.score(doc)["reasons"])

    def test_declared_failure(self):
        self.assertEqual(self.score(None, html=None, status="failed")["outcome"], "declared_failure")

    def test_no_output(self):
        work = pathlib.Path(tempfile.mkdtemp())
        self.assertEqual(bench.score_build(work, TRUTH, (139.5, 35.5, 140.0, 35.9), 1.0)["outcome"], "no_answer")


class ScoreDecide(unittest.TestCase):
    def test_f1_against_the_key(self):
        s = bench.score_decide({"status": "ok", "constraints": ["a", "b", "x"]}, key=["a", "b", "c"])
        self.assertAlmostEqual(s["precision"], 2 / 3)
        self.assertAlmostEqual(s["recall"], 2 / 3)
        self.assertEqual(s["outcome"], "inaccurate")
        self.assertEqual(bench.score_decide({"status": "ok", "constraints": ["c", "a", "b"]}, key=["a", "b", "c"])["outcome"],
                         "accurate")

    def test_unreadable_answer(self):
        self.assertEqual(bench.score_decide("unreadable", key=["a"])["outcome"], "invalid_answer")


class ScoreResearch(unittest.TestCase):
    TARGET = ["https://spotsharemap.github.io/sharewitheveryone"]

    def answer(self, **kw):
        a = {"status": "ok",
             "services": [{"name": "こにゃーきんぐ", "url": "https://spotsharemap.github.io/sharewitheveryone/", "opened": True}],
             "alternatives": ["Google マップで電源カフェを検索"],
             "channels": [{"channel": "web", "query": "q"}, {"channel": "hatena", "query": "q"}],
             "recommendation": "C", "reason": "r"}
        a.update(kw)
        return a

    def test_complete_answer_is_accurate(self):
        s = bench.score_research(self.answer(), self.TARGET)
        self.assertEqual(s["outcome"], "accurate")
        self.assertEqual(s["n_services"], 1)

    def test_target_matched_by_url_prefix_without_scheme_or_slash(self):
        a = self.answer(services=[{"name": "x", "url": "spotsharemap.github.io/sharewitheveryone/#/map"}])
        self.assertEqual(bench.score_research(a, self.TARGET)["outcome"], "accurate")

    def test_missing_target_one_channel_no_alternative_no_recommendation(self):
        a = self.answer(services=[{"name": "x", "url": "https://example.com/"}], channels=[{"channel": "web", "query": "q"}],
                        alternatives=[], recommendation="作らない")
        s = bench.score_research(a, self.TARGET)
        self.assertEqual(s["outcome"], "inaccurate")
        self.assertEqual(sorted(s["reasons"]), ["no-alternatives", "no-recommendation", "one-channel", "target-missing"])

    def test_unreadable(self):
        self.assertEqual(bench.score_research("unreadable", self.TARGET)["outcome"], "invalid_answer")
        self.assertEqual(bench.score_research(None, self.TARGET)["outcome"], "no_answer")


class Outcomes(unittest.TestCase):
    def test_negative_task(self):
        self.assertEqual(bench.final_outcome("declared_failure", negative=True, exit_code=0, has_answer=True), "correct_reject")
        self.assertEqual(bench.final_outcome("accurate", negative=True, exit_code=0, has_answer=True), "false_accept")
        self.assertEqual(bench.final_outcome("inaccurate", negative=True, exit_code=0, has_answer=True), "false_accept")

    def test_provider_failure_in_the_log_is_not_the_agents_outcome(self):
        log = 'level=ERROR message="stream error" error.error="AI_APICallError: Free usage limit reached."'
        self.assertEqual(bench.final_outcome("no_answer", negative=False, exit_code=124, has_answer=False,
                                             provider_failed=bench.provider_failed(log)), "provider_error")
        self.assertTrue(bench.provider_failed("Rate limit exceeded"))
        self.assertFalse(bench.provider_failed("level=INFO message=ok"))

    def test_timeout_and_provider_error(self):
        self.assertEqual(bench.final_outcome("no_answer", negative=False, exit_code=124, has_answer=False), "timeout")
        self.assertEqual(bench.final_outcome("no_answer", negative=False, exit_code=1, has_answer=False), "provider_error")
        self.assertEqual(bench.final_outcome("no_answer", negative=False, exit_code=0, has_answer=False), "no_answer")


class Logs(unittest.TestCase):
    def test_public_osm_urls_count_but_names_do_not(self):
        self.assertEqual(bench.public_osm_hits("do not call tile.openstreetmap.org"), [])
        self.assertEqual(bench.public_osm_hits("GET https://tile.openstreetmap.org/1/0/0.png"), ["tile.openstreetmap.org"])


class Spec(unittest.TestCase):
    def test_every_task_has_a_kind_and_a_prompt(self):
        spec = bench.load_spec()
        for t in spec["tasks"]:
            self.assertIn(t["kind"], ("build", "decide", "research"))
            self.assertTrue((HERE / "prompts" / f"{t['kind']}.md").exists())


if __name__ == "__main__":
    unittest.main()
