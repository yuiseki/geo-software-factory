#!/usr/bin/env python3
"""A stand-in for an external map service, for evaluation: serves local tiles and fixed answers, and fails on
purpose. Standard library only, local only.

    python3 twin.py --root fixtures/tiles [--routes routes.json] [--log requests.jsonl] [--port 8999]
                    [--delay-ms N] [--fail-every N --fail-status 503] [--rate-limit N --rate-window S]
                    [--empty-every N] [--truncate-every N]

- Files under --root, with HTTP Range (so a PMTiles archive works) and CORS for a page on another port.
- --routes: a JSON object from "path?query" to {"status": 200, "json": ...} or {"status": 200, "text": ...},
  matched exactly after decoding, for a geocoder or POI search with fixed answers, including "not found".
- Faults are by request count, not random, so a run can be repeated: every Nth request fails with a status, gets
  an empty body or half of its body; over N requests in a window gets 429 with Retry-After; every response is
  delayed. These make the edge-case scenarios of geo-software-eval (timeouts, 5xx, empty, broken, slow).
- --log writes one JSON line per request (path, status, fault), so a scenario can check what the app asked for.

It only binds to 127.0.0.1 by default. A twin is shaped after the real service's documents and responses; a pass
against it is not a pass against the real one (see references/twins.md).
"""
from __future__ import annotations

import argparse
import dataclasses
import http.server
import json
import re
import threading
import time
import urllib.parse
from collections import deque
from pathlib import Path

RANGE = re.compile(r"^bytes=(\d*)-(\d*)$")
TYPES = {".pbf": "application/x-protobuf", ".mvt": "application/vnd.mapbox-vector-tile", ".json": "application/json",
         ".geojson": "application/geo+json", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp",
         ".pmtiles": "application/octet-stream", ".html": "text/html; charset=utf-8"}


@dataclasses.dataclass
class Config:
    root: Path
    routes: dict = dataclasses.field(default_factory=dict)
    log: Path | None = None
    delay_ms: int = 0
    fail_every: int = 0
    fail_status: int = 503
    rate_limit: int = 0
    rate_window: float = 60.0
    empty_every: int = 0
    truncate_every: int = 0


def load_routes(path: Path) -> dict:
    return {urllib.parse.unquote(k): v for k, v in json.loads(path.read_text(encoding="utf-8")).items()}


def make_server(host: str, port: int, cfg: Config) -> http.server.ThreadingHTTPServer:
    lock = threading.Lock()
    state = {"n": 0, "times": deque()}
    root = cfg.root.resolve()

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            with lock:
                state["n"] += 1
                n = state["n"]
                now = time.monotonic()
                times = state["times"]
                while times and now - times[0] > cfg.rate_window:
                    times.popleft()
                times.append(now)
                over = cfg.rate_limit and len(times) > cfg.rate_limit
            if cfg.delay_ms:
                time.sleep(cfg.delay_ms / 1000)
            path = urllib.parse.unquote(self.path)
            if over:
                return self.reply(429, b"rate limited", "text/plain", "rate", {"Retry-After": str(int(cfg.rate_window))})
            if cfg.fail_every and n % cfg.fail_every == 0:
                return self.reply(cfg.fail_status, b"injected failure", "text/plain", "fail")
            status, body, ctype = self.resolve(path)
            fault, headers = None, {}
            if status == 200 and cfg.empty_every and n % cfg.empty_every == 0:
                body, fault = b"", "empty"
            elif status == 200 and cfg.truncate_every and n % cfg.truncate_every == 0:
                body, fault = body[: len(body) // 2], "truncate"
            elif status == 200 and (m := RANGE.match(self.headers.get("Range", ""))):
                size = len(body)
                a, b = m.groups()
                start, end = (int(a), min(int(b) if b else size - 1, size - 1)) if a else (max(size - int(b), 0), size - 1)
                if start > end or start >= size:
                    return self.reply(416, b"", ctype, None, {"Content-Range": f"bytes */{size}"})
                body, status = body[start:end + 1], 206
                headers["Content-Range"] = f"bytes {start}-{end}/{size}"
            self.reply(status, body, ctype, fault, headers)

        def resolve(self, path: str):
            if path in cfg.routes:
                r = cfg.routes[path]
                if "json" in r:
                    return r.get("status", 200), json.dumps(r["json"], ensure_ascii=False).encode(), "application/json"
                return r.get("status", 200), r.get("text", "").encode(), "text/plain; charset=utf-8"
            target = (root / path.split("?", 1)[0].lstrip("/")).resolve()
            if (target != root and root not in target.parents) or not target.is_file():
                return 404, b"not found", "text/plain"
            return 200, target.read_bytes(), TYPES.get(target.suffix, "application/octet-stream")

        def reply(self, status, body, ctype, fault, headers=None):
            # Log before answering, so a client that reads the log right after its response sees its request.
            if cfg.log is not None:
                with lock, cfg.log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({"path": urllib.parse.unquote(self.path), "status": status, "fault": fault},
                                       ensure_ascii=False) + "\n")
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Accept-Ranges", "bytes")
            for k, v in (headers or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

    return http.server.ThreadingHTTPServer((host, port), Handler)


def parse(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--routes", type=Path)
    ap.add_argument("--log", type=Path)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8999)
    for name in ("delay-ms", "fail-every", "rate-limit", "empty-every", "truncate-every"):
        ap.add_argument(f"--{name}", type=int, default=0)
    ap.add_argument("--fail-status", type=int, default=503)
    ap.add_argument("--rate-window", type=float, default=60.0)
    a = ap.parse_args(argv)
    cfg = Config(root=a.root, routes=load_routes(a.routes) if a.routes else {}, log=a.log, delay_ms=a.delay_ms,
                 fail_every=a.fail_every, fail_status=a.fail_status, rate_limit=a.rate_limit,
                 rate_window=a.rate_window, empty_every=a.empty_every, truncate_every=a.truncate_every)
    return cfg, a.host, a.port


def main(argv=None) -> int:
    cfg, host, port = parse(argv)
    server = make_server(host, port, cfg)
    print(json.dumps({"listening": f"http://{host}:{server.server_address[1]}"}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
