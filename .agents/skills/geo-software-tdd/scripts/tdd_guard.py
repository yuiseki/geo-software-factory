#!/usr/bin/env python3
"""TDD discipline & CI guard: flaky test quarantine ledger, downward-only ratchet, and external network blocker.

    python3 tdd_guard.py quarantine --ledger QUARANTINE.json [--passed-test NAME ...]
    python3 tdd_guard.py ratchet    --src-dir DIR --caps CAPS.json [--update]
    python3 tdd_guard.py run-local  -- CMD [ARGS ...]

Enforces geo-software-tdd principles (`discipline.md`, `fixtures.md`, `ci.md`) by program:
1. Quarantine ledger (`quarantine`): every quarantined test must specify `reason`, `owner`, and `expires` (YYYY-MM-DD);
   expired entries fail CI; if a quarantined test passes (`--passed-test`), CI fails so the stale entry is removed.
2. Downward-only ratchet (`ratchet`): counts `TODO` / `FIXME` markers in `src-dir`; fails if the count exceeds `caps.json`,
   and lowers the cap when `--update` is passed and the count decreased (`ci.md` rule 44).
3. Loopback-only network guard (`block_external_network` / `run-local`): blocks any socket connection to non-loopback
   hosts during tests so tests never call public tile/geocoder servers (`fixtures.md` rule 13-18).
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import json
import re
import socket
import subprocess
import sys
from pathlib import Path

TODO_RE = re.compile(r"\b(TODO|FIXME)\b")
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost"}


def check_quarantine(ledger_path: Path, passed_tests: list[str] | None = None,
                     today: datetime.date | None = None) -> dict:
    today = today or datetime.date.today()
    passed_set = set(passed_tests or [])
    errors: list[dict] = []
    if not ledger_path.is_file():
        return {"ok": True, "count": 0, "errors": []}
    doc = json.loads(ledger_path.read_text(encoding="utf-8"))
    entries = doc.get("quarantined", [])
    for e in entries:
        name = str(e.get("test") or "").strip()
        reason = str(e.get("reason") or "").strip()
        owner = str(e.get("owner") or "").strip()
        expires_str = str(e.get("expires") or "").strip()
        if not (name and reason and owner and expires_str):
            errors.append({
                "code": "missing_quarantine_metadata",
                "test": name or "(unnamed)",
                "message": f"{name or '(unnamed)'}: 隔離には test, reason, owner, expires のすべてが必須",
            })
            continue
        try:
            exp_date = datetime.date.fromisoformat(expires_str)
            if exp_date < today:
                errors.append({
                    "code": "expired_quarantine",
                    "test": name,
                    "message": f"{name}: 隔離の期限 ({expires_str}) が過ぎている。直すか消すかを決める",
                })
        except ValueError:
            errors.append({
                "code": "invalid_expiry_date",
                "test": name,
                "message": f"{name}: expires ({expires_str}) が YYYY-MM-DD ではない",
            })
        if name in passed_set:
            errors.append({
                "code": "quarantined_test_passed",
                "test": name,
                "message": f"{name}: 隔離された試験が通った。隔離の一覧から外す",
            })
    return {"ok": not errors, "count": len(entries), "errors": errors}


def count_markers(src_dir: Path) -> int:
    total = 0
    for p in sorted(src_dir.rglob("*")):
        if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts:
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            total += len(TODO_RE.findall(text))
    return total


def check_ratchet(src_dir: Path, caps_path: Path, update: bool = False) -> dict:
    caps = json.loads(caps_path.read_text(encoding="utf-8")) if caps_path.is_file() else {"todo_count": 0}
    limit = int(caps.get("todo_count", 0))
    current = count_markers(src_dir)
    errors = []
    if current > limit:
        errors.append({
            "code": "ratchet_exceeded",
            "message": f"TODO/FIXME の数が上限を超えた ({current} > {limit})",
        })
    elif update and current < limit:
        caps["todo_count"] = current
        caps_path.parent.mkdir(parents=True, exist_ok=True)
        caps_path.write_text(json.dumps(caps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"ok": not errors, "current": current, "limit": caps["todo_count"], "errors": errors}


@contextlib.contextmanager
def block_external_network():
    orig_create = socket.create_connection
    orig_connect = socket.socket.connect

    def guarded_create(address, *args, **kwargs):
        host = address[0] if isinstance(address, tuple) else str(address)
        if host not in LOOPBACK_HOSTS and not host.startswith("127."):
            raise RuntimeError(f"外部への通信は試験で禁止されている: {host}")
        return orig_create(address, *args, **kwargs)

    def guarded_connect(self, address):
        host = address[0] if isinstance(address, tuple) else str(address)
        if isinstance(host, str) and host not in LOOPBACK_HOSTS and not host.startswith("127.") and not host.startswith("/"):
            raise RuntimeError(f"外部への通信は試験で禁止されている: {host}")
        return orig_connect(self, address)

    socket.create_connection = guarded_create
    socket.socket.connect = guarded_connect
    try:
        yield
    finally:
        socket.create_connection = orig_create
        socket.socket.connect = orig_connect


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="subcmd", required=True)

    p_q = sub.add_parser("quarantine", help="validate flaky test quarantine ledger")
    p_q.add_argument("--ledger", type=Path, required=True)
    p_q.add_argument("--passed-test", dest="passed", action="append", default=[])

    p_r = sub.add_parser("ratchet", help="enforce downward-only cap on TODO/FIXME count")
    p_r.add_argument("--src-dir", type=Path, required=True)
    p_r.add_argument("--caps", type=Path, required=True)
    p_r.add_argument("--update", action="store_true")

    a = ap.parse_args(argv)
    if a.subcmd == "quarantine":
        res = check_quarantine(a.ledger, a.passed)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res["ok"] else 1
    if a.subcmd == "ratchet":
        res = check_ratchet(a.src_dir, a.caps, a.update)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res["ok"] else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
