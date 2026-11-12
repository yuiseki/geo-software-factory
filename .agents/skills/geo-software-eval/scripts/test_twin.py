import json
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import twin  # noqa: E402


def get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        with e:
            return e.code, dict(e.headers), e.read()


class Base(unittest.TestCase):
    faults: dict = {}

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "tiles" / "14").mkdir(parents=True)
        (root / "tiles" / "14" / "a.pbf").write_bytes(bytes(range(256)) * 4)
        routes = root / "routes.json"
        routes.write_text(json.dumps({"/geocode?q=上野駅": {"status": 200, "json": [{"lon": 139.777, "lat": 35.713}]},
                                      "/geocode?q=存在しない": {"status": 200, "json": []}}, ensure_ascii=False),
                          encoding="utf-8")
        self.log = root / "requests.jsonl"
        cfg = twin.Config(root=root / "tiles", routes=twin.load_routes(routes), log=self.log, **self.faults)
        self.server = twin.make_server("127.0.0.1", 0, cfg)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.tmp.cleanup()

    def requests(self):
        return [json.loads(x) for x in self.log.read_text(encoding="utf-8").splitlines()]


class ServeTest(Base):
    def test_serves_files_with_cors(self):
        status, headers, body = get(self.base + "/14/a.pbf")
        self.assertEqual((status, len(body)), (200, 1024))
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), "*")

    def test_range_request_for_pmtiles(self):
        status, headers, body = get(self.base + "/14/a.pbf", {"Range": "bytes=10-19"})
        self.assertEqual(status, 206)
        self.assertEqual(body, bytes(range(10, 20)))
        self.assertEqual(headers["Content-Range"], "bytes 10-19/1024")

    def test_missing_file_is_404_and_no_escape_from_root(self):
        self.assertEqual(get(self.base + "/14/none.pbf")[0], 404)
        self.assertEqual(get(self.base + "/../routes.json")[0], 404)
        self.assertEqual(get(self.base + "/%2e%2e/routes.json")[0], 404)

    def test_fixed_routes_answer_like_a_geocoder(self):
        q = urllib.parse.quote("上野駅")
        status, headers, body = get(self.base + f"/geocode?q={q}")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)[0]["lon"], 139.777)
        q = urllib.parse.quote("存在しない")
        self.assertEqual(json.loads(get(self.base + f"/geocode?q={q}")[2]), [])

    def test_every_request_is_logged(self):
        get(self.base + "/14/a.pbf")
        get(self.base + "/14/none.pbf")
        self.assertEqual([(r["path"], r["status"]) for r in self.requests()], [("/14/a.pbf", 200), ("/14/none.pbf", 404)])


class FailEveryTest(Base):
    faults = {"fail_every": 3, "fail_status": 503}

    def test_every_third_request_fails(self):
        self.assertEqual([get(self.base + "/14/a.pbf")[0] for _ in range(6)], [200, 200, 503, 200, 200, 503])


class RateTest(Base):
    faults = {"rate_limit": 2, "rate_window": 60.0}

    def test_over_the_limit_is_429_with_retry_after(self):
        codes = [get(self.base + "/14/a.pbf") for _ in range(3)]
        self.assertEqual([c[0] for c in codes], [200, 200, 429])
        self.assertIn("Retry-After", codes[2][1])


class BrokenBodyTest(Base):
    faults = {"empty_every": 2, "truncate_every": 3}

    def test_empty_and_truncated_bodies(self):
        lengths = [len(get(self.base + "/14/a.pbf")[2]) for _ in range(3)]
        self.assertEqual(lengths, [1024, 0, 512])


class DelayTest(Base):
    faults = {"delay_ms": 200}

    def test_responses_are_delayed(self):
        t0 = time.monotonic()
        get(self.base + "/14/a.pbf")
        self.assertGreaterEqual(time.monotonic() - t0, 0.19)


class CliTest(unittest.TestCase):
    def test_parse_args(self):
        cfg, host, port = twin.parse(["--root", ".", "--fail-every", "5", "--delay-ms", "50"])
        self.assertEqual((cfg.fail_every, cfg.delay_ms, host, port), (5, 50, "127.0.0.1", 8999))


if __name__ == "__main__":
    unittest.main()
