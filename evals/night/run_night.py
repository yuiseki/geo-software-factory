#!/usr/bin/env python3
"""One night of the dark factory, end to end, on a small task: the day's brief in, a judged app out.

    python3 evals/night/run_night.py --condition skills|baseline [--minutes 45] [--subnet 10.213.57.0/24]
                                     [--model gpt-6-luna] [--effort medium] [--dry-run]

What it does, in the containers of geo-software-eval's assets/isolation/:

1. Makes the app repository: the task (product-brief.md, data/) and, for `skills`, this repository's skills and
   AGENTS.md (git archive, so evals/ is not in it). One commit, as the day hands it over.
2. Copies the held-out scenarios to the evaluator's side, and only Codex's auth.json to a fresh Codex home.
3. Proves the isolation with check_isolation.py, using the same compose files as the night. Stops if it fails.
4. Starts the evaluator (eval_watch.py), then Codex as the implementer, cut off after --minutes.
5. After Codex ends, starts the last commit with `sh start.sh` and judges it once more (the final judgement).
6. Writes summary.json: the final result per scenario, evaluation requests made during the night, commits,
   whether the tree was left clean, the exit (124 = cut off), the tokens Codex reported, and any mention of the
   public OSM servers or this repository's evals/ in the implementer's log.

Everything lands in tmp/evals-night/<run id>/ (git-ignored). Needs Docker, the image of evals/Dockerfile.codex
and a Codex login in $EVAL_CODEX_HOME (default ~/.codex-evals; see evals/run_codex_docker.sh --login).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import io
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
EVAL = REPO / ".agents" / "skills" / "geo-software-eval"
COMPOSE = EVAL / "assets" / "isolation" / "compose.yaml"
sys.path.insert(0, str(EVAL / "scripts"))
import check_isolation  # noqa: E402

IMAGE = "geo-software-factory-evals-codex"
WATCH_FOR = ("tile.openstreetmap.org", "nominatim.openstreetmap.org", "overpass-api.de",
             "geo-software-factory/evals", "geo-software-factory/tree/main/evals", "evals/night")


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def prepare_app(app: Path, condition: str) -> None:
    app.mkdir(parents=True)
    if condition == "skills":
        tar = subprocess.run(["git", "-C", str(REPO), "archive", "HEAD"], check=True, capture_output=True).stdout
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            t.extractall(app, filter="data")
        # The factory's own docs stay; its examples and checker are not the app.
        for extra in ("examples", "scripts", "tests", ".github", "README.md", "TODO.md"):
            p = app / extra
            if p.is_dir():
                shutil.rmtree(p)
            elif p.exists():
                p.unlink()
    shutil.copy(HERE / "task" / "product-brief.md", app / "product-brief.md")
    shutil.copytree(HERE / "task" / "data", app / "data")
    git = ["git", "-C", str(app), "-c", "user.email=day@example.invalid", "-c", "user.name=day"]
    sh(["git", "init", "-q", "-b", "main", str(app)])
    sh(git + ["add", "-A"])
    sh(git + ["commit", "-q", "-m", "day: the brief and the data"])


def override(path: Path, codex_home: Path, subnet: str | None, command: list[str]) -> Path:
    doc = {"services": {"implementer": {
        "image": IMAGE, "command": command, "entrypoint": [],
        "environment": {"HOME": "/home/geo"},
        "volumes": [f"{codex_home}:/home/geo/.codex"]}}}
    if subnet:
        doc["networks"] = {"night": {"ipam": {"config": [{"subnet": subnet}]}}}
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")  # JSON is valid YAML
    return path


def tree_state(app: Path) -> dict:
    """Taken right after the implementer ends, before anything else touches the tree."""
    commits = sh(["git", "-C", str(app), "rev-list", "--count", "HEAD"]).stdout.strip()
    dirty = sh(["git", "-C", str(app), "status", "--porcelain"]).stdout.strip()
    return {"commits_after_day": int(commits) - 1, "left_dirty": bool(dirty)}


def summarize(root: Path, exit_code: int | None, seconds: float, tree: dict) -> dict:
    out = root / "out"
    final = json.loads((out / "final.json").read_text(encoding="utf-8")) if (out / "final.json").exists() else None
    requests = sorted(p.name for p in out.glob("*.json") if re.match(r"^\d{8}T\d{6}Z-", p.name))
    log = (root / "implementer.log").read_text(encoding="utf-8", errors="replace") if (root / "implementer.log").exists() else ""
    tokens = re.findall(r"tokens used\s*\n?\s*([\d,]+)", log)
    return {
        "exit": exit_code, "minutes": round(seconds / 60, 1),
        "final": {s["id"]: s["result"] for s in final["scenarios"]} if final else None,
        "final_ok": bool(final and final["ok"]),
        "final_version": final["version"] if final else None,
        "eval_requests": len(requests),
        **tree,
        "tokens": tokens[-1] if tokens else None,
        "mentions": {w: log.count(w) for w in WATCH_FOR if w in log},
    }


def wait_exit(compose, env, service, limit_s):
    deadline = time.monotonic() + limit_s
    while time.monotonic() < deadline:
        ps = subprocess.run(compose + ["ps", "-a", "--format", "json", service], env=env, capture_output=True, text=True)
        rows = [json.loads(x) for x in ps.stdout.splitlines() if x.strip().startswith("{")]
        if rows and rows[0].get("State") == "exited":
            return rows[0].get("ExitCode")
        time.sleep(15)
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--condition", choices=("skills", "baseline"), required=True)
    ap.add_argument("--minutes", type=int, default=45)
    ap.add_argument("--subnet", default=os.environ.get("GSF_DOCKER_SUBNET"))
    ap.add_argument("--model", default="gpt-6-luna")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--run-id")
    ap.add_argument("--dry-run", action="store_true", help="prepare and prove the isolation, but run no agent")
    a = ap.parse_args(argv)

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = a.run_id or f"{stamp}-{a.condition}"
    root = REPO / "tmp" / "evals-night" / run_id
    if root.exists():
        sys.exit(f"{root} exists")
    for d in ("handoff", "feedback", "out", "codex-home"):
        (root / d).mkdir(parents=True)
    prepare_app(root / "app", a.condition)
    shutil.copytree(HERE / "scenarios", root / "scenarios")
    auth = Path(os.environ.get("EVAL_CODEX_HOME", Path.home() / ".codex-evals")) / "auth.json"
    if not auth.is_file():
        sys.exit(f"no Codex login at {auth}; run evals/run_codex_docker.sh --login")
    shutil.copy(auth, root / "codex-home" / "auth.json")
    os.chmod(root / "codex-home" / "auth.json", 0o600)
    shutil.copy(HERE / "task" / "prompt.md", root / "handoff" / "prompt.md")

    env = {**os.environ, "RUN_NAME": f"gsf-night-{run_id.lower()}", "RUN_UID": str(os.getuid()),
           "RUN_GID": str(os.getgid()), "APP_DIR": str(root / "app"), "HANDOFF_DIR": str(root / "handoff"),
           "FEEDBACK_DIR": str(root / "feedback"), "SCENARIOS_DIR": str(root / "scenarios"),
           "REPORT_DIR": str(root / "out"), "EVAL_SCRIPTS": str(EVAL / "scripts")}
    codex = (f"timeout {a.minutes}m codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check "
             f"-C /work/app -m {a.model} -c model_reasoning_effort={a.effort} - < /work/handoff/prompt.md")
    night = override(root / "night.yaml", root / "codex-home", a.subnet, ["sh", "-c", codex])
    files = [COMPOSE, night]
    compose = ["docker", "compose"] + [x for f in files for x in ("-f", str(f))]

    iso = check_isolation.check(env, check_isolation.docker_runner(files, env))
    (root / "isolation.json").write_text(json.dumps(iso, ensure_ascii=False, indent=1), encoding="utf-8")
    if not iso["ok"] or a.dry_run:
        (root / "codex-home" / "auth.json").unlink(missing_ok=True)
    if not iso["ok"]:
        print(json.dumps({"isolation": "failed", "root": str(root)}))
        return 1
    if a.dry_run:
        print(json.dumps({"isolation": "ok", "root": str(root)}))
        return 0

    t0 = time.monotonic()
    exit_code, seconds, tree = None, 0.0, {}
    try:
        sh(compose + ["up", "-d", "evaluator", "implementer"], env=env)
        exit_code = wait_exit(compose, env, "implementer", a.minutes * 60 + 600)
        with open(root / "implementer.log", "w", encoding="utf-8") as f:
            subprocess.run(compose + ["logs", "--no-color", "--no-log-prefix", "implementer"], env=env, stdout=f,
                           stderr=subprocess.STDOUT)
        subprocess.run(compose + ["logs", "--no-color", "evaluator"], env=env,
                       stdout=open(root / "evaluator.log", "w", encoding="utf-8"), stderr=subprocess.STDOUT)
        seconds = time.monotonic() - t0
        tree = tree_state(root / "app")

        # Final judgement: the last commit, started the agreed way, by the evaluator, once.
        sh(compose + ["stop", "evaluator"], env=env)
        rev = sh(["git", "-C", str(root / "app"), "rev-parse", "HEAD"]).stdout.strip()
        final = override(root / "final.yaml", root / "codex-home", a.subnet, ["sh", "-c", "git clone -q /work/app /tmp/final && cd /tmp/final && exec sh start.sh"])
        fcompose = ["docker", "compose"] + [x for f in (COMPOSE, final) for x in ("-f", str(f))]
        sh(fcompose + ["up", "-d", "--force-recreate", "implementer"], env=env)
        (root / "feedback-final").mkdir()
        for _ in range(30):
            subprocess.run(fcompose + ["run", "--rm", "-T", "-v", f"{root / 'feedback-final'}:/eval/final",
                                       "evaluator", "python3", "-I", "/eval/bin/run_eval.py",
                                       "--scenarios", "/eval/scenarios", "--base", "http://implementer:8787",
                                       "--report", "/eval/out/final.json", "--feedback", "/eval/final/eval-feedback.md",
                                       "--version", rev], env=env, capture_output=True, text=True)
            fin = json.loads((root / "out" / "final.json").read_text(encoding="utf-8"))
            if not any(c["observed"].get("status") == "応答なし" for s in fin["scenarios"] for c in s["checks"]):
                break
            time.sleep(2)
        subprocess.run(fcompose + ["logs", "--no-color", "implementer"], env=env,
                       stdout=open(root / "final-app.log", "w", encoding="utf-8"), stderr=subprocess.STDOUT)
    finally:
        subprocess.run(compose + ["down", "--remove-orphans", "-t", "2"], env=env, capture_output=True)
        (root / "codex-home" / "auth.json").unlink(missing_ok=True)
    summary = {"run": run_id, "condition": a.condition, "model": a.model, "effort": a.effort,
               "limit_minutes": a.minutes, **summarize(root, exit_code, seconds, tree)}
    (root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
