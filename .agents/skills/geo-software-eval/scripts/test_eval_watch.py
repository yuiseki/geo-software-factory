import http.server
import json
import sys
import tempfile
import threading
import unittest
from functools import partial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import eval_watch  # noqa: E402


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class WatchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.site, self.handoff, self.scen, self.out, self.fbdir = (root / n for n in
                                                                    ("site", "handoff", "scen", "out", "feedback"))
        for d in (self.site, self.handoff, self.scen, self.out, self.fbdir):
            d.mkdir()
        (self.site / "index.html").write_text("<html>OpenStreetMap</html>", encoding="utf-8")
        (self.scen / "S1.json").write_text(json.dumps(
            {"id": "S1", "symptom": "帰属表示が無い", "checks": [{"kind": "http", "path": "/", "contains": "OpenStreetMap"}]},
            ensure_ascii=False), encoding="utf-8")
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=str(self.site)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.port = self.server.server_address[1]
        self.fb = self.fbdir / "eval-feedback.md"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def request(self, **body):
        (self.handoff / "ready.json").write_text(json.dumps(body), encoding="utf-8")

    def once(self):
        return eval_watch.once(handoff=self.handoff, scenarios=self.scen, report_dir=self.out, feedback=self.fb,
                               app_host="127.0.0.1")

    def test_no_request_does_nothing(self):
        self.assertIsNone(self.once())
        self.assertFalse(self.fb.exists())

    def test_a_request_is_judged_once(self):
        self.request(rev="abc1234", port=self.port)
        r = self.once()
        self.assertTrue(r["ok"])
        self.assertIn("abc1234", self.fb.read_text(encoding="utf-8"))
        self.assertEqual(len(list(self.out.glob("*-abc1234.json"))), 1)
        self.assertIsNone(self.once())  # the same request is not judged again

    def test_a_new_request_is_judged_again(self):
        self.request(rev="abc1234", port=self.port)
        self.once()
        self.request(rev="def5678", port=self.port)
        self.assertEqual(self.once()["version"], "def5678")

    def test_the_same_version_can_be_asked_again_with_a_nonce(self):
        self.request(rev="abc1234", port=self.port)
        self.once()
        self.request(rev="abc1234", port=self.port, nonce=2)
        self.assertIsNotNone(self.once())

    def test_the_implementer_cannot_choose_the_host(self):
        self.request(rev="abc1234", port=self.port, base="http://example.com")
        r = self.once()
        self.assertEqual(r["base"], f"http://127.0.0.1:{self.port}")

    def test_a_malformed_request_is_answered_in_the_feedback(self):
        for bad in ({"rev": "abc1234; rm -rf /", "port": self.port}, {"rev": "abc1234", "port": "80/../x"},
                    {"rev": "abc1234", "port": 70000}):
            (self.handoff / "ready.json").write_text(json.dumps(bad), encoding="utf-8")
            self.assertEqual(self.once(), {"refused": True})
            self.assertIn("依頼の形", self.fb.read_text(encoding="utf-8"))
        (self.handoff / "ready.json").write_text("{not json", encoding="utf-8")
        self.assertEqual(self.once(), {"refused": True})

    def test_feedback_beside_the_scenarios_is_refused(self):
        self.request(rev="abc1234", port=self.port)
        with self.assertRaises(eval_watch.run_eval.Refused):
            eval_watch.once(handoff=self.handoff, scenarios=self.scen, report_dir=self.out,
                            feedback=self.scen / "eval-feedback.md", app_host="127.0.0.1")


if __name__ == "__main__":
    unittest.main()
