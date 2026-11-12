"""Tests for smoke.py against a local HTTP server. Run: python3 -m unittest discover -s .agents/skills/geo-software-deploy/scripts"""
import http.server
import pathlib
import sys
import threading
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import smoke  # noqa: E402

INDEX = b'<html><script src="/app.js"></script><p>&copy; OpenStreetMap contributors</p></html>'


class Site:
    """A tiny site whose behaviour each test sets: routes map a path to (status, headers, body)."""

    def __init__(self, routes, fallback=None, headers=None):
        site = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):  # noqa: N802
                status, extra, body = site.routes.get(self.path.split("?")[0], site.fallback or (404, {}, b"not found"))
                self.send_response(status)
                for k, v in {**(site.headers or {}), **extra}.items():
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *a):
                pass

        self.routes, self.fallback, self.headers = routes, fallback, headers
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def codes(report, level):
    return sorted({f["code"] for f in report[level]})


class Smoke(unittest.TestCase):
    def site(self, *a, **kw):
        s = Site(*a, **kw)
        self.addCleanup(s.close)
        return s

    def test_healthy_site(self):
        s = self.site({"/": (200, {"Content-Type": "text/html"}, INDEX), "/api/places": (200, {"Content-Type": "application/json"}, b"[]")})
        r = smoke.check(s.url, expects=[("/api/places", 200)], expect_text=[("/", "OpenStreetMap")])
        self.assertEqual(r["errors"], [])

    def test_wrong_status_is_an_error(self):
        s = self.site({"/": (200, {}, INDEX)})
        r = smoke.check(s.url, expects=[("/api/places", 200)])
        self.assertIn("status", codes(r, "errors"))

    def test_missing_text_is_an_error(self):
        s = self.site({"/": (200, {}, b"<html>map</html>")})
        self.assertIn("text", codes(smoke.check(s.url, expect_text=[("/", "OpenStreetMap")]), "errors"))

    def test_exposed_git_and_env_are_errors(self):
        s = self.site({"/": (200, {"Content-Type": "text/html"}, INDEX),
                       "/.git/HEAD": (200, {"Content-Type": "text/plain"}, b"ref: refs/heads/main\n"),
                       "/.env": (200, {"Content-Type": "text/plain"}, b"API_KEY=abc\n")})
        r = smoke.check(s.url)
        self.assertIn("exposed", codes(r, "errors"))
        self.assertEqual(sorted(e for f in r["errors"] if f["code"] == "exposed" for e in f["examples"]), ["/.env", "/.git/HEAD"])

    def test_spa_fallback_is_not_exposure(self):
        # Single-page apps answer every path with the index page and 200.
        s = self.site({}, fallback=(200, {"Content-Type": "text/html"}, INDEX))
        self.assertNotIn("exposed", codes(smoke.check(s.url), "errors"))

    def test_source_map_of_the_page_script_is_a_warning(self):
        s = self.site({"/": (200, {"Content-Type": "text/html"}, INDEX),
                       "/app.js": (200, {"Content-Type": "text/javascript"}, b"1"),
                       "/app.js.map": (200, {"Content-Type": "application/json"}, b'{"version":3}')})
        self.assertIn("source-map", codes(smoke.check(s.url), "warnings"))

    def test_missing_security_headers_are_warnings_on_https_only(self):
        s = self.site({"/": (200, {"Content-Type": "text/html"}, INDEX)})
        w = codes(smoke.check(s.url), "warnings")
        self.assertIn("csp", w)
        self.assertNotIn("hsts", w)  # plain http here

    def test_slow_response_is_an_error(self):
        s = self.site({"/": (200, {}, INDEX)})
        self.assertIn("slow", codes(smoke.check(s.url, max_ms=0), "errors"))

    def test_unreachable_is_an_error(self):
        self.assertIn("unreachable", codes(smoke.check("http://127.0.0.1:9", timeout=2), "errors"))


if __name__ == "__main__":
    unittest.main()
