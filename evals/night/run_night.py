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
import dark_factory  # noqa: E402

IMAGE = "geo-software-factory-evals-codex"
AGENTS = ("claude", "codex", "gemini", "opencode", "qoder")
DEFAULT_MODELS = {
    "claude": "claude-sonnet-5-5",
    "codex": "gpt-6-luna",
    "gemini": "gemini-3.8-flash-low",
    "opencode": "opencode/deepseek-v4.1-flash-free",
    "qoder": "Auto",
}
WATCH_FOR = ("tile.openstreetmap.org", "nominatim.openstreetmap.org", "overpass-api.de",
             "geo-software-factory/evals", "geo-software-factory/tree/main/evals", "evals/night")


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def task_paths(task_name: str = "default") -> tuple[Path, Path]:
    base = HERE if task_name == "default" else HERE / "tasks" / task_name
    task_dir = base / "task"
    scen_dir = base / "scenarios"
    if not task_dir.is_dir() or not scen_dir.is_dir():
        sys.exit(f"unknown night task {task_name!r}: missing {task_dir} or {scen_dir}")
    return task_dir, scen_dir


def prepare_app(app: Path, condition: str, task_dir: Path | None = None) -> None:
    task_dir = task_dir or (HERE / "task")
    app.mkdir(parents=True)
    if condition == "skills":
        tar = subprocess.run(["git", "-C", str(REPO), "archive", "HEAD"], check=True, capture_output=True).stdout
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            try:
                t.extractall(app, filter="data")
            except TypeError:
                t.extractall(app)
        # The factory's own docs stay; its examples and checker are not the app.
        for extra in ("examples", "scripts", "tests", ".github", "README.md", "TODO.md"):
            p = app / extra
            if p.is_dir():
                shutil.rmtree(p)
            elif p.exists():
                p.unlink()
    shutil.copy(task_dir / "product-brief.md", app / "product-brief.md")
    shutil.copytree(task_dir / "data", app / "data")
    git = ["git", "-C", str(app), "-c", "user.email=day@example.invalid", "-c", "user.name=day"]
    sh(["git", "init", "-q", "-b", "main", str(app)])
    sh(git + ["add", "-A"])
    sh(git + ["commit", "-q", "-m", "day: the brief and the data"])


def override(path: Path, codex_home: Path | None, subnet: str | None, command: list[str],
             image: str = IMAGE, extra_env: dict | None = None, mount_target: str = "/home/geo/.codex") -> Path:
    env = {"HOME": "/home/geo", **(extra_env or {})}
    svc: dict = {"image": image, "command": command, "entrypoint": [], "environment": env}
    if codex_home is not None:
        svc["volumes"] = [f"{codex_home}:{mount_target}"]
    doc: dict = {"services": {"implementer": svc}}
    if subnet:
        doc["networks"] = {"night": {"ipam": {"config": [{"subnet": subnet}]}}}
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")  # JSON is valid YAML
    return path


def agent_setup(agent: str, root: Path, minutes: int, model: str, effort: str) -> tuple[str, list[str], Path | None, str, dict, Path | None]:
    """Return (image, command, host_mount_dir, container_mount_target, extra_env, secret_file_to_clean)."""
    image = os.environ.get("EVAL_IMAGE", f"geo-software-factory-evals-{agent}")
    if agent == "codex":
        auth = Path(os.environ.get("EVAL_CODEX_HOME", Path.home() / ".codex-evals")) / "auth.json"
        if not auth.is_file():
            sys.exit(f"no Codex login at {auth}; run evals/run_codex_docker.sh --login")
        dst = root / "codex-home" / "auth.json"
        shutil.copy(auth, dst)
        os.chmod(dst, 0o600)
        cmd = (f"timeout {minutes}m codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check "
               f"-C /work/app -m {model} -c model_reasoning_effort={effort} - < /work/handoff/prompt.md")
        return image, ["sh", "-c", cmd], root / "codex-home", "/home/geo/.codex", {}, dst
    if agent == "gemini":
        g_home = Path(os.environ.get("EVAL_GEMINI_HOME", Path.home() / ".gemini-evals"))
        tok = g_home / "antigravity-cli" / "antigravity-oauth-token"
        dst_dir = root / "gemini-home" / "antigravity-cli"
        dst_dir.mkdir(parents=True, exist_ok=True)
        extra_env = {}
        secret = None
        if tok.is_file():
            secret = dst_dir / "antigravity-oauth-token"
            shutil.copy(tok, secret)
            os.chmod(secret, 0o600)
            (dst_dir / "settings.json").write_text("{}\n", encoding="utf-8")
            m_args = f"--model {model}"
        else:
            key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")
            if not key:
                sys.exit(f"no Gemini OAuth token at {tok} and no GEMINI_API_KEY set; run evals/run_gemini_docker.sh --login")
            extra_env["GEMINI_API_KEY"] = key
            (dst_dir / "settings.json").write_text('{"modelProvider": "gemini"}\n', encoding="utf-8")
            m_args = f"--model {model} --effort {effort}"
        cmd = f'timeout {minutes}m agy --print="$(cat /work/handoff/prompt.md)" --output-format stream-json {m_args} --dangerously-skip-permissions'
        return image, ["bash", "-c", cmd], root / "gemini-home", "/home/geo/.gemini", extra_env, secret
    if agent == "claude":
        tok = Path(os.environ.get("EVAL_CLAUDE_HOME", Path.home() / ".claude-evals")) / "oauth_token"
        if not tok.is_file():
            sys.exit(f"no Claude token at {tok}; save `claude setup-token` there")
        cmd = (f"timeout {minutes}m claude -p --output-format stream-json --verbose --dangerously-skip-permissions "
               f"--strict-mcp-config --no-session-persistence --model {model} < /work/handoff/prompt.md")
        return image, ["sh", "-c", cmd], None, "", {"CLAUDE_CODE_OAUTH_TOKEN": tok.read_text(encoding="utf-8").strip()}, None
    if agent == "qoder":
        pat = Path(os.environ.get("EVAL_QODER_HOME", Path.home() / ".qoder-evals")) / "pat"
        if not pat.is_file():
            sys.exit(f"no Qoder PAT at {pat}")
        cmd = (f"timeout {minutes}m qodercli -p --output-format stream-json --dangerously-skip-permissions "
               f"--strict-mcp-config --no-session-persistence --model {model} < /work/handoff/prompt.md")
        return image, ["sh", "-c", cmd], None, "", {"QODER_PERSONAL_ACCESS_TOKEN": pat.read_text(encoding="utf-8").strip()}, None
    if agent == "opencode":
        cfg = '{"$schema":"https://opencode.ai/config.json","share":"disabled","autoupdate":false}'
        cmd = f"timeout {minutes}m opencode run --format json --auto --pure --print-logs --dir /work/app --model {model} < /work/handoff/prompt.md"
        return image, ["sh", "-c", cmd], None, "", {"OPENCODE_CONFIG_CONTENT": cfg}, None
    raise ValueError(f"unknown agent {agent!r}")


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


def write_reports(root: Path, summary: dict) -> dict:
    out = root / "out"
    out.mkdir(parents=True, exist_ok=True)
    eval_path = out / "eval-report.md"
    morning_path = out / "morning-report.md"
    eval_path.write_text(dark_factory.render_eval_report(root / "app", root / "scenarios", root), encoding="utf-8")
    morning_path.write_text(dark_factory.render_morning_report(root / "app", root / "scenarios", root, summary),
                            encoding="utf-8")
    return {"eval_report": str(eval_path), "morning_report": str(morning_path)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--condition", choices=("skills", "baseline"), required=True)
    ap.add_argument("--task", default="default", help="task name under evals/night/tasks/ (default: default)")
    ap.add_argument("--agent", choices=AGENTS, default="codex")
    ap.add_argument("--minutes", type=int, default=45)
    ap.add_argument("--subnet", default=os.environ.get("GSF_DOCKER_SUBNET"))
    ap.add_argument("--model", default=None)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--run-id")
    ap.add_argument("--dry-run", action="store_true", help="prepare and prove the isolation, but run no agent")
    a = ap.parse_args(argv)
    model = a.model or DEFAULT_MODELS[a.agent]

    task_dir, scen_dir = task_paths(a.task)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    task_tag = "" if a.task == "default" else f"-{a.task}"
    run_id = a.run_id or f"{stamp}-{a.agent}-{a.condition}{task_tag}"
    root = REPO / "tmp" / "evals-night" / run_id
    if root.exists():
        sys.exit(f"{root} exists")
    for d in ("handoff", "feedback", "out", "codex-home"):
        (root / d).mkdir(parents=True)
    prepare_app(root / "app", a.condition, task_dir=task_dir)
    shutil.copytree(scen_dir, root / "scenarios")
    shutil.copy(task_dir / "prompt.md", root / "handoff" / "prompt.md")
    image, cmd_list, mount_dir, mount_target, extra_env, secret_file = agent_setup(
        a.agent, root, a.minutes, model, a.effort
    )

    env = {**os.environ, "RUN_NAME": f"gsf-night-{run_id.lower()}", "RUN_UID": str(os.getuid()),
           "RUN_GID": str(os.getgid()), "APP_DIR": str(root / "app"), "HANDOFF_DIR": str(root / "handoff"),
           "FEEDBACK_DIR": str(root / "feedback"), "SCENARIOS_DIR": str(root / "scenarios"),
           "REPORT_DIR": str(root / "out"), "EVAL_SCRIPTS": str(EVAL / "scripts")}
    night = override(root / "night.yaml", mount_dir, a.subnet, cmd_list,
                     image=image, extra_env=extra_env, mount_target=mount_target)
    files = [COMPOSE, night]
    compose = ["docker", "compose"] + [x for f in files for x in ("-f", str(f))]

    iso = check_isolation.check(env, check_isolation.docker_runner(files, env))
    (root / "isolation.json").write_text(json.dumps(iso, ensure_ascii=False, indent=1), encoding="utf-8")
    if not iso["ok"] or a.dry_run:
        if secret_file is not None:
            secret_file.unlink(missing_ok=True)
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
        final = override(root / "final.yaml", mount_dir, a.subnet,
                         ["sh", "-c", "git clone -q /work/app /tmp/final && cd /tmp/final && exec sh start.sh"],
                         image=image, mount_target=mount_target)
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
        if secret_file is not None:
            secret_file.unlink(missing_ok=True)
    summary = {"run": run_id, "task": a.task, "agent": a.agent, "condition": a.condition, "model": model, "effort": a.effort,
               "limit_minutes": a.minutes, **summarize(root, exit_code, seconds, tree)}
    summary["deploy_ready"] = bool(summary.get("final_ok") and not summary.get("left_dirty"))
    (root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    write_reports(root, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
