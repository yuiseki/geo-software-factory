#!/usr/bin/env python3
"""Run held-out scenarios against a running app, and hand the implementer symptoms only.

    python3 run_eval.py --scenarios DIR --base http://127.0.0.1:8787 --app-repo PATH \
                        --report OUT/report.json [--feedback PATH/eval-feedback.md]

The evaluator runs this, never the implementer. Scenarios are JSON files outside the app repository:

    {"id": "S1", "name": "...", "symptom": "one line the implementer may read",
     "checks": [{"kind": "http", "path": "/", "status": 200, "contains": "OpenStreetMap"},
                {"kind": "geojson", "path": "/places.geojson", "bbox": [W, S, E, N], "min_features": 10,
                 "require": ["name"]},
                {"kind": "command", "run": ["npx", "playwright", "test", "s1.spec.ts"], "timeout": 300}]}

A command runs in the scenario directory with EVAL_BASE_URL set, passes on exit 0, and may print lines starting
with "OBSERVED:" for the implementer; the rest of its output stays in the report.

Separation is enforced, not promised (with --app-repo; in the isolated containers of assets/isolation/ the mounts
do it, and the version comes from --version): it refuses scenarios or a report inside the app repository (they hold the
thresholds), and a feedback file outside it. The feedback names the version judged, each failed scenario's
symptom line, the paths requested and what was observed there (status, feature count, error codes), and never
the scenario's name, expected values or thresholds. The report holds everything, for the morning.

Exit 0: every scenario passed. Exit 1: a scenario failed or could not be judged. Exit 2: refused.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import geocheck  # noqa: E402

OBSERVED = "OBSERVED:"
JUDGE_AGENTS = ("claude", "codex", "gemini", "opencode", "qoder")


class Refused(Exception):
    pass


def inside(path: Path, root: Path) -> bool:
    path, root = path.resolve(), root.resolve()
    return path == root or root in path.parents


def fetch(url: str, timeout: float):
    req = urllib.request.Request(url, headers={"User-Agent": "geo-software-eval"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(20_000_000)
    except urllib.error.HTTPError as e:
        return e.code, e.read(1_000_000)
    except (urllib.error.URLError, OSError) as e:
        return None, str(e).encode()


def default_judge_cmd(agent: str, model: str | None = None) -> list[str]:
    if agent == "claude":
        mflag = f"--model {shlex.quote(model)} " if model else ""
        return ["sh", "-c", f"claude -p --output-format text --no-session-persistence {mflag}"]
    if agent == "codex":
        m = model or "gpt-6-luna"
        return ["sh", "-c", f"codex exec --skip-git-repo-check -m {shlex.quote(m)} -"]
    if agent == "gemini":
        m = model or "gemini-3.8-flash-low"
        return ["sh", "-c", f"agy --print=\"$(cat)\" --model {shlex.quote(m)} --dangerously-skip-permissions"]
    if agent == "opencode":
        mflag = f"-m {shlex.quote(model)} " if model else ""
        return ["sh", "-c", f"opencode run --pure {mflag}\"$(cat)\""]
    if agent == "qoder":
        m = model or "Auto"
        return ["sh", "-c", f"qodercli -p --output-format text --no-session-persistence --model {shlex.quote(m)}"]
    raise ValueError(f"unknown judge agent {agent!r}")


def parse_judge_json(text: str) -> dict | None:
    text = text.strip()
    if not text:
        return None
    for candidate in [text] + re.findall(r"\{[^{}]*\}", text, flags=re.DOTALL):
        try:
            doc = json.loads(candidate)
            if isinstance(doc, dict) and "pass" in doc:
                return doc
        except ValueError:
            continue
    return None


def invoke_judge(prompt: str, c: dict, cwd: Path, timeout: float) -> dict:
    cmd = c.get("judge_cmd") or os.environ.get("EVAL_JUDGE_CMD")
    if isinstance(cmd, str):
        run_cmd = ["sh", "-c", cmd]
    elif isinstance(cmd, list):
        run_cmd = [str(x) for x in cmd]
    else:
        agent = c.get("agent") or os.environ.get("EVAL_JUDGE_AGENT")
        model = c.get("model") or os.environ.get("EVAL_JUDGE_MODEL")
        if not agent:
            return {"error": "no_judge_configured"}
        try:
            run_cmd = default_judge_cmd(agent, model)
        except ValueError as e:
            return {"error": str(e)}
    try:
        p = subprocess.run(run_cmd, input=prompt, cwd=cwd, capture_output=True, text=True,
                           timeout=c.get("timeout", timeout))
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except OSError as e:
        return {"error": str(e)}
    if p.returncode != 0:
        return {"error": f"exit {p.returncode}", "stderr": p.stderr[-1000:]}
    parsed = parse_judge_json(p.stdout)
    if parsed is None:
        return {"error": "invalid_json", "stdout": p.stdout[-1000:]}
    return {"doc": parsed}


def run_llm_check(c: dict, base: str, cwd: Path, timeout: float) -> dict:
    """Run an independent LLM-as-a-Judge check following judging.md rules."""
    path = c.get("path", "/")
    status, body = fetch(base + path, timeout)
    observed: dict = {"kind": "llm", "path": path, "status": status}
    if status is None:
        observed["status"] = "応答なし"
        return {"ok": False, "full": {**c, "error": body.decode(errors="replace")[:300]}, "observed": observed}
    if status != c.get("status", 200):
        return {"ok": False, "full": {**c, "got_status": status}, "observed": observed}
    excerpt = body.decode(errors="replace")[:8000]
    rubric = c.get("rubric", "")
    votes_n = max(1, int(c.get("votes", 1)))
    min_conf = float(c.get("min_confidence", 0.7))
    prompt = "\n".join([
        "あなたは独立した評価者 (LLM-as-a-Judge) です。実装のコードは読まず、下の観測と判定の観点だけで判定してください。",
        "次の JSON 1 個だけを出力してください:",
        '{"pass": true または false, "confidence": 0.0〜1.0, "evidence": "根拠にした観測の抜粋", "observed": "実装者に伝えてよい現象 1 行 (閾値や観点の文面は含めない)"}',
        "根拠の観測が無い場合は pass を false にしてください。",
        "",
        f"判定の観点 (Rubric): {rubric}",
        "",
        f"観測 (Path: {path}, Status: {status}):",
        "<<<OBSERVATION>>>",
        excerpt,
        "<<<END_OBSERVATION>>>",
    ])
    ballots = []
    for _ in range(votes_n):
        res = invoke_judge(prompt, c, cwd, timeout)
        if "error" in res:
            observed["judge"] = "未評価"
            return {"ok": None, "full": {**c, "error": res["error"], "detail": res}, "observed": observed}
        doc = res["doc"]
        raw_pass = bool(doc.get("pass"))
        evidence = str(doc.get("evidence") or "").strip()
        # Rule: 根拠の無い合格は不合格として扱う
        effective_pass = raw_pass and bool(evidence)
        conf = float(doc.get("confidence", 0.0) or 0.0)
        obs_line = str(doc.get("observed") or "").strip()
        # Scrub rubric string if accidentally echoed in observed
        if rubric and rubric in obs_line:
            obs_line = "観点の基準を満たしていない"
        ballots.append({
            "raw_pass": raw_pass,
            "effective_pass": effective_pass,
            "missing_evidence": raw_pass and not evidence,
            "confidence": conf,
            "evidence": evidence,
            "observed": obs_line,
        })
    passes = [b["effective_pass"] for b in ballots]
    split = len(set(passes)) > 1
    # Rule: 同じ観測で複数回判定させ、割れたら不合格の側に倒す
    ok = all(passes) and not split
    min_ballot_conf = min(b["confidence"] for b in ballots)
    low_confidence = min_ballot_conf < min_conf
    obs_lines = [b["observed"] for b in ballots if not b["effective_pass"] and b["observed"]]
    if not ok:
        if split:
            observed["split"] = True
        if any(b["raw_pass"] and not b["evidence"] for b in ballots):
            observed["body"] = "判定の根拠の観測が無い"
        elif obs_lines:
            observed["body"] = obs_lines[0]
        else:
            observed["body"] = "観点の基準を満たしていない"
    return {
        "ok": ok,
        "full": {
            **c,
            "got_status": status,
            "split": split,
            "low_confidence": low_confidence,
            "confidence": round(min_ballot_conf, 3),
            "ballots": ballots,
        },
        "observed": observed,
    }


def run_check(c: dict, base: str, cwd: Path, timeout: float) -> dict:
    """Returns {"ok": bool|None, "full": everything, "observed": what the implementer may read}."""
    kind = c.get("kind")
    if kind in ("http", "geojson"):
        path = c.get("path", "/")
        status, body = fetch(base + path, timeout)
        observed = {"kind": kind, "path": path, "status": status}
        if status is None:
            observed["status"] = "応答なし"
            return {"ok": False, "full": {**c, "error": body.decode(errors="replace")[:300]}, "observed": observed}
        if kind == "http":
            ok = status == c.get("status", 200)
            if ok and "contains" in c:
                ok = c["contains"].encode() in body
                if not ok:
                    observed["body"] = "期待した文言が無い"
            return {"ok": ok, "full": {**c, "got_status": status}, "observed": observed}
        if status != 200:
            return {"ok": False, "full": {**c, "got_status": status}, "observed": observed}
        try:
            doc = json.loads(body)
        except ValueError:
            observed["body"] = "JSON として読めない"
            return {"ok": False, "full": c, "observed": observed}
        rep = geocheck.check(doc, expect_bbox=c.get("bbox"), require_props=c.get("require", ()),
                             min_features=c.get("min_features", 0), allow_empty=c.get("allow_empty", False))
        observed.update(features=rep["features"], errors=[e["code"] for e in rep["errors"]])
        return {"ok": not rep["errors"], "full": {**c, "geocheck": rep}, "observed": observed}
    if kind == "command":
        try:
            p = subprocess.run(c["run"], cwd=cwd, capture_output=True, text=True,
                               timeout=c.get("timeout", 300), env={**os.environ, "EVAL_BASE_URL": base})
        except subprocess.TimeoutExpired:
            return {"ok": False, "full": {**c, "error": "timeout"}, "observed": {"kind": kind, "result": "時間切れ"}}
        except OSError as e:
            return {"ok": None, "full": {**c, "error": str(e)}, "observed": {"kind": kind}}
        lines = [ln[len(OBSERVED):].strip() for ln in p.stdout.splitlines() if ln.startswith(OBSERVED)]
        return {"ok": p.returncode == 0,
                "full": {**c, "exit": p.returncode, "stdout": p.stdout[-20_000:], "stderr": p.stderr[-20_000:]},
                "observed": {"kind": kind, "exit": p.returncode, "observed": lines}}
    if kind == "llm":
        return run_llm_check(c, base, cwd, timeout)
    return {"ok": None, "full": {**c, "error": f"unknown kind {kind!r}"}, "observed": {"kind": str(kind)}}


def git_rev(repo: Path) -> str:
    p = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    dirty = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True).stdout
    rev = p.stdout.strip() if p.returncode == 0 else "コミットなし"
    return rev + (" (未コミットの変更あり)" if dirty.strip() else "")


def describe(o: dict) -> str:
    if o["kind"] == "command":
        head = "時間切れ" if o.get("result") == "時間切れ" else f"終了コード {o.get('exit')}"
        return "; ".join([head] + o.get("observed", []))
    if "path" not in o:
        return f"判定できない確かめの種類 ({o['kind']})"
    parts = [f"{o['path']}: 状態 {o['status']}"]
    if o.get("judge") == "未評価":
        parts.append("評価者: 未評価")
    if o.get("split"):
        parts.append("判定が割れたため不合格")
    if "features" in o:
        parts.append(f"地物 {o['features']} 件")
    if o.get("errors"):
        parts.append("検出: " + ", ".join(o["errors"]))
    if "body" in o:
        parts.append(o["body"])
    return "、".join(parts)


def run(scenarios: Path, base: str, app_repo: Path | None, report: Path, feedback: Path | None = None,
        timeout: float = 15, version: str | None = None) -> dict:
    if app_repo is not None:
        if inside(scenarios, app_repo):
            raise Refused("シナリオが実装のリポジトリの中にある。外に置く")
        if inside(report, app_repo):
            raise Refused("報告には閾値が入るので、実装のリポジトリの外に書く")
        if feedback is not None and not inside(feedback, app_repo):
            raise Refused("症状の返し先は、実装のリポジトリの中にする")
    else:
        # Isolated containers: the feedback directory is the only one shared with the implementer.
        if version is None:
            raise Refused("実装のリポジトリが無いときは、判定する版を --version で渡す")
        if feedback is not None and (inside(feedback, scenarios) or inside(feedback, report.parent)):
            raise Refused("症状の返し先を、シナリオや報告と同じ場所に置かない")
    base = base.rstrip("/")
    rev = version if version is not None else git_rev(app_repo)
    results = []
    split_scenarios = []
    low_confidence_scenarios = []
    for f in sorted(scenarios.glob("*.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        sid = s.get("id", f.stem)
        checks = [run_check(c, base, scenarios, timeout) for c in s.get("checks", [])]
        if not checks or any(c["ok"] is None for c in checks):
            result = "error"
        else:
            result = "pass" if all(c["ok"] for c in checks) else "fail"
        split = any(c["full"].get("split") for c in checks)
        low_conf = any(c["full"].get("low_confidence") for c in checks)
        if split:
            split_scenarios.append(sid)
        if low_conf:
            low_confidence_scenarios.append(sid)
        results.append({"id": sid, "name": s.get("name"), "symptom": s.get("symptom", ""),
                        "result": result, "split": split, "low_confidence": low_conf, "checks": checks})
    ok = bool(results) and all(r["result"] == "pass" for r in results)
    passed_count = sum(1 for r in results if r["result"] == "pass")
    satisfaction = round(passed_count / len(results), 3) if results else 0.0
    when = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    out = {"when": when, "base": base, "version": rev, "ok": ok, "satisfaction": satisfaction,
           "split_scenarios": split_scenarios, "low_confidence_scenarios": low_confidence_scenarios,
           "scenarios": results}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    if feedback is not None:
        feedback.write_text(render_feedback(out), encoding="utf-8")
    return out


def render_feedback(out: dict) -> str:
    lines = ["# 評価の症状", "", f"- 判定した版: {out['version']}", f"- 判定した時刻: {out['when']}",
             f"- 結果: {sum(r['result'] == 'pass' for r in out['scenarios'])}/{len(out['scenarios'])} 合格", ""]
    if not out["scenarios"]:
        lines.append("シナリオが 1 本も無かった。評価は済んでいない。")
    for r in out["scenarios"]:
        if r["result"] == "pass":
            continue
        lines.append(f"## {r['id']}: {r['symptom'] or '症状の説明なし'}")
        if r["result"] == "error":
            lines.append("- 評価そのものが動かなかった。実装の不具合とは限らない")
        for c in r["checks"]:
            if c["ok"] is not True:
                lines.append(f"- {describe(c['observed'])}")
        lines.append("")
    if out["ok"]:
        lines.append("全シナリオ合格。")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--scenarios", type=Path, required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--app-repo", type=Path, help="omit only in the isolated containers, with --version")
    ap.add_argument("--version", help="the version judged, when there is no app repo to ask")
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--feedback", type=Path)
    ap.add_argument("--timeout", type=float, default=15)
    a = ap.parse_args(argv)
    try:
        out = run(a.scenarios, a.base, a.app_repo, a.report, a.feedback, a.timeout, a.version)
    except Refused as e:
        print(json.dumps({"refused": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps({"ok": out["ok"], "version": out["version"],
                      "results": {r["id"]: r["result"] for r in out["scenarios"]}}, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
