#!/usr/bin/env python3
"""Prove, by trying, that the implementer's container cannot see the scenarios or the reports.

    APP_DIR=... HANDOFF_DIR=... FEEDBACK_DIR=... SCENARIOS_DIR=... REPORT_DIR=... EVAL_SCRIPTS=... \
    python3 check_isolation.py [--compose ../assets/isolation/compose.yaml]

Run it with the same environment as the night's `docker compose up`, before the night. It writes a fresh random
canary into the scenarios and report directories, then, through the same compose file:

- implementer: searches its whole file system (and environment) for the canary: must find nothing
- evaluator: the same search over /eval: must find it (the control; without it "not found" proves nothing)
- implementer: cannot write the feedback, can write the handoff, has no Docker socket
- evaluator: cannot write the scenarios

The canaries are removed afterwards. A configuration error (a directory missing, or the scenarios or reports
inside the app directory) is reported before any container starts.

Prints a JSON report. Exit 0: isolated. Exit 1: not isolated. Exit 2: misconfigured.
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import shlex
import subprocess
import sys
from pathlib import Path

CANARY = ".isolation-canary"
# Printed first inside the container. Several probes expect a command to fail ("cannot write"), so a container
# that never started would pass them; a probe counts only when this marker shows it ran.
RAN = "ISOLATION-PROBE-RAN"
DIRS = ("APP_DIR", "HANDOFF_DIR", "FEEDBACK_DIR", "SCENARIOS_DIR", "REPORT_DIR", "EVAL_SCRIPTS")
COMPOSE = Path(__file__).parent.parent / "assets" / "isolation" / "compose.yaml"


class Misconfigured(Exception):
    pass


def inside(path: Path, root: Path) -> bool:
    path, root = path.resolve(), root.resolve()
    return path == root or root in path.parents


def docker_runner(compose, env: dict):
    """compose: one file or a list (the night's file plus overrides, exactly as the night will use them)."""
    files = [compose] if isinstance(compose, (str, Path)) else list(compose)
    flags = [x for f in files for x in ("-f", str(f))]

    def run(service: str, script: str):
        p = subprocess.run(["docker", "compose", *flags, "run", "--rm", "--no-deps", "-T",
                            "--entrypoint", "sh", service, "-c", script],
                           env={**os.environ, **env}, capture_output=True, text=True, timeout=600)
        return p.returncode, (p.stdout + p.stderr)

    def cleanup():
        # `run` creates the project's network; leave the host as it was (address pools are finite).
        subprocess.run(["docker", "compose", *flags, "down", "--remove-orphans", "-t", "1"],
                       env={**os.environ, **env}, capture_output=True, timeout=120)

    run.cleanup = cleanup
    return run


def search(token: str, root: str) -> str:
    # The token reaches the container only in this command line; /proc (where the command line lives) is skipped.
    t = shlex.quote(token)
    return (f"grep -rIlsF {t} {root} --exclude-dir=proc --exclude-dir=sys --exclude-dir=dev; "
            f"env | grep -qF {t} && echo ENV")


def check(env: dict, runner) -> dict:
    missing = [d for d in DIRS if not env.get(d) or not Path(env[d]).is_dir()]
    if missing:
        raise Misconfigured(f"directories not set or missing: {', '.join(missing)}")
    app = Path(env["APP_DIR"])
    for d in ("SCENARIOS_DIR", "REPORT_DIR", "FEEDBACK_DIR"):
        if inside(Path(env[d]), app):
            raise Misconfigured(f"{d} is inside APP_DIR, so the implementer would see it")
    token = secrets.token_hex(16)
    canaries = [Path(env[d]) / CANARY for d in ("SCENARIOS_DIR", "REPORT_DIR")]
    probes = []

    def probe(name, service, script, ok):
        code, out = runner(service, f"echo {RAN}; {script}")
        ran = RAN in out.split()
        out = out.replace(RAN, "").strip()
        probes.append({"name": name, "service": service, "ran": ran, "ok": ran and bool(ok(code, out)), "exit": code,
                       "output": out.replace(token, "<canary>")[-2000:]})

    try:
        for c in canaries:
            c.write_text(token + "\n", encoding="utf-8")
        probe("implementer cannot find the canary", "implementer", search(token, "/"),
              lambda code, out: CANARY not in out and "ENV" not in out.split())
        probe("evaluator finds the canary (control)", "evaluator", search(token, "/eval"),
              lambda code, out: out.count(CANARY) >= 2)
        probe("implementer cannot write the feedback", "implementer", "touch /work/feedback/.probe",
              lambda code, out: code != 0)
        probe("implementer can write the handoff", "implementer", "touch /work/handoff/.probe && rm /work/handoff/.probe",
              lambda code, out: code == 0)
        probe("implementer has no Docker socket", "implementer", "test -e /var/run/docker.sock",
              lambda code, out: code != 0)
        probe("evaluator cannot write the scenarios", "evaluator", "touch /eval/scenarios/.probe",
              lambda code, out: code != 0)
    finally:
        for c in canaries:
            c.unlink(missing_ok=True)
        if cleanup := getattr(runner, "cleanup", None):
            cleanup()
    return {"ok": all(p["ok"] for p in probes), "probes": probes}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--compose", type=Path, action="append",
                    help="the compose file, then any overrides, in the night's order (default: the asset)")
    a = ap.parse_args(argv)
    env = {k: os.environ[k] for k in os.environ}
    try:
        r = check(env, docker_runner(a.compose or [COMPOSE], env))
    except Misconfigured as e:
        print(json.dumps({"misconfigured": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
