#!/usr/bin/env python3
"""General-purpose Dark Factory harness: preflight, eval-of-eval, isolated night loop, final judgement, morning report.

    python3 dark_factory.py preflight    --app-dir APP --scenarios SCENARIOS --work-dir WORK [--mode local|docker]
    python3 dark_factory.py eval-of-eval --scenarios SCENARIOS --report OUT/eval-of-eval.json --good URL [--break NAME=URL ...]
    python3 dark_factory.py run          --app-dir APP --scenarios SCENARIOS --work-dir WORK [--mode local|docker]
                                         [--agent claude|codex|opencode|custom] [--implementer-cmd CMD]
                                         [--start-cmd "sh start.sh"] [--port 8787] [--minutes 45]
                                         [--verify-url URL] [--install-skills] [--dry-run]
    python3 dark_factory.py report       --app-dir APP --scenarios SCENARIOS --work-dir WORK

Enforces the Dark Factory invariants by program:
1. Preflight refuses to start unless product-brief.md passes check_brief.py, scenarios are outside the app repository
   and valid, the stop switch is off, and (in docker mode) container isolation is proven with canaries.
2. During the night, the evaluator watches handoff/ready.json and writes only symptoms to feedback/eval-feedback.md.
3. If the stop switch file (AGENT_STOP_FILE, default WORK/STOP) appears or the deadline passes, the implementer is stopped.
4. Final judgement runs on a fresh `git clone` of HEAD (uncommitted files cannot help it pass).
5. Produces out/eval-report.md, out/morning-report.md and out/summary.json for the human in the morning.
"""
from __future__ import annotations

import argparse
import datetime
import io
import json
import os
import re
import shlex
import shutil
import signal
import socket
import subprocess
import sys
import tarfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVAL_SKILL = HERE.parent
SKILLS_DIR = EVAL_SKILL.parent
REPO_ROOT = SKILLS_DIR.parent.parent
COMPOSE = EVAL_SKILL / "assets" / "isolation" / "compose.yaml"
UNATTENDED_SETTINGS = SKILLS_DIR / "geo-software-swarm" / "assets" / "unattended-settings.json"
HOOKS_SCRIPT = SKILLS_DIR / "geo-software-swarm" / "scripts" / "hooks.py"

for p in (
    HERE,
    SKILLS_DIR / "geo-software-product-grilling" / "scripts",
    SKILLS_DIR / "geo-software-deploy" / "scripts",
    SKILLS_DIR / "geo-software-security-audit" / "scripts",
):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import audit_probe  # noqa: E402
import check_brief  # noqa: E402
import check_isolation  # noqa: E402
import deploy_gate  # noqa: E402
import eval_watch  # noqa: E402
import run_eval  # noqa: E402
import smoke  # noqa: E402

VALID_CHECK_KINDS = ("http", "geojson", "command", "llm")
AGENTS = ("claude", "codex", "gemini", "opencode", "qoder", "custom")
DEFAULT_CHECKLIST = (
    "評価者に最新のコミットで評価を頼み、全シナリオが合格したか確かめる",
    "地図データとタイルの帰属表示が画面と README の両方にあるか確かめる",
    "product-brief.md の「夜に決めたこと」と「止まったこと」を書き、未コミットの変更を残さない",
)


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def product_name(brief_path: Path) -> str:
    if brief_path.is_file():
        for line in brief_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].replace("プロダクト概要:", "").strip() or brief_path.parent.name
    return brief_path.parent.name


def bullet_items(section_text: str) -> list[str]:
    items = []
    for line in section_text.splitlines():
        s = line.strip()
        if s.startswith("-"):
            val = s[1:].strip()
            if val and not check_brief.undecided(val):
                items.append(val)
    return items


def validate_scenarios(scenarios_dir: Path, app_dir: Path) -> dict:
    errors: list[str] = []
    if not scenarios_dir.is_dir():
        return {"count": 0, "ok": False, "errors": [f"シナリオのディレクトリが無い: {scenarios_dir}"]}
    if app_dir.exists() and run_eval.inside(scenarios_dir, app_dir):
        errors.append("シナリオが実装のリポジトリの中にある。外に置く")
    files = sorted(scenarios_dir.glob("*.json"))
    if not files:
        errors.append("シナリオの JSON ファイルが 1 本も無い")
    for f in files:
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            errors.append(f"{f.name}: JSON として読めない ({e})")
            continue
        if not isinstance(doc, dict):
            errors.append(f"{f.name}: JSON オブジェクトではない")
            continue
        if not str(doc.get("symptom", "")).strip():
            errors.append(f"{f.name}: symptom (実装者に返す症状の 1 行) が無い")
        checks = doc.get("checks")
        if not isinstance(checks, list) or not checks:
            errors.append(f"{f.name}: checks が空または配列ではない")
            continue
        for i, c in enumerate(checks):
            kind = c.get("kind") if isinstance(c, dict) else None
            if kind not in VALID_CHECK_KINDS:
                errors.append(f"{f.name}: checks[{i}] の kind {kind!r} が不正 ({', '.join(VALID_CHECK_KINDS)} のいずれか)")
    return {"count": len(files), "ok": not errors, "errors": errors}


def eval_of_eval(scenarios_dir: Path, good_base: str, broken_bases: dict[str, str], report_path: Path,
                 timeout: float = 15) -> dict:
    """Verify that the reference implementation passes all scenarios and every broken variant fails at least one."""
    tmp_dir = report_path.parent / ".eval-of-eval-tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    try:
        good = run_eval.run(scenarios=scenarios_dir, base=good_base, app_repo=None,
                            report=tmp_dir / "good.json", feedback=None, timeout=timeout, version="reference-good")
        breaks = {}
        for name, base in broken_bases.items():
            r = run_eval.run(scenarios=scenarios_dir, base=base, app_repo=None,
                             report=tmp_dir / f"break-{name}.json", feedback=None, timeout=timeout,
                             version=f"break-{name}")
            failed = [s["id"] for s in r["scenarios"] if s["result"] != "pass"]
            passed = [s["id"] for s in r["scenarios"] if s["result"] == "pass"]
            breaks[name] = {"base": base, "caught": bool(failed), "failed_scenarios": failed,
                            "passed_scenarios": passed}
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    ok = bool(good["ok"]) and all(b["caught"] for b in breaks.values())
    out = {
        "when": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "ok": ok,
        "good": {"base": good_base, "ok": good["ok"],
                 "results": {s["id"]: s["result"] for s in good["scenarios"]}},
        "breaks": breaks,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def ledger_path(work_dir: Path) -> Path:
    return work_dir / "state" / "ledger.json"


def load_ledger(work_dir: Path, initial_rev: str | None = None, day_commits: int = 1) -> dict:
    p = ledger_path(work_dir)
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return {
        "version": 1,
        "resume_epoch": 0,
        "day_commits": day_commits,
        "best_rev": initial_rev,
        "best_satisfaction": -1.0,
        "consecutive_no_progress": 0,
        "dead_ends": [],
        "rounds": [],
    }


def save_ledger(work_dir: Path, ledger: dict) -> None:
    p = ledger_path(work_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(p)


def rollback_to_best(app_dir: Path, best_rev: str, round_num: int) -> str | None:
    """Save the regressed HEAD on a dead-end branch and reset the working tree to best_rev."""
    if not best_rev:
        return None
    branch = f"dead-end/round-{round_num}"
    subprocess.run(["git", "-C", str(app_dir), "branch", "-f", branch, "HEAD"], capture_output=True)
    sh(["git", "-C", str(app_dir), "reset", "--hard", best_rev])
    sh(["git", "-C", str(app_dir), "clean", "-fd"])
    return branch


def render_round_prompt(base_prompt: str, ledger: dict, round_num: int, max_rounds: int,
                        remaining_minutes: float, feedback_path: Path, stagnation_limit: int = 3) -> str:
    lines = [base_prompt.rstrip(), "", "## ハーネスからの現在状態 (Round Ledger)", ""]
    lines.append(f"- ラウンド: {round_num} / {max_rounds} (resume_epoch: {ledger.get('resume_epoch', 0)})")
    lines.append(f"- 残り時間: 約 {max(0.0, remaining_minutes):.1f} 分")
    best_rev = ledger.get("best_rev") or "なし"
    best_sat = ledger.get("best_satisfaction", -1.0)
    sat_str = f"{best_sat:.3f}" if best_sat >= 0 else "未評価"
    lines.append(f"- 現在の最高到達コミット: `{best_rev}` (Satisfaction: {sat_str})")

    dead_ends = ledger.get("dead_ends") or []
    if dead_ends:
        lines.append("- 過去に試して失敗・退行した手 (同じ手は繰り返さない):")
        for item in dead_ends[-5:]:
            lines.append(f"  - {item}")

    if ledger.get("consecutive_no_progress", 0) >= stagnation_limit:
        lines.extend([
            "",
            "## 停滞監査の指示 (重要)",
            f"- 直近 {ledger['consecutive_no_progress']} ラウンド連続で評価が改善していません。",
            "- 同じ箇所の小手先の修正を止め、原因を根本から切り分けて別アプローチを設計・実装してください。",
        ])

    if feedback_path.is_file():
        fb = feedback_path.read_text(encoding="utf-8").strip()
        if fb:
            if len(fb) > 4000:
                fb = fb[:4000] + "\n...(省略)"
            lines.extend(["", "## 直近の評価症状 (eval-feedback.md)", "", fb])

    lines.append("")
    return "\n".join(lines)


def doctor(agent: str = "claude", mode: str = "local", app_dir: Path | None = None,
           env: dict | None = None) -> dict:
    """Check runtime prerequisites (git, python3, agent CLI, docker, and optional brief env/CLIs)."""
    env = os.environ if env is None else env
    checks: dict[str, dict] = {}

    def probe_cmd(name: str, cmd: list[str]) -> dict:
        exe = shutil.which(cmd[0])
        if not exe:
            return {"ok": False, "error": f"{cmd[0]} が PATH に無い"}
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            out = (p.stdout or p.stderr).strip().splitlines()
            return {"ok": p.returncode == 0, "path": exe, "version": out[0] if out else ""}
        except (OSError, subprocess.TimeoutExpired) as e:
            return {"ok": False, "path": exe, "error": str(e)}

    checks["python3"] = probe_cmd("python3", [sys.executable, "--version"])
    checks["git"] = probe_cmd("git", ["git", "--version"])
    agent_bins = {
        "claude": ["claude", "--version"],
        "codex": ["codex", "--version"],
        "gemini": ["agy", "--version"],
        "opencode": ["opencode", "--version"],
        "qoder": ["qodercli", "--version"],
    }
    if agent in agent_bins:
        checks[f"agent:{agent}"] = probe_cmd(agent, agent_bins[agent])
    if mode == "docker":
        checks["docker_compose"] = probe_cmd("docker", ["docker", "compose", "version"])
    if app_dir is not None and (app_dir / "product-brief.md").is_file():
        checks["brief"] = check_brief.check(app_dir / "product-brief.md", env=env)

    ok = all(v.get("ok") for v in checks.values())
    return {"ok": ok, "agent": agent, "mode": mode, "checks": checks}


def prepare_workspace(app_dir: Path, work_dir: Path, scenarios_dir: Path, install_skills: bool = False,
                      repo_root: Path | None = None, deadline: datetime.datetime | None = None,
                      port: int = 8787, start_cmd: str = "sh start.sh", mode: str = "local") -> dict:
    app_dir.mkdir(parents=True, exist_ok=True)
    for d in ("handoff", "feedback", "out", "state", "claude-settings", "codex-home"):
        (work_dir / d).mkdir(parents=True, exist_ok=True)

    root = repo_root or REPO_ROOT
    if install_skills and (root / ".agents" / "skills").is_dir():
        if (root / ".git").exists():
            tar = subprocess.run(["git", "-C", str(root), "archive", "HEAD"], check=True, capture_output=True).stdout
            with tarfile.open(fileobj=io.BytesIO(tar)) as t:
                try:
                    t.extractall(app_dir, filter="data")
                except TypeError:
                    t.extractall(app_dir)
            for extra in ("examples", "scripts", "tests", ".github", "README.md", "TODO.md"):
                p = app_dir / extra
                if p.is_dir():
                    shutil.rmtree(p)
                elif p.exists():
                    p.unlink()
        else:
            for item in ("AGENTS.md", "CLAUDE.md"):
                if (root / item).is_file() and not (app_dir / item).exists():
                    shutil.copy(root / item, app_dir / item)
            if not (app_dir / ".agents" / "skills").exists():
                shutil.copytree(root / ".agents" / "skills", app_dir / ".agents" / "skills")

    git = ["git", "-C", str(app_dir), "-c", "user.email=day@example.invalid", "-c", "user.name=day"]
    if not (app_dir / ".git").exists():
        sh(["git", "init", "-q", "-b", "main", str(app_dir)])
    has_head = subprocess.run(["git", "-C", str(app_dir), "rev-parse", "--verify", "HEAD"],
                              capture_output=True).returncode == 0
    dirty = subprocess.run(["git", "-C", str(app_dir), "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    if not has_head or dirty:
        sh(git + ["add", "-A"])
        sh(git + ["commit", "-q", "--allow-empty", "-m", "day: the brief and the data"])

    handoff_file = "/work/handoff/ready.json" if mode == "docker" else str((work_dir / "handoff" / "ready.json").resolve())
    feedback_file = "/work/feedback/eval-feedback.md" if mode == "docker" else str((work_dir / "feedback" / "eval-feedback.md").resolve())
    prompt = "\n".join([
        "いまは夜で、人間はいません。質問せず、最後まで自分で進めてください。",
        "",
        "このリポジトリの `product-brief.md` が、昼に人間と決めたプロダクト概要です。これに従って、アプリを作ってください。",
        "",
        "評価は、あなたとは別の評価者が、あなたに見せないシナリオで行います。",
        "",
        f"- 評価を頼むには、アプリを `{start_cmd}` で裏で起動したまま ({port} 番)、`{handoff_file}` に "
        f'`{{"rev": "<git rev-parse HEAD の値>", "port": {port}}}` を書きます。同じ版をもう一度頼むときは `"nonce"` に新しい値を足します。',
        f"- 結果の症状は、数十秒以内に `{feedback_file}` に出ます。ファイルの「判定した版」が、頼んだ版になるまで待ってから読んでください。",
        "- 症状を読んで直し、また頼む、を繰り返してください。評価を頼む前に、変更をコミットしてください。",
        "- 壊した版を評価に出してはいけません (評価そのものの確かめは評価者の仕事です)。",
        "",
        "作業が終わったら、すべてコミットし、`product-brief.md` の「夜に決めたこと」と「止まったこと」を書いてコミットし、終えてください。"
        f"終えたあと、評価者が最後のコミットを `{start_cmd}` で起動して、同じシナリオで最終判定します。",
        "",
    ])
    prompt_path = work_dir / "handoff" / "prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    (work_dir / "state" / "base-prompt.md").write_text(prompt, encoding="utf-8")

    checklist_path = work_dir / "state" / "checklist.txt"
    if not checklist_path.exists():
        checklist_path.write_text("\n".join(DEFAULT_CHECKLIST) + "\n", encoding="utf-8")

    settings_path = work_dir / "claude-settings" / "settings.json"
    if UNATTENDED_SETTINGS.is_file():
        raw = UNATTENDED_SETTINGS.read_text(encoding="utf-8")
        scen_no_slash = str(scenarios_dir.resolve()).lstrip("/")
        raw = raw.replace("HOOKS", str(HOOKS_SCRIPT.resolve())).replace("SCENARIOS", scen_no_slash)
        settings_path.write_text(raw, encoding="utf-8")

    return {
        "prompt": str(prompt_path),
        "settings": str(settings_path),
        "checklist": str(checklist_path),
        "handoff_file": handoff_file,
        "feedback_file": feedback_file,
        "deadline": deadline.isoformat() if deadline else None,
    }


def preflight(app_dir: Path, scenarios_dir: Path, work_dir: Path, mode: str = "local",
              compose_files: list[Path] | None = None, env: dict | None = None, runner=None) -> dict:
    env = os.environ if env is None else env
    errors: list[str] = []

    if app_dir.exists() and run_eval.inside(work_dir, app_dir):
        errors.append("作業ディレクトリ (work-dir) が実装のリポジトリの中にある。外に置く")

    brief_path = app_dir / "product-brief.md"
    if not brief_path.is_file():
        brief_rep = {"brief": str(brief_path), "ok": False, "errors": [{"item": "product-brief.md", "why": "ファイルが無い"}]}
        errors.append("product-brief.md が無い")
    else:
        brief_rep = check_brief.check(brief_path, env=env)
        if not brief_rep["ok"]:
            for e in brief_rep["errors"]:
                errors.append(f"product-brief.md: {e['item']} ({e['why']})")

    scen_rep = validate_scenarios(scenarios_dir, app_dir)
    if not scen_rep["ok"]:
        errors.extend(scen_rep["errors"])

    stop_file = Path(env.get("AGENT_STOP_FILE", work_dir / "STOP"))
    stop_active = stop_file.exists()
    if stop_active:
        errors.append(f"停止スイッチが入っている: {stop_file}")

    iso_rep = None
    if mode == "docker":
        for d in ("handoff", "feedback", "out"):
            (work_dir / d).mkdir(parents=True, exist_ok=True)
        app_dir.mkdir(parents=True, exist_ok=True)
        iso_env = {
            **env,
            "APP_DIR": str(app_dir.resolve()),
            "HANDOFF_DIR": str((work_dir / "handoff").resolve()),
            "FEEDBACK_DIR": str((work_dir / "feedback").resolve()),
            "SCENARIOS_DIR": str(scenarios_dir.resolve()),
            "REPORT_DIR": str((work_dir / "out").resolve()),
            "EVAL_SCRIPTS": str(HERE.resolve()),
        }
        files = compose_files or [COMPOSE]
        try:
            iso_rep = check_isolation.check(iso_env, runner or check_isolation.docker_runner(files, iso_env))
            if not iso_rep["ok"]:
                errors.append("コンテナの隔離の検査に落ちた")
        except check_isolation.Misconfigured as e:
            iso_rep = {"ok": False, "misconfigured": str(e)}
            errors.append(f"コンテナの隔離の設定誤り: {e}")

    return {
        "ok": not errors,
        "mode": mode,
        "brief": brief_rep,
        "scenarios": scen_rep,
        "stop_switch": stop_active,
        "isolation": iso_rep,
        "errors": errors,
    }


def tree_state(app_dir: Path, day_commits: int = 1) -> dict:
    commits = int(sh(["git", "-C", str(app_dir), "rev-list", "--count", "HEAD"]).stdout.strip())
    head = sh(["git", "-C", str(app_dir), "rev-parse", "--short", "HEAD"]).stdout.strip()
    dirty = sh(["git", "-C", str(app_dir), "status", "--porcelain"]).stdout.strip()
    return {"head": head, "commits_after_day": max(0, commits - day_commits), "left_dirty": bool(dirty)}


def terminate_process(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except OSError:
        proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            proc.kill()
        proc.wait(timeout=5)


def default_agent_cmd(agent: str, work_dir: Path, model: str | None = None, effort: str = "medium",
                      mode: str = "local") -> list[str]:
    prompt_file = "/work/handoff/prompt.md" if mode == "docker" else str((work_dir / "handoff" / "prompt.md").resolve())
    if agent == "claude":
        settings = str((work_dir / "claude-settings" / "settings.json").resolve())
        mflag = f"--model {shlex.quote(model)} " if model else ""
        return ["sh", "-c", f"claude -p --settings {shlex.quote(settings)} {mflag}< {shlex.quote(prompt_file)}"]
    if agent == "codex":
        m = model or "gpt-6-luna"
        return ["sh", "-c", f"codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check "
                            f"-m {shlex.quote(m)} -c model_reasoning_effort={shlex.quote(effort)} - < {shlex.quote(prompt_file)}"]
    if agent == "opencode":
        mflag = f"-m {shlex.quote(model)} " if model else ""
        return ["sh", "-c", f"opencode run {mflag}\"$(cat {shlex.quote(prompt_file)})\""]
    if agent == "gemini":
        m = model or "gemini-3.8-flash-low"
        return ["sh", "-c", f"agy --print=\"$(cat {shlex.quote(prompt_file)})\" --output-format stream-json "
                            f"--model {shlex.quote(m)} --effort {shlex.quote(effort)} --dangerously-skip-permissions"]
    if agent == "qoder":
        m = model or "Auto"
        return ["sh", "-c", f"qodercli -p --output-format stream-json --dangerously-skip-permissions "
                            f"--strict-mcp-config --no-session-persistence --model {shlex.quote(m)} < {shlex.quote(prompt_file)}"]
    raise ValueError(f"unknown agent {agent!r}")


def judge_clean_checkout(app_dir: Path, scenarios_dir: Path, work_dir: Path, start_cmd: str = "sh start.sh",
                         startup_timeout: float = 15.0, eval_timeout: float = 15.0,
                         report_path: Path | None = None, feedback_path: Path | None = None,
                         run_audit: bool = True) -> dict:
    """Clone HEAD into a clean directory, start the app on a free port, and judge it once with run_eval.py."""
    rev = sh(["git", "-C", str(app_dir), "rev-parse", "--short", "HEAD"]).stdout.strip()
    checkout = work_dir / "final-checkout"
    if checkout.exists():
        shutil.rmtree(checkout)
    sh(["git", "clone", "-q", str(app_dir), str(checkout)])
    shutil.rmtree(checkout / ".git", ignore_errors=True)
    port = free_port()
    env = {**os.environ, "PORT": str(port)}
    log_path = work_dir / "out" / "final-app.log"
    rep_path = report_path or (work_dir / "out" / "final.json")
    fb_path = feedback_path or (work_dir / "feedback" / "final-feedback.md")
    with open(log_path, "w", encoding="utf-8") as log_file:
        proc = subprocess.Popen(["sh", "-c", start_cmd], cwd=checkout, env=env,
                                stdout=log_file, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            deadline = time.monotonic() + startup_timeout
            out = None
            while True:
                out = run_eval.run(scenarios=scenarios_dir, base=f"http://127.0.0.1:{port}", app_repo=None,
                                   report=rep_path, feedback=fb_path, timeout=eval_timeout, version=rev)
                no_answer = any(c["observed"].get("status") == "応答なし"
                                for s in out["scenarios"] for c in s["checks"])
                if not no_answer or time.monotonic() >= deadline or proc.poll() is not None:
                    break
                time.sleep(0.25)
            if run_audit:
                audit_probe.probe(base=f"http://127.0.0.1:{port}", report_path=work_dir / "out" / "audit.json",
                                  timeout=eval_timeout)
            return out
        finally:
            terminate_process(proc)
            shutil.rmtree(checkout, ignore_errors=True)


def render_eval_report(app_dir: Path, scenarios_dir: Path, work_dir: Path, evaluator_name: str = "独立プロセス (run_eval.py)") -> str:
    brief_path = app_dir / "product-brief.md"
    name = product_name(brief_path)
    out_dir = work_dir / "out"
    final = json.loads((out_dir / "final.json").read_text(encoding="utf-8")) if (out_dir / "final.json").is_file() else None
    eoe = json.loads((out_dir / "eval-of-eval.json").read_text(encoding="utf-8")) if (out_dir / "eval-of-eval.json").is_file() else None
    prod = json.loads((out_dir / "prod-eval.json").read_text(encoding="utf-8")) if (out_dir / "prod-eval.json").is_file() else None

    when = final["when"] if final else datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    target = f"手元の版のコミット {final['version']}" if final else "未評価"
    if prod:
        target += f" / 本番 URL {prod['base']}"

    lines = [
        f"# 評価の報告: {name}",
        "",
        f"- 評価した日時: {when}",
        f"- 対象: {target}",
        f"- 評価者: {evaluator_name}",
        f"- シナリオの置き場所: `{scenarios_dir}`",
        "",
        "## 結果",
        "",
        "| シナリオ | 対象 | 代役 / 本物 | 合否 | 根拠 (観測の置き場所) | 確信 |",
        "|---|---|---|---|---|---|",
    ]
    if final and final.get("scenarios"):
        for s in final["scenarios"]:
            obs = " / ".join(run_eval.describe(c["observed"]) for c in s.get("checks", [])) or "観測なし"
            res_jp = "合格" if s["result"] == "pass" else ("エラー" if s["result"] == "error" else "不合格")
            lines.append(f"| {s['id']} ({s.get('name') or s.get('symptom', '')}) | {final['version']} | 手元 | "
                         f"{res_jp} | {obs} (`out/final.json`) | 機械判定 |")
        if prod and prod.get("scenarios"):
            for s in prod["scenarios"]:
                obs = " / ".join(run_eval.describe(c["observed"]) for c in s.get("checks", [])) or "観測なし"
                res_jp = "合格" if s["result"] == "pass" else ("エラー" if s["result"] == "error" else "不合格")
                lines.append(f"| {s['id']} ({s.get('name') or s.get('symptom', '')}) | {prod['base']} | 本番 | "
                             f"{res_jp} | {obs} (`out/prod-eval.json`) | 機械判定 |")
        passed = sum(1 for s in final["scenarios"] if s["result"] == "pass")
        total = len(final["scenarios"])
        sat = final.get("satisfaction", round(passed / total, 3) if total else 0.0)
        splits = ", ".join(final.get("split_scenarios", [])) or "なし"
        low_confs = ", ".join(final.get("low_confidence_scenarios", [])) or "なし"
        lines.extend([
            "",
            f"- 合格: {passed} / {total} (Satisfaction: {sat})",
            f"- 判定が割れたもの: {splits}",
            f"- 確信が低いもの: {low_confs}",
        ])
    else:
        lines.extend(["| (なし) | - | - | 未評価 | `out/final.json` が無い | - |", "", "- 合格: 0 / 0", "- 判定が割れたもの: なし"])

    lines.extend([
        "",
        "## 評価の評価",
        "",
        "| 壊し方 | 落ちたシナリオ | 通ってしまったシナリオ |",
        "|---|---|---|",
    ])
    if eoe and eoe.get("breaks"):
        for bname, binfo in eoe["breaks"].items():
            failed = ", ".join(binfo.get("failed_scenarios", [])) or "なし (要見直し)"
            passed = ", ".join(binfo.get("passed_scenarios", [])) or "なし"
            lines.append(f"| {bname} | {failed} | {passed} |")
    else:
        lines.append("| 未実施 | - | - |")

    lines.extend([
        "",
        "## 確かめていないこと",
        "",
        "- 実機のブラウザでの目視と操作感、本物の外部サービスの契約上限や長期の安定性、法的な最終判断",
        "",
        "## 人間に見てほしいこと",
        "",
    ])
    failed_final = [s for s in (final.get("scenarios", []) if final else []) if s["result"] != "pass"]
    if failed_final:
        for s in failed_final:
            lines.append(f"- シナリオ {s['id']} が不合格: {s.get('symptom', '')}")
    else:
        lines.append("- 全シナリオが合格。画面の見た目と操作感を朝に確かめてください")
    return "\n".join(lines) + "\n"


def render_morning_report(app_dir: Path, scenarios_dir: Path, work_dir: Path, summary: dict) -> str:
    brief_path = app_dir / "product-brief.md"
    name = product_name(brief_path)
    secs = check_brief.sections(brief_path.read_text(encoding="utf-8")) if brief_path.is_file() else {}
    out_dir = work_dir / "out"
    final = json.loads((out_dir / "final.json").read_text(encoding="utf-8")) if (out_dir / "final.json").is_file() else None
    eoe = json.loads((out_dir / "eval-of-eval.json").read_text(encoding="utf-8")) if (out_dir / "eval-of-eval.json").is_file() else None
    prod_smoke = json.loads((out_dir / "prod-smoke.json").read_text(encoding="utf-8")) if (out_dir / "prod-smoke.json").is_file() else None
    prod_eval = json.loads((out_dir / "prod-eval.json").read_text(encoding="utf-8")) if (out_dir / "prod-eval.json").is_file() else None
    audit = json.loads((out_dir / "audit.json").read_text(encoding="utf-8")) if (out_dir / "audit.json").is_file() else None

    history = []
    for p in sorted(out_dir.glob("*.json")):
        if re.match(r"^\d{8}T\d{6}Z-", p.name):
            doc = json.loads(p.read_text(encoding="utf-8"))
            sc = doc.get("scenarios", [])
            passed = sum(1 for s in sc if s.get("result") == "pass")
            history.append(f"`{doc.get('version', '?')}` ({passed}/{len(sc)} 合格)")

    lines = [
        f"# 朝の報告: {name}",
        "",
        "## できたもの",
        "",
        f"- 最後のコミット: `{summary.get('final_version') or summary.get('head') or 'なし'}` "
        f"(昼のあとのコミット {summary.get('commits_after_day', 0)} 本、未コミットの変更: "
        f"{'あり' if summary.get('left_dirty') else 'なし'})",
        f"- デプロイ可能か (Deploy Gate): {'はい' if summary.get('deploy_ready') else 'いいえ'}",
        f"- かかった時間: {summary.get('minutes', 0)} 分 "
        f"(ラウンド数: {summary.get('rounds_executed', 1)}、ロールバック: {summary.get('rollbacks', 0)} 回、"
        f"resume_epoch: {summary.get('resume_epoch', 0)})",
    ]
    if prod_smoke:
        smoke_ok = not prod_smoke.get("errors")
        lines.append(f"- 本番 URL: {prod_smoke['base']} (smoke: {'合格' if smoke_ok else '不合格'})")
    else:
        lines.append("- 本番 URL: 未デプロイ (手元の版まで)")
    lines.append("- 外したブレーキ: なし (既定のブレーキのまま)")

    lines.extend([
        "",
        "## 評価の結果と証跡",
        "",
    ])
    if final and final.get("scenarios"):
        sc = final["scenarios"]
        passed = sum(1 for s in sc if s["result"] == "pass")
        lines.append(f"- 最終判定: {passed}/{len(sc)} 合格 (証跡: `out/final.json`、`out/eval-report.md`)")
        for s in sc:
            obs = " / ".join(run_eval.describe(c["observed"]) for c in s.get("checks", []))
            mark = "合格" if s["result"] == "pass" else "不合格"
            lines.append(f"  - {s['id']} ({s.get('name') or s.get('symptom', '')}): {mark} ({obs})")
    else:
        lines.append("- 最終判定: 未実施")

    if history:
        lines.append(f"- 夜のあいだの評価の依頼 ({len(history)} 回): " + " -> ".join(history))
    else:
        lines.append("- 夜のあいだの評価の依頼: 0 回")

    if eoe:
        lines.append(f"- 評価の評価 (壊した版で落ちるか): {'合格' if eoe.get('ok') else '要見直し'} (`out/eval-of-eval.json`)")
    if prod_eval and prod_eval.get("scenarios"):
        psc = prod_eval["scenarios"]
        ppassed = sum(1 for s in psc if s["result"] == "pass")
        lines.append(f"- 本番 URL でのシナリオ評価: {ppassed}/{len(psc)} 合格 (`out/prod-eval.json`)")

    decisions = bullet_items(secs.get("夜に決めたこと", ""))
    lines.extend(["", "## 夜に決めたこと", ""])
    if decisions:
        for d in decisions:
            lines.append(f"- {d}")
    else:
        lines.append("- 記録なし")

    stopped = bullet_items(secs.get("止まったこと", ""))
    if summary.get("stopped_by") == "stop_switch":
        stopped.append("停止スイッチ (AGENT_STOP_FILE) が入ったため、夜の実行を途中で止めた")
    elif summary.get("stopped_by") == "timeout" or summary.get("exit") == 124:
        stopped.append("制限時間に達したため、夜の実行を打ち切った")
    if summary.get("left_dirty"):
        stopped.append("作業ツリーに未コミットの変更が残っている (最終判定には含めていない)")
    if final and not final.get("ok"):
        failed_ids = [f"{s['id']} ({s.get('symptom', '')})" for s in final.get("scenarios", []) if s["result"] != "pass"]
        stopped.append("最終判定で落ちたシナリオがある: " + "、".join(failed_ids))
    if audit and not audit.get("ok"):
        audit_ids = [f"{f['id']} ({f.get('title', '')})" for f in audit.get("findings", []) if f.get("status") == "問題あり"]
        stopped.append("セキュリティ監査で問題が見つかったため本番公開を止めた: " + "、".join(audit_ids))
    if prod_smoke and prod_smoke.get("errors"):
        stopped.append("本番の smoke 検査でエラーが出た: " + "、".join(e["code"] for e in prod_smoke["errors"]))

    lines.extend(["", "## 止まったこと", ""])
    if stopped:
        for st in stopped:
            lines.append(f"- {st}")
    else:
        lines.append("- なし")

    return "\n".join(lines) + "\n"


def _activity_fingerprint(log_path: Path, ready_path: Path, app_dir: Path) -> tuple:
    log_sz = log_path.stat().st_size if log_path.is_file() else 0
    ready_mt = ready_path.stat().st_mtime_ns if ready_path.is_file() else 0
    git_mt = 0
    for p in app_dir.rglob("*"):
        if ".git" in p.parts:
            continue
        try:
            mt = p.stat().st_mtime_ns
            if mt > git_mt:
                git_mt = mt
        except OSError:
            pass
    return (log_sz, ready_mt, git_mt)


def run_local(app_dir: Path, scenarios_dir: Path, work_dir: Path, cmd: list[str], port: int = 8787,
              start_cmd: str = "sh start.sh", minutes: float = 45.0, watch_interval: float = 0.2,
              startup_timeout: float = 15.0, inactivity_seconds: float | None = 600.0,
              round_num: int | None = None) -> tuple[int | None, str | None]:
    handoff = work_dir / "handoff"
    feedback = work_dir / "feedback" / "eval-feedback.md"
    out_dir = work_dir / "out"
    stop_file = Path(os.environ.get("AGENT_STOP_FILE", work_dir / "STOP"))
    deadline_dt = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=minutes)

    stop_watch = threading.Event()

    def watcher():
        while not stop_watch.is_set():
            try:
                eval_watch.once(handoff=handoff, scenarios=scenarios_dir, report_dir=out_dir,
                                feedback=feedback, app_host="127.0.0.1")
            except Exception:
                pass
            stop_watch.wait(watch_interval)

    t = threading.Thread(target=watcher, daemon=True)
    t.start()

    env = {
        **os.environ,
        "EVAL_HANDOFF": str((handoff / "ready.json").resolve()),
        "EVAL_FEEDBACK": str(feedback.resolve()),
        "EVAL_PROMPT": str((handoff / "prompt.md").resolve()),
        "RUN_STATE_DIR": str((work_dir / "state").resolve()),
        "AGENT_STOP_FILE": str(stop_file.resolve()),
        "RUN_DEADLINE": deadline_dt.isoformat(),
        "STOP_GUARD_CHECKLIST": str((work_dir / "state" / "checklist.txt").resolve()),
        "APP_PORT": str(port),
        "GSF_ROUND": str(round_num or 1),
    }

    log_name = f"implementer-r{round_num:03d}.log" if round_num else "implementer.log"
    log_path = work_dir / log_name
    ready_path = handoff / "ready.json"
    stopped_by = None
    exit_code = None
    deadline_mono = time.monotonic() + minutes * 60.0
    last_fp = _activity_fingerprint(log_path, ready_path, app_dir)
    last_activity = time.monotonic()
    last_fp_check = last_activity
    try:
        with open(log_path, "w", encoding="utf-8") as log_file:
            proc = subprocess.Popen(cmd, cwd=app_dir, env=env, stdout=log_file, stderr=subprocess.STDOUT,
                                    start_new_session=True)
            while proc.poll() is None:
                now_mono = time.monotonic()
                if stop_file.exists():
                    stopped_by = "stop_switch"
                    terminate_process(proc)
                    break
                if now_mono >= deadline_mono:
                    stopped_by = "timeout"
                    terminate_process(proc)
                    exit_code = 124
                    break
                if inactivity_seconds is not None and now_mono - last_fp_check >= 0.2:
                    last_fp_check = now_mono
                    fp = _activity_fingerprint(log_path, ready_path, app_dir)
                    if fp != last_fp:
                        last_fp = fp
                        last_activity = now_mono
                    elif now_mono - last_activity >= inactivity_seconds:
                        stopped_by = "stalled"
                        terminate_process(proc)
                        exit_code = 125
                        break
                time.sleep(0.05)
            if exit_code is None:
                exit_code = proc.returncode
    finally:
        stop_watch.set()
        t.join(timeout=2.0)
        try:
            eval_watch.once(handoff=handoff, scenarios=scenarios_dir, report_dir=out_dir,
                            feedback=feedback, app_host="127.0.0.1")
        except Exception:
            pass
    return exit_code, stopped_by


def docker_override(path: Path, image: str, command: list[str], subnet: str | None = None,
                    extra_volumes: list[str] | None = None) -> Path:
    svc: dict = {"image": image, "command": command, "entrypoint": []}
    if extra_volumes:
        svc["volumes"] = extra_volumes
    doc: dict = {"services": {"implementer": svc}}
    if subnet:
        doc["networks"] = {"night": {"ipam": {"config": [{"subnet": subnet}]}}}
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


def run_docker(app_dir: Path, scenarios_dir: Path, work_dir: Path, cmd: list[str], port: int = 8787,
               start_cmd: str = "sh start.sh", minutes: float = 45.0, image: str = "python:3.12-slim-bookworm",
               subnet: str | None = None) -> tuple[int | None, str | None, dict]:
    out_dir = work_dir / "out"
    stop_file = Path(os.environ.get("AGENT_STOP_FILE", work_dir / "STOP"))
    night_yaml = docker_override(work_dir / "night.yaml", image, cmd, subnet=subnet)
    files = [COMPOSE, night_yaml]
    compose = ["docker", "compose"] + [x for f in files for x in ("-f", str(f))]
    env = {
        **os.environ,
        "RUN_NAME": f"gsf-df-{work_dir.name.lower()}",
        "RUN_UID": str(os.getuid()),
        "RUN_GID": str(os.getgid()),
        "APP_DIR": str(app_dir.resolve()),
        "HANDOFF_DIR": str((work_dir / "handoff").resolve()),
        "FEEDBACK_DIR": str((work_dir / "feedback").resolve()),
        "SCENARIOS_DIR": str(scenarios_dir.resolve()),
        "REPORT_DIR": str(out_dir.resolve()),
        "EVAL_SCRIPTS": str(HERE.resolve()),
    }
    stopped_by = None
    exit_code = None
    final = None
    try:
        sh(compose + ["up", "-d", "evaluator", "implementer"], env=env)
        deadline = time.monotonic() + minutes * 60.0
        while time.monotonic() < deadline:
            if stop_file.exists():
                stopped_by = "stop_switch"
                subprocess.run(compose + ["stop", "implementer"], env=env, capture_output=True)
                break
            ps = subprocess.run(compose + ["ps", "-a", "--format", "json", "implementer"],
                                env=env, capture_output=True, text=True)
            rows = [json.loads(x) for x in ps.stdout.splitlines() if x.strip().startswith("{")]
            if rows and rows[0].get("State") == "exited":
                exit_code = rows[0].get("ExitCode")
                break
            time.sleep(2)
        else:
            stopped_by = "timeout"
            exit_code = 124
            subprocess.run(compose + ["stop", "implementer"], env=env, capture_output=True)

        with open(work_dir / "implementer.log", "w", encoding="utf-8") as f:
            subprocess.run(compose + ["logs", "--no-color", "--no-log-prefix", "implementer"],
                           env=env, stdout=f, stderr=subprocess.STDOUT)
        with open(work_dir / "evaluator.log", "w", encoding="utf-8") as f:
            subprocess.run(compose + ["logs", "--no-color", "evaluator"],
                           env=env, stdout=f, stderr=subprocess.STDOUT)

        sh(compose + ["stop", "evaluator"], env=env)
        rev = sh(["git", "-C", str(app_dir), "rev-parse", "--short", "HEAD"]).stdout.strip()
        final_yaml = docker_override(
            work_dir / "final.yaml", image,
            ["sh", "-c", (f"if command -v git >/dev/null 2>&1; then git clone -q /work/app /tmp/final; "
                          f"else cp -a /work/app /tmp/final; fi && cd /tmp/final && PORT={port} exec {start_cmd}")],
            subnet=subnet,
        )
        fcompose = ["docker", "compose"] + [x for f in (COMPOSE, final_yaml) for x in ("-f", str(f))]
        sh(fcompose + ["up", "-d", "--force-recreate", "implementer"], env=env)
        for _ in range(30):
            subprocess.run(fcompose + ["run", "--rm", "-T", "evaluator", "python3", "-I", "/eval/bin/run_eval.py",
                                       "--scenarios", "/eval/scenarios", "--base", f"http://implementer:{port}",
                                       "--report", "/eval/out/final.json", "--feedback", "/eval/feedback/final-feedback.md",
                                       "--version", rev], env=env, capture_output=True, text=True)
            if (out_dir / "final.json").is_file():
                final = json.loads((out_dir / "final.json").read_text(encoding="utf-8"))
                if not any(c["observed"].get("status") == "応答なし" for s in final["scenarios"] for c in s["checks"]):
                    break
            time.sleep(1)
    finally:
        subprocess.run(compose + ["down", "--remove-orphans", "-t", "2"], env=env, capture_output=True)
    return exit_code, stopped_by, final


def run_factory(app_dir: Path, scenarios_dir: Path, work_dir: Path, mode: str = "local",
                agent: str = "custom", implementer_cmd: str | list[str] | None = None,
                start_cmd: str = "sh start.sh", port: int = 8787, minutes: float = 45.0,
                verify_url: str | None = None, install_skills: bool = False, dry_run: bool = False,
                model: str | None = None, effort: str = "medium", image: str = "python:3.12-slim-bookworm",
                subnet: str | None = None, watch_interval: float = 0.2, startup_timeout: float = 15.0,
                max_rounds: int = 5, round_minutes: float | None = None,
                inactivity_seconds: float | None = 600.0, stagnation_limit: int = 3,
                resume: bool = False, extra_rounds: int = 0) -> dict:
    deadline_dt = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=minutes)
    out_dir = work_dir / "out"
    feedback_file = work_dir / "feedback" / "eval-feedback.md"
    stop_file = Path(os.environ.get("AGENT_STOP_FILE", work_dir / "STOP"))

    if resume:
        if not ledger_path(work_dir).is_file():
            raise FileNotFoundError(f"resume に必要な台帳が無い: {ledger_path(work_dir)}")
        prep = {
            "prompt": str(work_dir / "handoff" / "prompt.md"),
            "settings": str(work_dir / "claude-settings" / "settings.json"),
            "checklist": str(work_dir / "state" / "checklist.txt"),
            "handoff_file": "/work/handoff/ready.json" if mode == "docker" else str((work_dir / "handoff" / "ready.json").resolve()),
            "feedback_file": "/work/feedback/eval-feedback.md" if mode == "docker" else str(feedback_file.resolve()),
            "deadline": deadline_dt.isoformat(),
        }
    else:
        prep = prepare_workspace(app_dir=app_dir, work_dir=work_dir, scenarios_dir=scenarios_dir,
                                 install_skills=install_skills, deadline=deadline_dt, port=port,
                                 start_cmd=start_cmd, mode=mode)

    compose_files = [COMPOSE]
    if mode == "docker":
        cmd_preview = (["sh", "-c", implementer_cmd] if isinstance(implementer_cmd, str)
                       else (implementer_cmd or default_agent_cmd(agent, work_dir, model, effort, mode)))
        night_yaml = docker_override(work_dir / "night.yaml", image, cmd_preview, subnet=subnet)
        compose_files = [COMPOSE, night_yaml]

    pre = preflight(app_dir=app_dir, scenarios_dir=scenarios_dir, work_dir=work_dir, mode=mode,
                    compose_files=compose_files)
    (out_dir / "preflight.json").write_text(json.dumps(pre, ensure_ascii=False, indent=2), encoding="utf-8")
    if not pre["ok"] or dry_run:
        return {"ok": pre["ok"], "dry_run": dry_run, "preflight": pre, "work_dir": str(work_dir)}

    initial_rev = sh(["git", "-C", str(app_dir), "rev-parse", "--short", "HEAD"]).stdout.strip()
    day_commits_now = int(sh(["git", "-C", str(app_dir), "rev-list", "--count", "HEAD"]).stdout.strip())
    ledger = load_ledger(work_dir, initial_rev=initial_rev, day_commits=day_commits_now)
    if resume:
        ledger["resume_epoch"] = int(ledger.get("resume_epoch", 0)) + 1
        target_rounds = len(ledger["rounds"]) + (extra_rounds or max_rounds)
    else:
        target_rounds = max(1, max_rounds)
    day_commits = int(ledger.get("day_commits", day_commits_now))
    save_ledger(work_dir, ledger)

    if implementer_cmd is not None:
        cmd = ["sh", "-c", implementer_cmd] if isinstance(implementer_cmd, str) else list(implementer_cmd)
    else:
        cmd = default_agent_cmd(agent, work_dir, model=model, effort=effort, mode=mode)

    base_prompt_path = work_dir / "state" / "base-prompt.md"
    base_prompt = (base_prompt_path.read_text(encoding="utf-8")
                   if base_prompt_path.is_file()
                   else (work_dir / "handoff" / "prompt.md").read_text(encoding="utf-8"))

    t0 = time.monotonic()
    overall_deadline = t0 + minutes * 60.0
    exit_code: int | None = None
    stopped_by: str | None = None
    final: dict | None = None
    fatal_error: str | None = None

    try:
        if mode == "docker":
            round_num = len(ledger["rounds"]) + 1
            exit_code, stopped_by, final = run_docker(app_dir, scenarios_dir, work_dir, cmd, port=port,
                                                      start_cmd=start_cmd, minutes=minutes, image=image, subnet=subnet)
            end_rev = sh(["git", "-C", str(app_dir), "rev-parse", "--short", "HEAD"]).stdout.strip()
            sat = float(final.get("satisfaction", 0.0)) if final else 0.0
            eval_ok = bool(final and final.get("ok"))
            ledger["rounds"].append({
                "round": round_num,
                "epoch": ledger["resume_epoch"],
                "start_rev": initial_rev,
                "end_rev": end_rev,
                "satisfaction": sat,
                "eval_ok": eval_ok,
                "status": "passed" if eval_ok else (stopped_by or "failed"),
                "rolled_back": False,
            })
            if sat > float(ledger.get("best_satisfaction", -1.0)):
                ledger["best_rev"] = end_rev
                ledger["best_satisfaction"] = sat
            save_ledger(work_dir, ledger)
        else:
            start_round = len(ledger["rounds"]) + 1
            for round_num in range(start_round, target_rounds + 1):
                if stop_file.exists():
                    stopped_by = "stop_switch"
                    break
                remaining_min = (overall_deadline - time.monotonic()) / 60.0
                if remaining_min <= 0:
                    stopped_by = "timeout"
                    exit_code = 124
                    break

                round_budget = min(remaining_min, round_minutes) if round_minutes else remaining_min
                prompt_text = render_round_prompt(
                    base_prompt, ledger, round_num=round_num, max_rounds=target_rounds,
                    remaining_minutes=remaining_min, feedback_path=feedback_file,
                    stagnation_limit=stagnation_limit,
                )
                (work_dir / "handoff" / "prompt.md").write_text(prompt_text, encoding="utf-8")

                start_rev = sh(["git", "-C", str(app_dir), "rev-parse", "--short", "HEAD"]).stdout.strip()
                started_at = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
                exit_code, r_stopped = run_local(
                    app_dir, scenarios_dir, work_dir, cmd, port=port, start_cmd=start_cmd,
                    minutes=round_budget, watch_interval=watch_interval,
                    startup_timeout=startup_timeout, inactivity_seconds=inactivity_seconds,
                    round_num=round_num,
                )
                ended_at = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
                end_rev = sh(["git", "-C", str(app_dir), "rev-parse", "--short", "HEAD"]).stdout.strip()

                if r_stopped == "stop_switch":
                    stopped_by = "stop_switch"
                    ledger["rounds"].append({
                        "round": round_num, "epoch": ledger["resume_epoch"],
                        "started_at": started_at, "ended_at": ended_at,
                        "start_rev": start_rev, "end_rev": end_rev,
                        "satisfaction": 0.0, "eval_ok": False,
                        "status": "stop_switch", "rolled_back": False,
                    })
                    save_ledger(work_dir, ledger)
                    break

                round_rep_path = out_dir / f"round-{round_num:03d}.json"
                round_eval = judge_clean_checkout(
                    app_dir, scenarios_dir, work_dir, start_cmd=start_cmd,
                    startup_timeout=startup_timeout, report_path=round_rep_path,
                    feedback_path=feedback_file, run_audit=False,
                )
                sat = float(round_eval.get("satisfaction", 0.0))
                eval_ok = bool(round_eval.get("ok"))
                best_sat = float(ledger.get("best_satisfaction", -1.0))
                rolled_back = False
                r_status = "passed" if eval_ok else (r_stopped or "failed")

                if eval_ok:
                    ledger["best_rev"] = end_rev
                    ledger["best_satisfaction"] = sat
                    ledger["consecutive_no_progress"] = 0
                elif best_sat >= 0.0 and sat < best_sat and ledger.get("best_rev"):
                    branch = rollback_to_best(app_dir, ledger["best_rev"], round_num)
                    rolled_back = True
                    r_status = "regressed"
                    ledger["consecutive_no_progress"] = int(ledger.get("consecutive_no_progress", 0)) + 1
                    ledger.setdefault("dead_ends", []).append(
                        f"round {round_num} ({end_rev}): satisfaction が {best_sat:.3f} -> {sat:.3f} に退行したため "
                        f"`{ledger['best_rev']}` に戻した (退避ブランチ: `{branch}`)"
                    )
                elif sat > best_sat:
                    ledger["best_rev"] = end_rev
                    ledger["best_satisfaction"] = sat
                    ledger["consecutive_no_progress"] = 0
                else:
                    ledger["consecutive_no_progress"] = int(ledger.get("consecutive_no_progress", 0)) + 1
                    if r_stopped == "stalled":
                        ledger.setdefault("dead_ends", []).append(
                            f"round {round_num} ({end_rev}): 無活動タイムアウトにより中断"
                        )

                ledger["rounds"].append({
                    "round": round_num, "epoch": ledger["resume_epoch"],
                    "started_at": started_at, "ended_at": ended_at,
                    "start_rev": start_rev, "end_rev": end_rev,
                    "satisfaction": sat, "eval_ok": eval_ok,
                    "status": r_status, "rolled_back": rolled_back,
                })
                save_ledger(work_dir, ledger)

                if eval_ok:
                    stopped_by = None
                    break
                if r_stopped == "timeout" and (overall_deadline - time.monotonic()) <= 0:
                    stopped_by = "timeout"
                    break

            final = judge_clean_checkout(app_dir, scenarios_dir, work_dir, start_cmd=start_cmd,
                                         startup_timeout=startup_timeout)
    except BaseException as e:
        fatal_error = f"{type(e).__name__}: {e}"
        stopped_by = stopped_by or "error"
    finally:
        save_ledger(work_dir, ledger)
        tree = tree_state(app_dir, day_commits=day_commits)
        elapsed_min = round((time.monotonic() - t0) / 60.0, 2)
        requests = sorted(p.name for p in out_dir.glob("*.json") if re.match(r"^\d{8}T\d{6}Z-", p.name))
        final_ok = bool(final and final.get("ok"))
        audit_path = out_dir / "audit.json"
        audit_doc = json.loads(audit_path.read_text(encoding="utf-8")) if audit_path.is_file() else None
        audit_ok = bool(audit_doc["ok"]) if audit_doc is not None else True
        gate = deploy_gate.check(app_repo=app_dir, eval_report=out_dir / "final.json",
                                 audit_report=audit_path if audit_path.is_file() else None)
        deploy_ready = final_ok and gate["ok"] and stopped_by != "stop_switch" and not fatal_error

        prod_smoke = None
        prod_eval = None
        if verify_url and not fatal_error:
            prod_smoke = smoke.check(verify_url)
            (out_dir / "prod-smoke.json").write_text(json.dumps(prod_smoke, ensure_ascii=False, indent=2), encoding="utf-8")
            prod_eval = run_eval.run(scenarios=scenarios_dir, base=verify_url, app_repo=None,
                                     report=out_dir / "prod-eval.json", feedback=None, version=verify_url)

        summary = {
            "ok": deploy_ready and (prod_eval["ok"] if prod_eval else True) and (not prod_smoke["errors"] if prod_smoke else True),
            "mode": mode,
            "exit": exit_code,
            "stopped_by": stopped_by,
            "fatal_error": fatal_error,
            "minutes": elapsed_min,
            "rounds_executed": len(ledger.get("rounds", [])),
            "rollbacks": sum(1 for r in ledger.get("rounds", []) if r.get("rolled_back")),
            "resume_epoch": ledger.get("resume_epoch", 0),
            "best_rev": ledger.get("best_rev"),
            "eval_requests": len(requests),
            "final": {s["id"]: s["result"] for s in final["scenarios"]} if final else None,
            "final_ok": final_ok,
            "final_version": final["version"] if final else None,
            "audit_ok": audit_ok,
            "deploy_ready": deploy_ready,
            **tree,
            "verify_url": verify_url,
            "prod_smoke_ok": (not prod_smoke["errors"]) if prod_smoke else None,
            "prod_eval_ok": prod_eval["ok"] if prod_eval else None,
            "workspace": prep,
        }
        (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        (out_dir / "eval-report.md").write_text(render_eval_report(app_dir, scenarios_dir, work_dir), encoding="utf-8")
        (out_dir / "morning-report.md").write_text(render_morning_report(app_dir, scenarios_dir, work_dir, summary),
                                                   encoding="utf-8")
    return summary


def pair_arg(s: str) -> tuple[str, str]:
    name, sep, url = s.partition("=")
    if not sep or not name or not url:
        raise argparse.ArgumentTypeError(f"expected NAME=URL, got {s!r}")
    return name, url


def _add_run_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--app-dir", type=Path, required=True)
    p.add_argument("--scenarios", type=Path, required=True)
    p.add_argument("--work-dir", type=Path, required=True)
    p.add_argument("--mode", choices=("local", "docker"), default="local")
    p.add_argument("--agent", choices=AGENTS, default="claude")
    p.add_argument("--implementer-cmd", help="shell command for the implementer (required when --agent=custom)")
    p.add_argument("--start-cmd", default="sh start.sh")
    p.add_argument("--port", type=int, default=8787)
    p.add_argument("--minutes", type=float, default=45.0)
    p.add_argument("--max-rounds", type=int, default=5)
    p.add_argument("--round-minutes", type=float)
    p.add_argument("--inactivity-seconds", type=float, default=600.0)
    p.add_argument("--stagnation-limit", type=int, default=3)
    p.add_argument("--verify-url", help="deployed URL to run smoke.py and scenarios against")
    p.add_argument("--install-skills", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--model")
    p.add_argument("--effort", default="medium")
    p.add_argument("--image", default="python:3.12-slim-bookworm")
    p.add_argument("--subnet", default=os.environ.get("GSF_DOCKER_SUBNET"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="subcmd", required=True)

    p_pre = sub.add_parser("preflight", help="check product-brief.md, scenarios, stop switch, and isolation")
    p_pre.add_argument("--app-dir", type=Path, required=True)
    p_pre.add_argument("--scenarios", type=Path, required=True)
    p_pre.add_argument("--work-dir", type=Path, required=True)
    p_pre.add_argument("--mode", choices=("local", "docker"), default="local")
    p_pre.add_argument("--compose", type=Path, action="append")

    p_doc = sub.add_parser("doctor", help="check runtime prerequisites (git, python3, agent CLI, docker, brief)")
    p_doc.add_argument("--agent", choices=AGENTS, default="claude")
    p_doc.add_argument("--mode", choices=("local", "docker"), default="local")
    p_doc.add_argument("--app-dir", type=Path)

    p_eoe = sub.add_parser("eval-of-eval", help="verify reference passes and broken variants fail")
    p_eoe.add_argument("--scenarios", type=Path, required=True)
    p_eoe.add_argument("--report", type=Path, required=True)
    p_eoe.add_argument("--good", required=True, help="base URL of the reference app")
    p_eoe.add_argument("--break", dest="breaks", type=pair_arg, action="append", default=[], help="NAME=URL")
    p_eoe.add_argument("--timeout", type=float, default=15.0)

    p_run = sub.add_parser("run", help="run preflight, the night loop, final judgement, and write morning reports")
    _add_run_args(p_run)

    p_res = sub.add_parser("resume", help="resume an interrupted or incomplete run from state/ledger.json")
    _add_run_args(p_res)
    p_res.add_argument("--extra-rounds", type=int, default=0)

    p_rep = sub.add_parser("report", help="render eval-report.md and morning-report.md from an existing work-dir")
    p_rep.add_argument("--app-dir", type=Path, required=True)
    p_rep.add_argument("--scenarios", type=Path, required=True)
    p_rep.add_argument("--work-dir", type=Path, required=True)

    a = ap.parse_args(argv)
    if a.subcmd == "preflight":
        r = preflight(a.app_dir, a.scenarios, a.work_dir, mode=a.mode, compose_files=a.compose)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1
    if a.subcmd == "doctor":
        r = doctor(agent=a.agent, mode=a.mode, app_dir=a.app_dir)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1
    if a.subcmd == "eval-of-eval":
        r = eval_of_eval(a.scenarios, a.good, dict(a.breaks), a.report, timeout=a.timeout)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1
    if a.subcmd in ("run", "resume"):
        if a.agent == "custom" and not a.implementer_cmd:
            ap.error("--implementer-cmd is required when --agent=custom")
        r = run_factory(app_dir=a.app_dir, scenarios_dir=a.scenarios, work_dir=a.work_dir, mode=a.mode,
                        agent=a.agent, implementer_cmd=a.implementer_cmd, start_cmd=a.start_cmd, port=a.port,
                        minutes=a.minutes, verify_url=a.verify_url, install_skills=a.install_skills,
                        dry_run=a.dry_run, model=a.model, effort=a.effort, image=a.image, subnet=a.subnet,
                        max_rounds=a.max_rounds, round_minutes=a.round_minutes,
                        inactivity_seconds=a.inactivity_seconds, stagnation_limit=a.stagnation_limit,
                        resume=(a.subcmd == "resume"), extra_rounds=getattr(a, "extra_rounds", 0))
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1
    if a.subcmd == "report":
        out_dir = a.work_dir / "out"
        summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8")) if (out_dir / "summary.json").is_file() else {}
        (out_dir / "eval-report.md").write_text(render_eval_report(a.app_dir, a.scenarios, a.work_dir), encoding="utf-8")
        (out_dir / "morning-report.md").write_text(render_morning_report(a.app_dir, a.scenarios, a.work_dir, summary),
                                                   encoding="utf-8")
        print(json.dumps({"eval_report": str(out_dir / "eval-report.md"),
                          "morning_report": str(out_dir / "morning-report.md")}, ensure_ascii=False))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
