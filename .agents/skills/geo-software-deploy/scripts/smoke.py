#!/usr/bin/env python3
"""Read-only checks of a deployed map product, run right after each deploy.

Only GET, only to the given origin (redirects to another origin are not followed), a handful of requests. It is
not a load test and must not be pointed at anything but your own service.

    python3 smoke.py https://example.com [--expect /api/places=200] [--expect-text /=OpenStreetMap]
                                         [--max-ms 3000] [--timeout 10]

Errors: unreachable, wrong status, missing text, a slow response, files that must not be public (.git, .env)
served as themselves. Warnings: missing security headers (HSTS on https, CSP, nosniff) and a source map for a
script of the page. Prints a JSON report. Exit 0: no errors. Exit 1: errors.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Paths that must never be served as themselves, with how to recognise the real file.
FORBIDDEN = {
    "/.git/HEAD": re.compile(rb"^ref: refs/"),
    "/.git/config": re.compile(rb"\[core\]"),
    "/.env": re.compile(rb"^[A-Z][A-Z0-9_]*=", re.M),
    "/.env.local": re.compile(rb"^[A-Z][A-Z0-9_]*=", re.M),
    "/.dev.vars": re.compile(rb"^[A-Z][A-Z0-9_]*=", re.M),
}
SCRIPT_SRC = re.compile(rb"<script[^>]+src=[\"']([^\"']+\.js)[\"']", re.I)


class SameOrigin(urllib.request.HTTPRedirectHandler):
    def __init__(self, origin: str):
        self.origin = origin

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlsplit(newurl)[:2] != urllib.parse.urlsplit(self.origin)[:2]:
            return None  # do not leave our own service
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(opener, url: str, timeout: float):
    t0 = time.monotonic()
    try:
        with opener.open(urllib.request.Request(url, headers={"User-Agent": "geo-software-smoke"}), timeout=timeout) as r:
            body = r.read(1_000_000)
            return r.status, {k.lower(): v for k, v in r.headers.items()}, body, (time.monotonic() - t0) * 1000
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, e.read(1_000_000), (time.monotonic() - t0) * 1000
    except (urllib.error.URLError, OSError) as e:
        return None, {}, str(e).encode(), (time.monotonic() - t0) * 1000


def check(base: str, expects=(), expect_text=(), max_ms: float = 3000, timeout: float = 10) -> dict:
    base = base.rstrip("/")
    opener = urllib.request.build_opener(SameOrigin(base))
    found: dict[tuple[str, str], dict] = {}
    timings = {}

    def add(level, code, message, where=None):
        f = found.setdefault((level, code), {"code": code, "message": message, "examples": []})
        if where is not None and len(f["examples"]) < 10:
            f["examples"].append(where)

    cache = {}

    def get(path):
        if path not in cache:
            cache[path] = fetch(opener, base + path, timeout)
            timings[path] = round(cache[path][3])
        return cache[path]

    status, headers, root_body, ms = get("/")
    if status is None:
        add("errors", "unreachable", f"{base} did not answer: {root_body.decode(errors='replace')[:200]}")
        return {"base": base, "errors": [f for (lv, _), f in found.items() if lv == "errors"], "warnings": [], "ms": timings}

    for path, want in expects:
        st = get(path)[0]
        if st != want:
            add("errors", "status", "A path answered with an unexpected status.", f"{path}: {st}, expected {want}")
    for path, text in expect_text:
        if text.encode() not in get(path)[2]:
            add("errors", "text", "Expected text is missing (attribution, a heading, a marker).", f"{path}: {text!r}")
    for path, pattern in FORBIDDEN.items():
        st, hd, body, _ = get(path)
        is_html = "html" in hd.get("content-type", "") or body.lstrip()[:1] == b"<"
        if st == 200 and body != root_body and not is_html and pattern.search(body):
            add("errors", "exposed", "A file that must not be public is served.", path)

    for m in SCRIPT_SRC.findall(root_body)[:5]:
        src = urllib.parse.urljoin(base + "/", m.decode(errors="replace"))
        if urllib.parse.urlsplit(src)[:2] != urllib.parse.urlsplit(base)[:2]:
            continue
        path = urllib.parse.urlsplit(src).path + ".map"
        st, hd, body, _ = get(path)
        if st == 200 and body.lstrip()[:1] == b"{" and b'"version"' in body:
            add("warnings", "source-map", "A source map of the page's script is public; decide whether that is intended.", path)

    if base.startswith("https://") and "strict-transport-security" not in headers:
        add("warnings", "hsts", "No Strict-Transport-Security header on the page.")
    if "content-security-policy" not in headers:
        add("warnings", "csp", "No Content-Security-Policy header on the page.")
    if headers.get("x-content-type-options", "").lower() != "nosniff":
        add("warnings", "nosniff", "No X-Content-Type-Options: nosniff on the page.")
    for path, t in timings.items():
        if t > max_ms and path in ("/",) + tuple(p for p, _ in expects) + tuple(p for p, _ in expect_text):
            add("errors", "slow", f"Slower than {max_ms} ms.", f"{path}: {t} ms")

    return {"base": base, "ms": timings,
            "errors": [f for (lv, _), f in found.items() if lv == "errors"],
            "warnings": [f for (lv, _), f in found.items() if lv == "warnings"]}


def pair(s: str):
    path, _, value = s.partition("=")
    if not path.startswith("/") or not value:
        raise argparse.ArgumentTypeError(f"expected /path=value, got {s!r}")
    return path, value


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base")
    ap.add_argument("--expect", type=pair, action="append", default=[], help="/path=STATUS")
    ap.add_argument("--expect-text", type=pair, action="append", default=[], help="/path=TEXT")
    ap.add_argument("--max-ms", type=float, default=3000)
    ap.add_argument("--timeout", type=float, default=10)
    a = ap.parse_args(argv)
    report = check(a.base, [(p, int(v)) for p, v in a.expect], a.expect_text, a.max_ms, a.timeout)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
