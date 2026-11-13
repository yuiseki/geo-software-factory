import http.server
import json
import sys
import tempfile
import threading
import unittest
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import audit_probe  # noqa: E402


class VulnerableHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/.env":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"SECRET_KEY=leaked\n")
            return
        if parsed.path == "/api/places":
            q = qs.get("q", [""])[0]
            bbox = qs.get("bbox", [""])[0]
            # Vulnerable: accepts 10,000-char query and world bbox with 200 OK and returns unescaped XSS
            if "<img" in q:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"<html>{q}</html>".encode("utf-8"))
                return
            if len(q) > 2000 or bbox == "-180,-90,180,90":
                self.send_response(200)
                self.end_headers()
                features = [{"type": "Feature", "properties": {"id": i}, "geometry": {"type": "Point", "coordinates": [139.7, 35.7]}} for i in range(1500)]
                self.wfile.write(json.dumps({"type": "FeatureCollection", "features": features}).encode("utf-8"))
                return
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"type":"FeatureCollection","features":[]}')
            return
        self.send_response(404)
        self.end_headers()


class DefendedHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if parsed.path in ("/.env", "/.git/HEAD"):
            self.send_response(404)
            self.end_headers()
            return
        if parsed.path == "/api/places":
            q = qs.get("q", [""])[0]
            bbox = qs.get("bbox", [""])[0]
            if len(q) > 500 or bbox in ("-180,-90,180,90", "180,90,-180,-90"):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"bad request"}')
                return
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"type":"FeatureCollection","features":[]}')
            return
        self.send_response(404)
        self.end_headers()


class AuditProbeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_detects_vulnerabilities_and_generates_eval_scenarios(self):
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), VulnerableHandler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{srv.server_address[1]}"
            scen_out = self.root / "scenarios"
            rep = audit_probe.probe(base=base, search_path="/api/places", scenarios_out=scen_out)
            self.assertFalse(rep["ok"])
            statuses = {f["id"]: f["status"] for f in rep["findings"]}
            self.assertEqual(statuses["EXPOSURE-ENV"], "問題あり")
            self.assertEqual(statuses["ABUSE-HUGE-QUERY"], "問題あり")
            self.assertEqual(statuses["ABUSE-WORLD-BBOX"], "問題あり")
            self.assertEqual(statuses["INJECTION-XSS-REFLECT"], "問題あり")
            # Confirmed issues are converted to geo-software-eval scenario JSON files
            generated = list(scen_out.glob("AUDIT-*.json"))
            self.assertGreaterEqual(len(generated), 3)
            sample = json.loads(generated[0].read_text(encoding="utf-8"))
            self.assertIn("symptom", sample)
            self.assertIn("checks", sample)
        finally:
            srv.shutdown()
            srv.server_close()

    def test_marks_defended_with_observation_when_server_rejects_bad_inputs(self):
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), DefendedHandler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{srv.server_address[1]}"
            rep = audit_probe.probe(base=base, search_path="/api/places")
            self.assertTrue(rep["ok"], rep)
            for f in rep["findings"]:
                self.assertEqual(f["status"], "防御されている")
                self.assertTrue(f["observed"])  # Rule: 観測の無い「防御されている」は付けない
        finally:
            srv.shutdown()
            srv.server_close()

    def test_enforces_triage_rule_downgrading_unobserved_defended_to_unverified(self):
        raw = [
            {"id": "X1", "status": "防御されている", "observed": "", "title": "コード上は大丈夫そう"},
            {"id": "X2", "status": "防御されている", "observed": "status=400 (12ms)", "title": "実測済み"},
        ]
        cleaned = audit_probe.enforce_observation_rule(raw)
        self.assertEqual(cleaned[0]["status"], "未確認")
        self.assertEqual(cleaned[1]["status"], "防御されている")


if __name__ == "__main__":
    unittest.main()
